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

## Instalação e configuração

Consulte o [SETUP.md](SETUP.md) para instruções de instalação, configuração do ambiente, execução e testes.

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

## Flags da linha de comando

| Forma curta | Forma longa | Argumento | O que faz e para que serve |
| --- | --- | --- | --- |
| `-h` | `--help` | — | Exibe as instruções de uso e as opções disponíveis. |
| `-v` | `--version` | — | Exibe a versão instalada do `case-cli` e encerra. Serve para identificar qual versão está em uso. |
| `-c` | `--case` | `STYLE` | Converte o texto de entrada para o estilo indicado. Use para escolher o formato de saída nesta execução; os estilos aceitos são os listados na ajuda da CLI. Se omitida, a ferramenta procura um padrão definido por `CASE_CLI_DEFAULT_CASE` ou `case-cli set <style>`. |
| — | `--completion` | `SHELL` | Gera as instruções para que o terminal ajude a completar opções e estilos ao pressionar Tab. Informe `bash` ou `zsh`, conforme o terminal usado. Veja como ativar abaixo. |

Para converter um texto, escreva-o no comando, como em `case-cli "hello world" -c snake`. Para salvar um estilo como padrão, use `case-cli set snake`; assim, nas próximas conversões, você pode omitir a opção `-c`.

### Completar comandos com Tab

Para ativar a sugestão de opções e estilos na janela atual do terminal, execute o comando correspondente ao seu shell:

```bash
# Bash
eval "$(case-cli --completion bash)"

# Zsh
eval "$(case-cli --completion zsh)"
```

Depois, por exemplo, digite `case-cli "hello world" --case sna` e pressione Tab para completar `snake`. Para ativar esse recurso em novas sessões, acrescente o comando correspondente ao arquivo `~/.bashrc` (Bash) ou `~/.zshrc` (Zsh). Executar apenas `case-cli --completion bash` ou `case-cli --completion zsh` exibe as instruções no terminal; o comando com `eval` acima as ativa.

## Estilos aceitos

Use qualquer valor da coluna **Estilo** ou seu apelido, quando disponível, no lugar de `STYLE`. A tabela mostra o resultado para o texto `hello world`:

| Estilo | Apelido | Resultado |
| --- | --- | --- |
| `upper` | `u` | `HELLO WORLD` |
| `lower` | `l` | `hello world` |
| `snake` | `s` | `hello_world` |
| `kebab` | `k` | `hello-world` |
| `header` | `h` | `Hello-World` |
| `camel` | `c` | `helloWorld` |
| `pascal` | `p` | `HelloWorld` |
| `title` | `t` | `Hello World` |
| `random` | `r` | Letras maiúsculas e minúsculas escolhidas aleatoriamente, como `hELlo WoRLd` |
| `constant` | — | `HELLO_WORLD` |
| `ada` | — | `Hello_World` |
| `cobol` | — | `HELLO-WORLD` |
| `train` | — | `Hello-World` |
| `sentence` | — | `Hello world` |
| `dot` | — | `hello.world` |

Os nomes e apelidos aceitam letras maiúsculas ou minúsculas. Em `title`, algumas palavras curtas em inglês, como `and` e `the`, ficam em minúsculas, exceto quando são a primeira palavra.

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
