## Pré-requisitos

- Python 3.6 ou superior (o pacote declara `requires-python = ">=3.6"`).
- `pip` disponível para instalar dependências.
- (Opcional) `virtualenv` ou outro gerenciador de ambientes para isolamento.

## Instalação

```bash
python -m pip install --upgrade pip setuptools wheel
pip install -e .[dev]
```

> `pip install -e .[dev]` instala o pacote em modo editável e traz as dependências listadas em `[project.optional-dependencies]` (`pytest`, `pytest-cov`).

## Variáveis de ambiente

- `CASE_CLI_CONFIG_PATH` – caminho do arquivo que guarda o estilo padrão (o padrão é `~/.case-cli/config.json`).
- `CASE_CLI_DEFAULT_CASE` – define temporariamente o estilo de conversão sem alterar o arquivo de configuração.
- `CASE_CLI_LOG_LEVEL` – controla o nível de log (`DEBUG`, `INFO`, `WARNING`, `ERROR`); padrão `WARNING`.

> Não existe `.env.example`; exporte as variáveis diretamente antes de executar o binário ou use um gerenciador de ambiente que carregue variáveis.

## Execução

```bash
case-cli "texto de exemplo" --case=snake
case-cli --case=pascal "texto de exemplo"
case-cli set kebab
case-cli "outro texto"
```

- Use `case-cli set <style>` para persistir o estilo padrão (salvo em `CASE_CLI_CONFIG_PATH` ou no arquivo padrão).
- Sem `--case`, o CLI usa primeiro `CASE_CLI_DEFAULT_CASE` e depois o arquivo de configuração para decidir o estilo.

## Testes

```bash
pytest
```

- `pytest` executa os testes em `tests/`, cobrindo o dispatcher de estilos e a persistência de configuração.

## Observações adicionais

- O pacote expõe o script `case-cli` conforme o entry point definido em `pyproject.toml` (`case_cli.main:main`).
- Cada estilo de case vive em `case_cli/styles/`, facilitando a extensão com formatos adicionais.
- A configuração padrão é gravada em JSON em `~/.case-cli/config.json`, mas pode ser redirecionada pelo `CASE_CLI_CONFIG_PATH`.
