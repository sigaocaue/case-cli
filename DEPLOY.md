# Deploy do case-cli

O código e os workflows ficam em [sigaocaue/case-cli](https://github.com/sigaocaue/case-cli). A distribuição Python fica no [PyPI](https://pypi.org/project/case-cli/), e a fórmula usada pelo Homebrew fica no repositório [sigaocaue/homebrew-case-cli](https://github.com/sigaocaue/homebrew-case-cli), em `Formula/case-cli.rb`.

## Pré-requisitos

- Tenha acesso para integrar mudanças ao repositório principal. As regras da branch `main` e das tags `v*` precisam permitir que o GitHub Actions grave o commit de versão e a tag com `GITHUB_TOKEN`.
- No PyPI, o projeto `case-cli` precisa autorizar o [Trusted Publisher do GitHub Actions](https://docs.pypi.org/trusted-publishers/adding-a-publisher/) com proprietário `sigaocaue`, repositório `case-cli`, arquivo `ci.yml` e ambiente `pypi`. O job usa OIDC.
- No repositório principal, o secret `HOMEBREW_TAP_TOKEN` precisa permitir leitura e escrita do conteúdo de `sigaocaue/homebrew-case-cli`. Para um token de acesso pessoal com permissões granulares, use [Contents: Read and write](https://docs.github.com/en/rest/repos/contents#create-or-update-file-contents) no repositório do tap.
- No macOS, tenha o Homebrew instalado para validar a fórmula e a instalação.

## Publicar a partir da main

No repositório principal, um merge na `main` ou um `git push origin main` aciona o [workflow CI](.github/workflows/ci.yml). A CI também roda os testes nos pull requests, antes do merge.

1. A CI testa o commit recebido em todas as versões de Python da matriz (3.8 a 3.13). Se algum teste falhar, a publicação fica bloqueada.
2. Depois dos testes, a CI instala as dependências de desenvolvimento e executa o `bump-my-version`. A ferramenta sincroniza `pyproject.toml`, `case_cli/__init__.py` e `uv.lock`, cria o commit de versão e gera a tag `v<versão>`. O commit e a tag são enviados juntos ao GitHub.
3. A CI gera o wheel e o pacote fonte a partir da tag e os publica no PyPI via Trusted Publishing.
4. Depois que o pacote fonte estiver disponível, a CI usa a URL e o SHA-256 informados pelo PyPI para atualizar a fórmula na branch padrão do tap.

Acompanhe as etapas em [Actions → CI](https://github.com/sigaocaue/case-cli/actions/workflows/ci.yml). O push do bot usa `GITHUB_TOKEN` e [não inicia outra execução da CI](https://docs.github.com/en/actions/concepts/security/github_token#when-github_token-triggers-workflow-runs). A tag identifica a versão no Git. O workflow não cria uma entrada na aba **Releases** do GitHub.

### Escolher patch, minor ou major

| Incremento | Como solicitar | Exemplo partindo de `0.1.1` |
| --- | --- | --- |
| `patch` | Integre ou envie as mudanças normalmente. É o padrão. | `0.1.2` |
| `minor` | Inclua `[release:minor]` no título do PR ou na mensagem de um commit enviado para `main`. | `0.2.0` |
| `major` | Inclua `[release:major]` no título do PR ou na mensagem de um commit enviado para `main`. | `1.0.0` |

Para um PR, inclua o marcador no título **antes do merge**. Exemplos de título:

```text
feat: add a conversion style [release:minor]
feat!: change the default conversion behavior [release:major]
```

Para push direto, coloque o marcador na mensagem do commit. Use apenas o incremento desejado:

```bash
git commit -m "feat: add a conversion style [release:minor]"
git push origin main
```

Para uma versão `major`, use `[release:major]` na mensagem. Se os dois marcadores aparecerem na mesma execução, `major` tem precedência. O tipo do Conventional Commit, como `feat`, por si só mantém o incremento padrão `patch`.

### Recuperar uma publicação com falha

- Se a `main` avançar antes que a CI grave o commit de versão, a execução do commit antigo é interrompida para preservar o histórico da branch. A CI da atualização mais recente pode publicar as mudanças acumuladas. Se o incremento maior ainda for necessário, inclua o marcador em uma nova atualização da `main`.
- Se o commit e a tag já foram criados, use **Re-run failed jobs** na execução original após corrigir a falha. Uma reexecução completa da mesma execução também reaproveita a tag existente. Fazer um novo push inicia outro incremento.
- Se a etapa de versão falhar por regras de branch ou tag, confira se a automação pode gravar na `main` e criar tags `v*`. Se a publicação no PyPI falhar por autenticação, confira o Trusted Publisher e o ambiente `pypi`.

## Atualizar o tap manualmente

Use este procedimento se a versão já saiu no PyPI, mas o job `update-homebrew` falhou ou a fórmula remota ficou desatualizada. Se o problema no job já foi corrigido, também é possível reexecutar apenas o job com falha no run original. Se optar pelo ajuste manual, use a versão publicada mais recente para evitar que a fórmula volte a apontar para uma versão anterior.

1. Abra a página da versão em `https://pypi.org/project/case-cli/<versão>/#files`. Em **Source Distribution**, copie a URL do arquivo `.tar.gz` e o SHA-256 correspondente. Use os dados do pacote fonte, pois é o arquivo instalado pela fórmula.
2. No clone de `homebrew-case-cli` (diretório irmão deste projeto), sincronize a branch padrão com o remoto. Atualize `url` e `sha256` em `Formula/case-cli.rb`. Preserve as demais instruções da fórmula. O arquivo homônimo neste repositório é uma referência e sua edição não atualiza o tap.
3. Revise o diff, faça o commit e envie a atualização ao repositório do tap conforme as permissões da branch padrão.

## Verificar a publicação

1. Confirme no [PyPI](https://pypi.org/project/case-cli/#history) que a versão aparece e tem um pacote fonte e um wheel.
2. Confira no [repositório do tap](https://github.com/sigaocaue/homebrew-case-cli) se a fórmula aponta para o pacote fonte publicado e tem o SHA-256 correspondente.
3. Em um terminal no macOS, atualize o índice, instale ou atualize o pacote e rode o teste da fórmula:

```bash
brew tap sigaocaue/case-cli
brew update
# Primeira instalação:
brew install sigaocaue/case-cli/case-cli
# Se já estiver instalado, use no lugar da instalação:
brew upgrade sigaocaue/case-cli/case-cli

brew test sigaocaue/case-cli/case-cli
case-cli --version
case-cli "hello world" --case=snake
```

Confirme que `case-cli --version` exibe a versão publicada e que a conversão retorna `hello_world`.
