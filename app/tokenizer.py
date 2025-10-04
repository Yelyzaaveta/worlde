"""Module for tokenizing text with spaCy NLP."""

import pandas as pd
import spacy
from result import Err, Ok, Result


def tokenize_sentences(
    sentences: list[str], model_prefix: str = "sm"
) -> Result[pd.DataFrame, str]:
    """
    Tokenize sentences with spaCy and extract tokens with their POS tags.

    Each sentence is kept separate with a sentence_id to maintain paragraph structure.

    Args:
        sentences: List of sentences to process
        model_prefix: spaCy model prefix ('sm', 'md', 'lg', 'trf')

    Returns:
        Result containing DataFrame with columns: 'sentence_id', 'token_text', 'pos_tag'
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

    rows = []

    for sentence_id, sentence in enumerate(sentences):
        if not sentence or not str(sentence).strip():
            continue

        # Process the sentence with spaCy
        doc = nlp(str(sentence))

        # Extract tokens with their POS tags for this sentence
        for token in doc:
            rows.append(
                {
                    "sentence_id": sentence_id,
                    "token_text": token.text_with_ws,
                    "pos_tag": token.pos_,
                }
            )

    df = pd.DataFrame(rows)

    return Ok(df)
