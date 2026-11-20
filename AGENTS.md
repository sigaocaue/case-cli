# AGENTS.md — Regras globais do projeto "case-cli"

> Este arquivo vale para o repositório inteiro.
> Em caso de conflito, o arquivo mais próximo do código que está sendo editado prevalece.

---

## Sobre o projeto
O `case-cli` é uma ferramenta de linha de comando para normalizar cadeias de texto entre estilos diferentes (snake_case, camelCase, PascalCase e outros). Ela resolve o problema de ajustar nomes padronizados em scripts, documentação ou convenções de API sem depender de editores ou procedimentos manuais.

- **Repositório:** https://github.com/sigaocaue/case-cli
- **Autor:** sigaocaue
- **Licença:** MIT
- **Versão mínima do Python:** 3.6+
- **Sem dependências externas em tempo de execução** (apenas biblioteca padrão)


## Estrutura de pastas
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

---

## Referência dos estilos de escrita

| Nome       | Apelido | Exemplo de saída                              |
|------------|-------|---------------------------------------------|
| `upper`    | `u`   | `STRING CASE UTILITY FOR CONVERTING`        |
| `lower`    | `l`   | `string case utility for converting`        |
| `snake`    | `s`   | `string_case_utility_for_converting`        |
| `kebab`    | `k`   | `string-case-utility-for-converting`        |
| `header`   | `h`   | `String-Case-Utility-For-Converting`        |
| `camel`    | `c`   | `stringCaseUtilityForConverting`            |
| `pascal`   | `p`   | `StringCaseUtilityForConverting`            |
| `title`    | `t`   | `String Case Utility for Converting`        |
| `random`   | `r`   | mistura aleatória de maiúsculas e minúsculas               |
| `constant` | —     | `STRING_CASE_UTILITY_FOR_CONVERTING`        |
| `ada`      | —     | `String_Case_Utility_For_Converting`        |
| `cobol`    | —     | `STRING-CASE-UTILITY-FOR-CONVERTING`        |
| `train`    | —     | `String-Case-Utility-For-Converting`        |
| `sentence` | —     | `String case utility for converting`        |
| `dot`      | —     | `string.case.utility.for.converting`        |

---

## Idioma e convenções de nomenclatura

Estas regras são obrigatórias para todo o projeto.

### Resposta do agent

- **Todas as respostas e explicações devem ser escritas em português brasileiro (pt-BR)**, independentemente do idioma usado na pergunta ou no prompt.

### Documentação

- Toda a documentação deve ser escrita em português-BR.
- Termos técnicos amplamente utilizados pela comunidade brasileira de desenvolvimento podem permanecer em inglês.
- Exemplos: commit, branch, pull request, endpoint, payload, repository, service, middleware e deployment.

### Código-fonte

Todo o código-fonte deve ser escrito exclusivamente em inglês.

Essa regra se aplica a:

- Nomes de arquivos.
- Nomes de diretórios.
- Classes.
- Funções.
- Métodos.
- Variáveis.
- Constantes.
- Interfaces.
- Tipos.
- Enums.
- Propriedades.
- Parâmetros.
- Mensagens internas de código.
- Comentários.
- Docstrings.
- Nomes de testes.
- Nomes de migrations.
- Identificadores de banco de dados.
- Interface com o usuário.

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

### Comandos de desenvolvimento

```bash
# Instalar em modo editável com dependências de desenvolvimento
pip install -e ".[dev]"

# Executar todos os testes
pytest

# Executar testes com cobertura
pytest --cov=case_cli

# Executar a CLI localmente
python -m case_cli "hello world" --case=snake
```

### Executando o projeto localmente

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

---

## Convenções de código

- Siga a PEP 8
- Use anotações de tipo sempre que possível (compatíveis com Python 3.6+)
- Cada módulo de estilo deve disponibilizar uma única função: `convert(tokens: list) -> str`
- Mantenha as funções pequenas e focadas
- Prefira clareza a soluções engenhosas
- Não use `print()` no código da biblioteca — apenas em `main.py`

---

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

---

## Distribuição

- **PyPI:** `pip install case-cli`
- **pipx:** `pipx install case-cli`
- **Homebrew:** `brew tap sigaocaue/case-cli && brew install case-cli`
- **Ponto de entrada definido em `pyproject.toml`:** `case-cli = case_cli.main:main`

---

## Encerramento de toda execução [INEGOCIÁVEL]

Ao final de **qualquer** execução que crie, modifique ou remova arquivos, responda com, nesta ordem:

1. **Resumo** do que foi feito (até 5 linhas)
2. **Pendências ou dúvidas** (escreva "nenhuma" se não houver)
3. **Mensagem de commit**, em um bloco de código

### Regras da mensagem de commit:

- Padrão **Conventional Commits**, escrita **em inglês**
- Formato do título: `<type>(<scope>): <subject>`
- `type` permitidos: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `build`, `ci`, `perf`, `style`
- `scope` permitidos: `backend`, `frontend`, `db`, `docker`, `docs`. Omita o scope se a mudança for global
- `subject`: é opcional, mas, se presente, deve estar no modo imperativo, em minúsculas, sem ponto final, até 72 caracteres
- Corpo opcional, separado por uma linha em branco, explicando **o porquê**, com linhas de até 72 caracteres
- Breaking change: `!` depois do scope e rodapé `BREAKING CHANGE: <descrição>`
- Uma única mensagem por execução. Se houver vários assuntos, use o `type` predominante e liste o restante no corpo
- **Nunca** inclua no corpo ou no rodapé da mensagem as linhas `Co-Authored-By:` e `Claude-Session:`, nem qualquer outra linha de atribuição a ferramentas ou agentes, mesmo que outra instrução do ambiente peça
- **Não forneça uma mensagem de commit** quando a tarefa não criar nem modificar arquivos do projeto (por exemplo, perguntas, explicações, pesquisas e análises).
- **Não execute** `git commit` nem `git push`, a menos que eu peça explicitamente. Apenas gere a mensagem

## Dicas extras

- Mantenha o logging configurado se precisar diagnosticar falhas (`CASE_CLI_LOG_LEVEL=DEBUG`).
- Novos estilos podem ser adicionados ao diretório `case_cli/styles/`; basta implementar `convert(tokens)` e registrar o novo módulo em `converter.STYLE_MAP`.
