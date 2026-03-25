# case-cli

![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/github/license/sigaocaue/case-cli)
![PyPI](https://img.shields.io/pypi/v/case-cli)

A command-line tool for converting strings between different case styles (snake_case, camelCase, PascalCase, and more).

## Installation

### pip

```bash
pip install case-cli
```

### pipx

```bash
pipx install case-cli
```

### Homebrew

```bash
brew tap sigaocaue/case-cli
brew install case-cli
```

### asdf

There is no official asdf plugin yet. To create one, follow the [asdf plugin creation guide](https://asdf-vm.com/plugins/create.html). The plugin should download the appropriate release from PyPI or GitHub and install it via `pip`.

### apt / deb

You can package `case-cli` as a `.deb` using [fpm](https://fpm.readthedocs.io/):

```bash
pip install case-cli
fpm -s python -t deb case-cli
sudo dpkg -i python-case-cli_*.deb
```

Alternatively, use [stdeb](https://github.com/astraw/stdeb):

```bash
pip install stdeb
python setup.py --command-packages=stdeb.command bdist_deb
sudo dpkg -i deb_dist/python3-case-cli_*.deb
```

### Windows

```bash
pip install case-cli
```

Support for `winget` is planned for a future release.

## Usage

### Convert with explicit case style

```bash
case-cli "hello world" --case=snake
# hello_world

case-cli --case=pascal "hello world"
# HelloWorld

case-cli --case=pascal "hello world!"
# HelloWorld!

case-cli -c=snake "hello world"
# hello_world

# Using alias
case-cli -c=s "hello world"
# hello_world
```

### Set a default case style

```bash
case-cli set kebab
# Default case style set to 'kebab'.
```

### Convert using the default case style

```bash
case-cli "Hello World"
# hello-world
```

### Flags

| Long flag    | Short flag | Description                      |
|--------------|------------|----------------------------------|
| `--case`     | `-c`       | Target case style                |
| `--version`  | `-v`       | Show version                     |
| `--help`     | `-h`       | Show help                        |

## Available Case Styles

| Name       | Alias | Example Output                              |
|------------|-------|---------------------------------------------|
| `upper`    | `u`   | `STRING CASE UTILITY FOR CONVERTING`        |
| `lower`    | `l`   | `string case utility for converting`        |
| `snake`    | `s`   | `string_case_utility_for_converting`        |
| `kebab`    | `k`   | `string-case-utility-for-converting`        |
| `header`   | `h`   | `String-Case-Utility-For-Converting`        |
| `camel`    | `c`   | `stringCaseUtilityForConverting`            |
| `pascal`   | `p`   | `StringCaseUtilityForConverting`            |
| `title`    | `t`   | `String Case Utility for Converting`        |
| `random`   | `r`   | random mix of upper/lowercase               |
| `constant` | --    | `STRING_CASE_UTILITY_FOR_CONVERTING`        |
| `ada`      | --    | `String_Case_Utility_For_Converting`        |
| `cobol`    | --    | `STRING-CASE-UTILITY-FOR-CONVERTING`        |
| `train`    | --    | `String-Case-Utility-For-Converting`        |
| `sentence` | --    | `String case utility for converting`        |
| `dot`      | --    | `string.case.utility.for.converting`        |

Both full names and aliases are accepted with the `--case` / `-c` flag.

## Default Case Style

You can set a default case style so you don't need to pass `--case` every time:

```bash
case-cli set snake
```

The default is saved to `~/.case-cli/config.json`.

## Environment Variables

| Variable               | Default                     | Description                                  |
|------------------------|-----------------------------|----------------------------------------------|
| `CASE_CLI_CONFIG_PATH` | `~/.case-cli/config.json`   | Custom path for the config file              |
| `CASE_CLI_LOG_LEVEL`   | `WARNING`                   | Log level: DEBUG, INFO, WARNING, ERROR       |
| `CASE_CLI_DEFAULT_CASE`| _(none)_                    | Overrides config file default case style     |

## Development

```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run tests with coverage
pytest --cov=case_cli
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
