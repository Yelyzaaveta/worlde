"""Module for processing sentences with NLP to extract words and their POS tags."""

from collections import defaultdict

import pandas as pd
import spacy
from spacy.lang.en import stop_words


def process_sentences(sentences: list[str]) -> pd.DataFrame:
    """
    Process sentences and extract nouns, verbs, and adjectives with counts.

    Args:
        sentences: List of sentences to process

    Returns:
        DataFrame with columns: 'word', 'POS', 'count', sorted by 'word'
    """
    nlp = spacy.load("en_core_web_sm")

    nouns: dict[str, int] = defaultdict(int)
    verbs: dict[str, int] = defaultdict(int)
    adjs: dict[str, int] = defaultdict(int)

    for sentence in sentences:
        if not sentence or pd.isna(sentence):
            continue

        doc = nlp(str(sentence))

        for token in doc:
            lemma = token.lemma_.lower().strip()

            # Skip stop words, non-alphabetic tokens, and empty lemmas
            if not lemma or lemma in stop_words.STOP_WORDS or not token.is_alpha:
                continue

            pos = token.pos_

            if pos == "NOUN":
                nouns[lemma] += 1
            elif pos == "VERB":
                verbs[lemma] += 1
            elif pos == "ADJ":
                adjs[lemma] += 1

    # Build list of word records
    rows = []
    for lemma, count in nouns.items():
        rows.append({"word": lemma, "POS": "noun", "count": count})
    for lemma, count in verbs.items():
        rows.append({"word": lemma, "POS": "verb", "count": count})
    for lemma, count in adjs.items():
        rows.append({"word": lemma, "POS": "adj", "count": count})

    df = pd.DataFrame(rows)
    df = df.sort_values(by="word").reset_index(drop=True)

    return df
