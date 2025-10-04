# worlde

Word counting application for extracting and counting nouns, verbs, and adjectives from sentences.

## Technical Task

Завдання полягає в тому, щоб розподілити всі слова (лексеми) на три основні
групи: іменники, дієслова та прикметники.

Для іменників: форми однини та множини вважаються однією лексемою.
Для прикметників: усі ступені порівняння об'єднуються в одну лексему.
Для дієслів: усі часові, особові та видові форми рахуються як одна лексема.

Потрібно також порахувати кількість слововживань для кожної лексеми в межах її
групи. Блакитним кольором позначено речення, в яких здійснено підрахунок.
Жовтим — кількість слововживань відповідних лексем.

## Installation

1. Install dependencies using `uv`:

```bash
uv sync --all-extras
```

2. Download the spaCy English model:

```bash
uv run python -m spacy download en_core_web_sm
```

## Usage

The application provides a CLI interface to process Excel files containing sentences.

### Basic Usage

```bash
uv run python -m app.main <excel-file>
```

### Options

- `excel-file`: Path to the Excel file with sentences (required)
- `--sheet-name TEXT`: Sheet name to read (default: first sheet or 'data')
- `--output-sheet TEXT`: Output sheet name for results (default: "results")

### Examples

Process sentences from the first sheet:
```bash
uv run python -m app.main data.xlsx
```

Process sentences from a specific sheet:
```bash
uv run python -m app.main data.xlsx --sheet-name "sentences"
```

Specify custom output sheet name:
```bash
uv run python -m app.main data.xlsx --output-sheet "word_counts"
```

### Input Format

The input Excel file should contain:
- One column with sentences (no headers required)
- One sentence per row
- The application will read from the first sheet by default, or from a sheet named "data" if the first sheet is not accessible

### Output Format

The application creates a new sheet in the same Excel file with the following structure:

**Header Row:**
```
| (blank) | Nouns | (blank) | Verbs | (blank) | Adjectives | (blank) |
```

**Data Rows:**
- Column 1: Letter navigation
  - First letter (uppercase) for the first occurrence of words starting with that letter
  - Second letter (lowercase) for subsequent rows
- Columns 2-3: Noun word and its count
- Columns 4-5: Verb word and its count
- Columns 6-7: Adjective word and its count

Words are grouped alphabetically by their first and second letters, with all three parts of speech displayed in the same row when they share the same letter pattern.

## Development

### Code Structure

- `app/reader.py`: Reads sentences from Excel files
- `app/processor.py`: Processes sentences with spaCy NLP to extract and count words
- `app/writer.py`: Writes formatted results to Excel
- `app/main.py`: CLI application entry point

### Running Linters

Check code quality with ruff:
```bash
uv run ruff check app/
```

Check type annotations with mypy:
```bash
uv run mypy app/
```

Format code with ruff:
```bash
uv run ruff format app/
```
