"""Core text analysis functions."""

from collections import Counter
import json
from pathlib import Path
from typing import Any


def analyze_text_file(
    file_path: Path, min_len: int = 1, encoding: str = "utf-8"
) -> tuple[int, int, int, Counter[str]]:
    """Analyze file: return line count, word count, char count, and word frequencies."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with file_path.open("r", encoding=encoding) as f:
        content = f.read()

    lines = content.splitlines()
    line_count = len(lines)
    char_count = len(content)

    # Разбиваем текст на слова и фильтруем по минимальной длине
    raw_words = content.split()
    words = [
        word.strip(".,!?:;\"'()[]{}").lower()
        for word in raw_words
        if len(word.strip(".,!?:;\"'()[]{}")) >= min_len
    ]
    word_count = len(words)
    counter = Counter(words)

    return line_count, word_count, char_count, counter


def format_output(
    line_count: int,
    word_count: int,
    char_count: int,
    top_words: list[tuple[str, int]],
    output_format: str = "text",
) -> str:
    """Format analysis statistics into text or JSON format."""
    if output_format == "json":
        data: dict[str, Any] = {
            "lines": line_count,
            "words": word_count,
            "chars": char_count,
            "top_words": [{"word": w, "count": c} for w, c in top_words],
        }
        return json.dumps(data, indent=2)

    # Форматирование по умолчанию в обычный текст (только ASCII)
    lines_res = [
        "--- Text Analysis Result ---",
        f"Lines: {line_count}",
        f"Words: {word_count}",
        f"Characters: {char_count}",
        "Top Words:",
    ]
    for word, count in top_words:
        lines_res.append(f"  {word}: {count}")

    return "\n".join(lines_res)