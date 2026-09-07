"""CLI entry point for text analyzer."""

import argparse
from pathlib import Path
import sys

from text_analyzer.core import analyze_text_file, format_output


def main() -> None:
    """Parse CLI arguments and run analysis."""
    parser = argparse.ArgumentParser(
        description="ASCII Text Analyzer CLI Tool"
    )
    parser.add_argument("path", type=Path, help="Path to text file")
    parser.add_argument(
        "--top", type=int, default=10, help="Number of top words to show"
    )
    parser.add_argument(
        "--min-len", type=int, default=1, help="Minimum word length filter"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (text or json)",
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