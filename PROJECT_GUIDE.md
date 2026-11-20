# Guia para Desenvolvedor

Este projeto é um utilitário de linha de comando em Python chamado `case-cli` que converte textos entre diversos estilos de case (snake, camel, Pascal, kebab etc.). O foco abaixo é explicar o propósito de cada arquivo/diretório e mostrar como executar o projeto em um ambiente de desenvolvimento local.

## Estrutura do repositório

- `case_cli/` – pacote principal com o código em inglês. Contém:
  - `__main__.py` / `main.py` – ponto de entrada para o console script `case-cli`, usa `argparse` para interpretar comandos e direcionar chamadas ao conversor.
  - `converter.py` – mapeia nomes e aliases (`snake`, `s`, `kebab`, `k`, etc.) para módulos de estilos e expõe a função `convert(text, case_style)` usada pela CLI.
  - `config.py` – gerencia persistência do estilo padrão em `~/.case-cli/config.json`, respeitando `CASE_CLI_CONFIG_PATH`, `CASE_CLI_DEFAULT_CASE` e `CASE_CLI_LOG_LEVEL`.
  - `styles/` – submódulos como `snake.py`, `camel.py`, `pascal.py`, `upper.py` etc., cada um implementando o comportamento necessário para seu estilo.
- `tests/` – suíte automatizada (executada com `pytest`) que valida `case_cli.converter` e `case_cli.config`. Contém `test_converter.py`, `test_config.py` e pacotes auxiliares.
- `pyproject.toml` – define metadados do projeto (bundle, versão, dependências de runtime e dev) e registra o entry point `case-cli = "case_cli.main:main"`.
- `setup.cfg` – pode conter configurações extras para lint/testes (não foi explorado mas fica junto).
- `case_cli.egg-info/` – artefato gerado pelo empacotamento; ignore para o desenvolvimento diário.
- `LICENSE` – texto completo da licença MIT usada pelo projeto.
- `README.md` e `SETUP.md` – documentos com visão geral e instruções de instalação/execução (podem ser atualizados conforme necessário).

## Como preparar o ambiente

Rode os comandos abaixo:

Usando pip:
```bash
python -m pip install --upgrade pip setuptools wheel
pip install -e .[dev]
```

Usando uv:
```bash
python -m pip install --upgrade pip setuptools wheel
pip install -e .[dev]
```

Isso garante que o comando `case-cli` fique disponível enquanto você desenvolve, e, que as bibliotecas de teste (`pytest`, `pytest-cov`) fiquem acessíveis.

## Executando o projeto localmente

- **Como módulo Python:**

```bash
python -m case_cli.main "texto de exemplo" --case=snake
```

- **Como comando instalado (após `pip install -e .`):**

Usando pip:
```bash
pip install -e .
```
Depois rode:
```bash
case-cli "hello world" --case=pascal
case-cli "nome exemplo" --case=kebab
case-cli set snake
case-cli "outro texto"  # usa estilo padrão salvo
```

---
Usando uv:
```bash
uv pip install -e .
```
Depois disso, o comando case-cli fica disponível no .venv:
```bash
# Ativando o venv (se ainda não estiver ativo)
source .venv/bin/activate
case-cli "hello world" --case=snake

# Ou sem ativar o venv, usando uv run
uv run case-cli "hello world" --case=snake
```
O uv run é o mais prático — ele resolve o ambiente automaticamente sem precisar ativar o venv manualmente.


O comando `case-cli set <style>` grava o estilo em `~/.case-cli/config.json` ou no caminho configurado por `CASE_CLI_CONFIG_PATH`, tornando-o o padrão para chamadas futuras sem `--case`.

## Variáveis de ambiente úteis

- `CASE_CLI_CONFIG_PATH` – altera o caminho do arquivo de configuração que guarda o default case.
- `CASE_CLI_DEFAULT_CASE` – força um estilo temporário sem editar arquivos.
- `CASE_CLI_LOG_LEVEL` – define verbosidade (`DEBUG`, `INFO`, `WARNING`, `ERROR`).

Exemplo de uso antes de executar o CLI:

```bash
export CASE_CLI_DEFAULT_CASE=sentence
export CASE_CLI_LOG_LEVEL=DEBUG
case-cli "variável importante"
```

## Testes

1. Execute **toda a suíte** com:

```bash
pytest
```

2. Para cobertura:

```bash
pytest --cov=case_cli
```

O `tests/test_converter.py` garante que todos os estilos definidos em `case_cli.converter.STYLE_NAMES` estejam mapeados e produzam as saídas corretas. `tests/test_config.py` foca na leitura/escrita do arquivo de configuração com fixtures do `pytest`.

## Executando como ferramenta externa no terminal

Depois de instalar (`pip install -e .`), o binário `case-cli` pode ser chamado exatamente da mesma forma que um utilitário independente:

```bash
case-cli "texto exemplo" --case=snake
case-cli "texto exemplo" --case=pascal
case-cli set kebab
case-cli "texto"  # usa o default salvo
```

Ele aceita flags curtas e longas (`-c`, `--case`, `-v`, `--version`, `-h`, `--help`) e trata aliases como `s`, `k`, `c`, `p`. Em caso de estilo desconhecido, apresenta erro informando os estilos disponíveis.

## Dicas extras

- Mantenha o logging configurado se precisar diagnosticar falhas (`CASE_CLI_LOG_LEVEL=DEBUG`).
- Novos estilos podem ser adicionados ao diretório `case_cli/styles/`; basta implementar `convert(tokens)` e registrar o novo módulo em `converter.STYLE_MAP`.
