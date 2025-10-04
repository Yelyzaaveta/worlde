"""Module for counting POS-tagged words from sentences."""

from collections import defaultdict

import pandas as pd
import spacy
from result import Err, Ok, Result
from spacy.lang.en import stop_words


def count_pos_words(
    sentences: list[str], model_prefix: str = "sm"
) -> Result[pd.DataFrame, str]:
    """
    Count nouns, verbs, and adjectives from sentences.

    Args:
        sentences: List of sentences to process
        model_prefix: spaCy model prefix ('sm', 'md', 'lg', 'trf')

    Returns:
        Result containing DataFrame with columns: 'word', 'POS', 'count', sorted by 'word'
        or error message
    """
    model_name = f"en_core_web_{model_prefix}"

    try:
        nlp = spacy.load(model_name)
    except OSError:
        return Err(
            f"Model '{model_name}' not found. "
            f"Please install it using: python -m spacy download {model_name}"
        )

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

    return Ok(df)
