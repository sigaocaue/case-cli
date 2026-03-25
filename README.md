# case-cli

[![Python](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-brightgreen)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/case-cli)](https://pypi.org/project/case-cli)

case-cli é uma ferramenta de linha de comando para normalizar cadeias de texto entre estilos diferentes (snake_case, camelCase, PascalCase e outros). Ela resolve o problema de ajustar nomes padronizados em scripts, documentação ou convenções de API sem depender de editores ou procedimentos manuais.

## Funcionalidades

- Converte entradas de texto para 15 estilos de escrita, incluindo upper, lower, snake, kebab, constant, ada, cobol, train, header, sentence e dot.
- Aceita nomes completos e apelidos (por exemplo, `snake` ou `s`), além de ser case-insensitive ao identificar o estilo desejado.
- Permite persistir um estilo padrão via `case-cli set <style>`, armazenando a preferência em `~/.case-cli/config.json` ou no caminho configurado por `CASE_CLI_CONFIG_PATH`.
- Sobrepõe o estilo padrão com a variável `CASE_CLI_DEFAULT_CASE` e ajusta o nível de log com `CASE_CLI_LOG_LEVEL`.
- Arquitetura modular separa o parser CLI, mapeamento de estilos e lógica de cada estilo em módulos dedicados, facilitando a manutenção.

## Demonstração

```bash
case-cli "hello world" --case=snake
# hello_world

case-cli set pascal
# Default case style set to 'pascal'.

case-cli "another example"
# AnotherExample
```

> Ao executar sem `--case`, o utilitário consulta primeiro `CASE_CLI_DEFAULT_CASE` e depois o arquivo de configuração em `~/.case-cli/config.json` para decidir o estilo.

## Tecnologias e bibliotecas

- Python 3.6+ (padrão do pacote, conforme `pyproject.toml`)
- `argparse` e `logging` (CLI e registros)
- `json` e `os` (persistência da configuração padrão)
- `pytest` e `pytest-cov` para validação automatizada (dependências de desenvolvimento)

## Organização do projeto

- `case_cli/` – pacote principal com o ponto de entrada (`main.py`), dispatcher (`converter.py`), persistência (`config.py`) e implementações por estilo (`styles/`).
- `tests/` – suíte de testes unitários para converter estilos e manipular configuração.
- `pyproject.toml` – configuração de empacotamento e metadados do projeto.

## Variáveis de ambiente

| Variável | Valor padrão | Descrição |
| --- | --- | --- |
| `CASE_CLI_CONFIG_PATH` | `~/.case-cli/config.json` | Caminho do arquivo que guarda o estilo padrão. |
| `CASE_CLI_DEFAULT_CASE` | _(não definido)_ | Sobrepõe temporariamente o estilo padrão ao converter. |
| `CASE_CLI_LOG_LEVEL` | `WARNING` | Ajusta o nível de log (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |

## Licença

Distribuído sob a licença MIT. Consulte o arquivo [`LICENSE`](LICENSE) para a redação completa e os direitos de uso.
