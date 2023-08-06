from __future__ import annotations

import logging
import os
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import combinations, product
from pprint import pformat

from numpy import array_split
from tqdm import tqdm

from plagdef.model.extension import ClusterBuilder
from plagdef.model.filtering import ClusterFilter
from plagdef.model.models import Document, Match, DocumentPairMatches, Cluster, Fragment, PlagiarismType
from plagdef.model.preprocessing import Preprocessor
from plagdef.model.seeding import SeedFinder

log = logging.getLogger(__name__)


class DocumentMatcher:
    def __init__(self, config: dict):
        self._preprocessor = Preprocessor(config['min_sent_len'], config['rem_stop_words'])
        self._seeder = SeedFinder(config['min_cos_sim'], config['min_dice_sim'])
        self._extender = ClusterBuilder(config['adjacent_sents_gap'], config['min_adjacent_sents_gap'],
                                        config['min_sent_number'], config['min_cluster_cos_sim'])
        self._cluster_filter = ClusterFilter(config['min_cluster_char_len'])
        self._adjacent_sents_gap_summary = config['adjacent_sents_gap_summary']
        self._min_verbatim_match_char_len = config['min_verbatim_match_char_len']

    def preprocess(self, lang: str, docs: set[Document], common_docs=None):
        self._preprocessor.preprocess(lang, docs, common_docs)

    def find_matches(self, docs: set[Document], archive_docs=None) -> dict[PlagiarismType, list[DocumentPairMatches]]:
        doc_combs = list(combinations(docs, 2))
        if archive_docs:
            doc_combs.update(product(docs, archive_docs))
        return self._parallelized_search(doc_combs)

    def _parallelized_search(self, doc_combs, threshold=4000):
        if len(doc_combs) > threshold:
            doc_comb_chunks = array_split(doc_combs, os.cpu_count())
            with ProcessPoolExecutor(max_workers=os.cpu_count()) as p:
                futures = []
                for chunk in doc_comb_chunks:
                    futures.append(p.submit(self._find_matches, chunk))
                match_chunks = [f.result() for f in as_completed(futures)]
            return self._merge(match_chunks)
        else:
            return self._find_matches(doc_combs)

    def _merge(self, match_chunks):
        matches = defaultdict(list)
        for chunk in match_chunks:
            for plag_type, doc_pair_matches in chunk.items():
                matches[plag_type] += doc_pair_matches
        return matches

    def _find_matches(self, doc_combs) \
        -> dict[PlagiarismType, list[DocumentPairMatches]]:
        matches = defaultdict(list)
        for doc1, doc2 in tqdm(doc_combs, desc='Matching', bar_format='{l_bar}{bar}| [{elapsed}<{remaining}{postfix}]',
                               leave=False, mininterval=1):
            log.debug(f'Examining pair ({doc1}, {doc2}).')
            seeds = self._seeder.seed(doc1, doc2)
            log.debug(f'Found the following seeds:\n{pformat(sorted(seeds, key=lambda s: s.sent1.idx))}')
            clusters = self._extender.extend(seeds)
            clusters = self._cluster_filter.filter(clusters)
            log.debug(f'Seeds were extended to the following clusters:\n{pformat(clusters)}')
            verbatim_matches = self._verbatim_matches(clusters)
            if len(verbatim_matches):
                log.debug(f'Plagiarism type is verbatim. Found these matches:\n{pformat(verbatim_matches)}')
                matches[PlagiarismType.VERBATIM].append(DocumentPairMatches(PlagiarismType.VERBATIM, verbatim_matches))
            if len(clusters):
                intelligent_matches = {Match.from_cluster(cluster) for cluster in clusters}.difference(verbatim_matches)
                if len(intelligent_matches):
                    log.debug(
                        f'Plagiarism type is intelligent. Found these matches:\n{pformat(intelligent_matches)}')
                    matches[PlagiarismType.INTELLIGENT].append(DocumentPairMatches(PlagiarismType.INTELLIGENT,
                                                                                   intelligent_matches))
            summary_clusters = self._extender.extend(seeds, self._adjacent_sents_gap_summary)
            summary_clusters = self._cluster_filter.filter(summary_clusters)
            if len(summary_clusters):
                sum_cluster_len_doc1, sum_cluster_len_doc2 = \
                    tuple(map(sum, zip(*(cluster.char_lengths() for cluster in summary_clusters))))
                if sum_cluster_len_doc1 >= 3 * sum_cluster_len_doc2 \
                    or sum_cluster_len_doc2 >= 3 * sum_cluster_len_doc1:
                    summary_matches = {Match.from_cluster(cluster) for cluster in summary_clusters}.difference(
                        verbatim_matches)
                    if len(summary_matches):
                        log.debug(f'Plagiarism type is summary. Found these matches:\n{pformat(summary_matches)}')
                        matches[PlagiarismType.SUMMARY].append(DocumentPairMatches(PlagiarismType.SUMMARY,
                                                                                   summary_matches))

        return matches

    def _verbatim_matches(self, clusters: set[Cluster]) -> set[Match]:
        matches = set()
        for cluster in clusters:
            cluster_matches = self._common_words(cluster)
            matches.update(_resolve_match_overlaps(cluster_matches))
        return matches

    def _common_words(self, cluster: Cluster) -> set[Match]:
        verbatim_matches = set()
        frag1_words = [word for sent_words in [sent.words for sent in cluster.sents_doc1] for word in sent_words]
        frag2_words = [word for sent_words in [sent.words for sent in cluster.sents_doc2] for word in sent_words]
        lookup = [[0 for _ in range(len(frag2_words) + 1)] for _ in range(len(frag1_words) + 1)]
        for i in range(1, len(frag1_words) + 1):
            for j in range(1, len(frag2_words) + 1):
                if frag1_words[i - 1].text.lower() == frag2_words[j - 1].text.lower():
                    lookup[i][j] = lookup[i - 1][j - 1] + 1
                    match_char_len = sum([len(word) for word in frag1_words[i - lookup[i][j]:i]])
                    if match_char_len >= self._min_verbatim_match_char_len:
                        frag1_first, frag2_first = i - lookup[i][j], j - lookup[i][j]
                        # Include punctuation (mostly periods) if exists
                        punct = _include_punct(cluster, frag1_words[i - 1].end_char, frag2_words[j - 1].end_char)
                        frag1 = Fragment(frag1_words[frag1_first].start_char, frag1_words[i - 1].end_char + punct,
                                         cluster.doc1)
                        frag2 = Fragment(frag2_words[frag2_first].start_char, frag2_words[j - 1].end_char + punct,
                                         cluster.doc2)
                        verbatim_matches.add(Match(frag1, frag2))
        return verbatim_matches


def _resolve_match_overlaps(matches: set[Match]) -> set[Match]:
    non_ol_matches = set()
    for match in sorted(matches, key=len, reverse=True):
        if not any(match.overlaps_with(non_ol_match) for non_ol_match in non_ol_matches):
            non_ol_matches.add(match)
    return non_ol_matches


def _include_punct(cluster: Cluster, frag1_end_char: int, frag2_end_char: int) -> int:
    if cluster.doc1.text[frag1_end_char] == cluster.doc2.text[frag2_end_char] \
        and not cluster.doc1.text[frag1_end_char].isspace():
        return 1
    return 0
