"""Tests for all 15 case style converters."""

import pytest

from case_cli.styles.base import tokenize
from case_cli.styles import (
    upper, lower, snake, kebab, header, camel, pascal,
    title, random_case, constant, ada, cobol, train, sentence, dot
)


class TestTokenize:
    """Tests for the tokenizer utility."""

    def test_simple_spaces(self):
        assert tokenize("hello world") == ["hello", "world"]

    def test_camel_case_input(self):
        assert tokenize("helloWorld") == ["hello", "world"]

    def test_pascal_case_input(self):
        assert tokenize("HelloWorld") == ["hello", "world"]

    def test_snake_case_input(self):
        assert tokenize("hello_world") == ["hello", "world"]

    def test_kebab_case_input(self):
        assert tokenize("hello-world") == ["hello", "world"]

    def test_dot_case_input(self):
        assert tokenize("hello.world") == ["hello", "world"]

    def test_mixed_delimiters(self):
        assert tokenize("helloWorld_foo-bar") == ["hello", "world", "foo", "bar"]

    def test_trailing_special_characters(self):
        assert tokenize("hello world!") == ["hello", "world!"]

    def test_trailing_multiple_special(self):
        assert tokenize("hello world?!") == ["hello", "world?!"]

    def test_empty_string(self):
        assert tokenize("") == []

    def test_consecutive_uppercase(self):
        assert tokenize("XMLParser") == ["xml", "parser"]

    def test_single_word(self):
        assert tokenize("hello") == ["hello"]


class TestUpperCase:
    def test_simple(self):
        tokens = tokenize("hello world")
        assert upper.convert(tokens) == "HELLO WORLD"

    def test_with_special_chars(self):
        tokens = tokenize("hello world!")
        assert upper.convert(tokens) == "HELLO WORLD!"

    def test_already_upper(self):
        tokens = tokenize("HELLO WORLD")
        assert upper.convert(tokens) == "HELLO WORLD"


class TestLowerCase:
    def test_simple(self):
        tokens = tokenize("Hello World")
        assert lower.convert(tokens) == "hello world"

    def test_with_special_chars(self):
        tokens = tokenize("Hello World!")
        assert lower.convert(tokens) == "hello world!"

    def test_already_lower(self):
        tokens = tokenize("hello world")
        assert lower.convert(tokens) == "hello world"


class TestSnakeCase:
    def test_simple(self):
        tokens = tokenize("hello world")
        assert snake.convert(tokens) == "hello_world"

    def test_with_special_chars(self):
        tokens = tokenize("hello world!")
        assert snake.convert(tokens) == "hello_world!"

    def test_already_snake(self):
        tokens = tokenize("hello_world")
        assert snake.convert(tokens) == "hello_world"

    def test_from_camel(self):
        tokens = tokenize("helloWorld")
        assert snake.convert(tokens) == "hello_world"


class TestKebabCase:
    def test_simple(self):
        tokens = tokenize("hello world")
        assert kebab.convert(tokens) == "hello-world"

    def test_with_special_chars(self):
        tokens = tokenize("hello world!")
        assert kebab.convert(tokens) == "hello-world!"

    def test_already_kebab(self):
        tokens = tokenize("hello-world")
        assert kebab.convert(tokens) == "hello-world"


class TestHeaderCase:
    def test_simple(self):
        tokens = tokenize("hello world")
        assert header.convert(tokens) == "Hello-World"

    def test_with_special_chars(self):
        tokens = tokenize("hello world!")
        assert header.convert(tokens) == "Hello-World!"

    def test_already_header(self):
        tokens = tokenize("Hello-World")
        assert header.convert(tokens) == "Hello-World"


class TestCamelCase:
    def test_simple(self):
        tokens = tokenize("hello world")
        assert camel.convert(tokens) == "helloWorld"

    def test_with_special_chars(self):
        tokens = tokenize("hello world!")
        assert camel.convert(tokens) == "helloWorld!"

    def test_already_camel(self):
        tokens = tokenize("helloWorld")
        assert camel.convert(tokens) == "helloWorld"

    def test_single_word(self):
        tokens = tokenize("hello")
        assert camel.convert(tokens) == "hello"


class TestPascalCase:
    def test_simple(self):
        tokens = tokenize("hello world")
        assert pascal.convert(tokens) == "HelloWorld"

    def test_with_special_chars(self):
        tokens = tokenize("hello world!")
        assert pascal.convert(tokens) == "HelloWorld!"

    def test_already_pascal(self):
        tokens = tokenize("HelloWorld")
        assert pascal.convert(tokens) == "HelloWorld"


class TestTitleCase:
    def test_simple(self):
        tokens = tokenize("hello world")
        assert title.convert(tokens) == "Hello World"

    def test_with_special_chars(self):
        tokens = tokenize("hello world!")
        assert title.convert(tokens) == "Hello World!"

    def test_minor_words(self):
        tokens = tokenize("string case utility for converting")
        assert title.convert(tokens) == "String Case Utility for Converting"

    def test_first_word_minor(self):
        tokens = tokenize("the quick brown fox")
        assert title.convert(tokens) == "The Quick Brown Fox"


class TestRandomCase:
    def test_simple_produces_output(self):
        tokens = tokenize("hello world")
        result = random_case.convert(tokens)
        assert result.lower() == "hello world"

    def test_with_special_chars(self):
        tokens = tokenize("hello world!")
        result = random_case.convert(tokens)
        assert result.lower() == "hello world!"

    def test_preserves_length(self):
        tokens = tokenize("hello world")
        result = random_case.convert(tokens)
        assert len(result) == len("hello world")


class TestConstantCase:
    def test_simple(self):
        tokens = tokenize("hello world")
        assert constant.convert(tokens) == "HELLO_WORLD"

    def test_with_special_chars(self):
        tokens = tokenize("hello world!")
        assert constant.convert(tokens) == "HELLO_WORLD!"

    def test_already_constant(self):
        tokens = tokenize("HELLO_WORLD")
        assert constant.convert(tokens) == "HELLO_WORLD"


class TestAdaCase:
    def test_simple(self):
        tokens = tokenize("hello world")
        assert ada.convert(tokens) == "Hello_World"

    def test_with_special_chars(self):
        tokens = tokenize("hello world!")
        assert ada.convert(tokens) == "Hello_World!"

    def test_already_ada(self):
        tokens = tokenize("Hello_World")
        assert ada.convert(tokens) == "Hello_World"


class TestCobolCase:
    def test_simple(self):
        tokens = tokenize("hello world")
        assert cobol.convert(tokens) == "HELLO-WORLD"

    def test_with_special_chars(self):
        tokens = tokenize("hello world!")
        assert cobol.convert(tokens) == "HELLO-WORLD!"

    def test_already_cobol(self):
        tokens = tokenize("HELLO-WORLD")
        assert cobol.convert(tokens) == "HELLO-WORLD"


class TestTrainCase:
    def test_simple(self):
        tokens = tokenize("hello world")
        assert train.convert(tokens) == "Hello-World"

    def test_with_special_chars(self):
        tokens = tokenize("hello world!")
        assert train.convert(tokens) == "Hello-World!"

    def test_already_train(self):
        tokens = tokenize("Hello-World")
        assert train.convert(tokens) == "Hello-World"


class TestSentenceCase:
    def test_simple(self):
        tokens = tokenize("hello world")
        assert sentence.convert(tokens) == "Hello world"

    def test_with_special_chars(self):
        tokens = tokenize("hello world!")
        assert sentence.convert(tokens) == "Hello world!"

    def test_single_word(self):
        tokens = tokenize("hello")
        assert sentence.convert(tokens) == "Hello"

    def test_already_sentence(self):
        tokens = tokenize("Hello world")
        assert sentence.convert(tokens) == "Hello world"


class TestDotCase:
    def test_simple(self):
        tokens = tokenize("hello world")
        assert dot.convert(tokens) == "hello.world"

    def test_with_special_chars(self):
        tokens = tokenize("hello world!")
        assert dot.convert(tokens) == "hello.world!"

    def test_already_dot(self):
        tokens = tokenize("hello.world")
        assert dot.convert(tokens) == "hello.world"
