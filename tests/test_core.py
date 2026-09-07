"""Tests for text analyzer core functionality."""

from pathlib import Path
import pytest

from text_analyzer.core import analyze_text_file, format_output


def test_missing_file(tmp_path: Path) -> None:
    """Test handling of missing file."""
    fake_file = tmp_path / "non_existent.txt"
    with pytest.raises(FileNotFoundError):
        analyze_text_file(fake_file)


def test_empty_file(tmp_path: Path) -> None:
    """Test analysis of an empty file."""
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("", encoding="utf-8")

    lines, words, chars, counter = analyze_text_file(empty_file)
    assert lines == 0
    assert words == 0
    assert chars == 0
    assert len(counter) == 0


@pytest.mark.parametrize(
    ("content", "min_len", "expected_words"),
    [
        ("apple banana apple", 1, 3),
        ("a bb ccc dddd", 3, 2),
        ("hello, world! hello.", 1, 3),
    ],
)
def test_word_counting(
    tmp_path: Path, content: str, min_len: int, expected_words: int
) -> None:
    """Parameterized test for word counting and filtering."""
    test_file = tmp_path / "sample.txt"
    test_file.write_text(content, encoding="utf-8")

    _, words, _, _ = analyze_text_file(test_file, min_len=min_len)
    assert words == expected_words


def test_invalid_encoding(tmp_path: Path) -> None:
    """Test invalid encoding handling."""
    binary_file = tmp_path / "binary.bin"
    binary_file.write_bytes(bytes([0x80, 0x81, 0x82]))

    with pytest.raises(UnicodeDecodeError):
        analyze_text_file(binary_file, encoding="utf-8")


def test_format_output_text() -> None:
    """Test output formatting in text mode."""
    res = format_output(
        line_count=2,
        word_count=4,
        char_count=20,
        top_words=[("hello", 2), ("world", 1)],
        output_format="text",
    )
    assert "Lines: 2" in res
    assert "Words: 4" in res
    assert "hello: 2" in res


def test_format_output_json() -> None:
    """Test output formatting in JSON mode."""
    res = format_output(
        line_count=1,
        word_count=2,
        char_count=10,
        top_words=[("test", 2)],
        output_format="json",
    )
    assert '"lines": 1' in res
    assert '"word": "test"' in res