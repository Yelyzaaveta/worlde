"""Main CLI application for word counting."""

from pathlib import Path

import typer

from app.docx_writer import write_highlighted_docx
from app.pos_counter import count_pos_words
from app.reader import read_sentences
from app.tokenizer import tokenize_sentences
from app.writer import write_formatted_excel

app = typer.Typer(help="Word counting application for nouns, verbs, and adjectives")


def _error_and_exit(message: str | None) -> None:
    """Print error message in typer style and exit."""
    typer.secho(f"Error: {message}", fg=typer.colors.RED, err=True)
    raise typer.Exit(1)


@app.command()
def count(
    excel_file: Path = typer.Argument(
        ...,
        help="Path to the Excel file with sentences",
        exists=True,
        dir_okay=False,
    ),
    sheet_name: str | None = typer.Option(
        None,
        help="Sheet name to read (default: first sheet or 'data')",
    ),
    output_sheet: str = typer.Option(
        "results",
        help="Output sheet name for results",
    ),
    model_prefix: str = typer.Option(
        "sm",
        help="spaCy model prefix to use (sm, md, lg, trf)",
    ),
) -> None:
    """Process sentences from Excel file and write formatted word counts."""
    typer.echo(f"Reading sentences from {excel_file}...")

    # Functional composition with Result pattern
    sentences_result = read_sentences(excel_file, sheet_name)

    if sentences_result.is_err():
        _error_and_exit(sentences_result.err())

    sentences = sentences_result.unwrap()
    typer.echo(
        f"Processing {len(sentences)} sentences with model 'en_core_web_{model_prefix}'..."
    )

    words_result = count_pos_words(sentences, model_prefix)

    if words_result.is_err():
        _error_and_exit(words_result.err())

    words_df = words_result.unwrap()

    noun_count = len(words_df[words_df["POS"] == "noun"])
    verb_count = len(words_df[words_df["POS"] == "verb"])
    adj_count = len(words_df[words_df["POS"] == "adj"])

    typer.echo(f"Found {len(words_df)} unique words:")
    typer.echo(f"  Nouns: {noun_count}")
    typer.echo(f"  Verbs: {verb_count}")
    typer.echo(f"  Adjectives: {adj_count}")

    typer.echo(f"Writing results to sheet '{output_sheet}'...")

    write_result = write_formatted_excel(words_df, excel_file, output_sheet)

    if write_result.is_err():
        _error_and_exit(write_result.err())

    typer.secho(
        f"✓ Results written to {excel_file} (sheet: {output_sheet})",
        fg=typer.colors.GREEN,
    )


@app.command()
def highlight(
    excel_file: Path = typer.Argument(
        ...,
        help="Path to the Excel file with sentences",
        exists=True,
        dir_okay=False,
    ),
    output_docx: Path = typer.Argument(
        ...,
        help="Path to the output DOCX file",
    ),
    sheet_name: str | None = typer.Option(
        None,
        help="Sheet name to read (default: first sheet or 'data')",
    ),
    model_prefix: str = typer.Option(
        "sm",
        help="spaCy model prefix to use (sm, md, lg, trf)",
    ),
) -> None:
    """Create a DOCX with sentences highlighted by POS (nouns, verbs, and adjectives)."""
    typer.echo(f"Reading sentences from {excel_file}...")

    # Functional composition with Result pattern
    sentences_result = read_sentences(excel_file, sheet_name)

    if sentences_result.is_err():
        _error_and_exit(sentences_result.err())

    sentences = sentences_result.unwrap()
    typer.echo(
        f"Processing {len(sentences)} sentences with model 'en_core_web_{model_prefix}'..."
    )
    typer.echo(
        "Highlighting nouns (turquoise), verbs (yellow), and adjectives (pink)..."
    )

    tokens_result = tokenize_sentences(sentences, model_prefix)

    if tokens_result.is_err():
        _error_and_exit(tokens_result.err())

    tokens_df = tokens_result.unwrap()

    write_result = write_highlighted_docx(tokens_df, output_docx)

    if write_result.is_err():
        _error_and_exit(write_result.err())

    typer.secho(f"✓ Highlighted DOCX created at {output_docx}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
