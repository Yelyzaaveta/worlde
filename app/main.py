"""Main CLI application for word counting."""

from pathlib import Path

import typer

from app.processor import process_sentences
from app.reader import read_sentences
from app.writer import write_formatted_excel

app = typer.Typer(help="Word counting application for nouns, verbs, and adjectives")


@app.command()
def process(
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
) -> None:
    """Process sentences from Excel file and write formatted word counts."""
    typer.echo(f"Reading sentences from {excel_file}...")

    try:
        sentences = read_sentences(excel_file, sheet_name)
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

    typer.echo(f"Processing {len(sentences)} sentences...")
    words_df = process_sentences(sentences)

    noun_count = len(words_df[words_df["POS"] == "noun"])
    verb_count = len(words_df[words_df["POS"] == "verb"])
    adj_count = len(words_df[words_df["POS"] == "adj"])

    typer.echo(f"Found {len(words_df)} unique words:")
    typer.echo(f"  Nouns: {noun_count}")
    typer.echo(f"  Verbs: {verb_count}")
    typer.echo(f"  Adjectives: {adj_count}")

    typer.echo(f"Writing results to sheet '{output_sheet}'...")
    write_formatted_excel(words_df, excel_file, output_sheet)

    typer.echo(f"✓ Results written to {excel_file} (sheet: {output_sheet})")


if __name__ == "__main__":
    app()
