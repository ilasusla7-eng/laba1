"""CLI entry point for text analyzer."""

import argparse
import sys
from pathlib import Path

from text_analyzer.core import analyze_text_file, format_output


def main() -> None:
    """Парсинг CLI аргументов и запуск аналитики."""
    parser = argparse.ArgumentParser(description="ASCII Text Analyzer CLI Tool")
    parser.add_argument("path", type=Path, help="Путь к текстовому файлу")
    parser.add_argument(
        "--top", type=int, default=10, help="Количество отображаемых слов в топе"
    )
    parser.add_argument(
        "--min-len", type=int, default=1, help="Фильтр минимальной длины слова"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Формат вывода (text или json)",
    )
    parser.add_argument(
        "--encoding", default="utf-8", help="File encoding (default: utf-8)"
    )

    args = parser.parse_args()

    try:
        lines, words, chars, counter = analyze_text_file(
            file_path=args.path, min_len=args.min_len, encoding=args.encoding
        )
        top_words = counter.most_common(args.top)
        output = format_output(
            line_count=lines,
            word_count=words,
            char_count=chars,
            top_words=top_words,
            output_format=args.format,
        )
        print(output)
    except FileNotFoundError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(
            f"Error: Failed to decode file using encoding '{args.encoding}'",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
