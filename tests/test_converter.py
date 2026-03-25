"""Tests for the converter dispatch logic."""

import pytest

from case_cli.converter import convert, STYLE_MAP, STYLE_NAMES


class TestConvert:
    """Tests for the convert function."""

    def test_full_name_snake(self):
        assert convert("hello world", "snake") == "hello_world"

    def test_full_name_pascal(self):
        assert convert("hello world", "pascal") == "HelloWorld"

    def test_full_name_camel(self):
        assert convert("hello world", "camel") == "helloWorld"

    def test_full_name_kebab(self):
        assert convert("hello world", "kebab") == "hello-world"

    def test_full_name_upper(self):
        assert convert("hello world", "upper") == "HELLO WORLD"

    def test_full_name_lower(self):
        assert convert("Hello World", "lower") == "hello world"

    def test_full_name_constant(self):
        assert convert("hello world", "constant") == "HELLO_WORLD"

    def test_full_name_dot(self):
        assert convert("hello world", "dot") == "hello.world"

    def test_full_name_ada(self):
        assert convert("hello world", "ada") == "Hello_World"

    def test_full_name_cobol(self):
        assert convert("hello world", "cobol") == "HELLO-WORLD"

    def test_full_name_train(self):
        assert convert("hello world", "train") == "Hello-World"

    def test_full_name_header(self):
        assert convert("hello world", "header") == "Hello-World"

    def test_full_name_sentence(self):
        assert convert("hello world", "sentence") == "Hello world"

    def test_alias_s(self):
        assert convert("hello world", "s") == "hello_world"

    def test_alias_k(self):
        assert convert("hello world", "k") == "hello-world"

    def test_alias_c(self):
        assert convert("hello world", "c") == "helloWorld"

    def test_alias_p(self):
        assert convert("hello world", "p") == "HelloWorld"

    def test_alias_u(self):
        assert convert("hello world", "u") == "HELLO WORLD"

    def test_alias_l(self):
        assert convert("Hello World", "l") == "hello world"

    def test_alias_h(self):
        assert convert("hello world", "h") == "Hello-World"

    def test_alias_t(self):
        assert convert("hello world", "t") == "Hello World"

    def test_case_insensitive_style(self):
        assert convert("hello world", "SNAKE") == "hello_world"
        assert convert("hello world", "Snake") == "hello_world"

    def test_unknown_style_raises_error(self):
        with pytest.raises(ValueError, match="Unknown case style"):
            convert("hello world", "nonexistent")

    def test_empty_input(self):
        assert convert("", "snake") == ""

    def test_preserves_trailing_special_chars(self):
        assert convert("hello world!", "pascal") == "HelloWorld!"

    def test_all_style_names_in_map(self):
        for name in STYLE_NAMES:
            assert name in STYLE_MAP, "Style '{}' missing from STYLE_MAP".format(name)
