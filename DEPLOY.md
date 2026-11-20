# Deploy do case-cli

O código e os workflows ficam em [sigaocaue/case-cli](https://github.com/sigaocaue/case-cli). A distribuição Python fica no [PyPI](https://pypi.org/project/case-cli/), e a fórmula usada pelo Homebrew fica no repositório [sigaocaue/homebrew-case-cli](https://github.com/sigaocaue/homebrew-case-cli), em `Formula/case-cli.rb`.

## Pré-requisitos

- Tenha Git, `uv` e acesso para enviar mudanças ao repositório principal. Se a branch `main` exigir pull request, siga as regras de merge do repositório.
- No PyPI, o projeto `case-cli` precisa autorizar o [Trusted Publisher do GitHub Actions](https://docs.pypi.org/trusted-publishers/adding-a-publisher/) com proprietário `sigaocaue`, repositório `case-cli`, arquivo `ci.yml` e ambiente `pypi`. O job usa OIDC.
- No repositório principal, o secret `HOMEBREW_TAP_TOKEN` precisa permitir leitura e escrita do conteúdo de `sigaocaue/homebrew-case-cli`. Para um token de acesso pessoal com permissões granulares, use [Contents: Read and write](https://docs.github.com/en/rest/repos/contents#create-or-update-file-contents) no repositório do tap.
- No macOS, tenha o Homebrew instalado para validar a fórmula e a instalação.

## Gerar e publicar uma versão

Escolha o incremento conforme a mudança: `patch` para correções compatíveis, `minor` para novos recursos compatíveis ou `major` para mudanças incompatíveis.

Com as mudanças da versão já integradas, a árvore limpa e a `main` local atualizada, execute na raiz do `case-cli`:

```bash
git switch main
git pull --ff-only origin main
uv sync --extra dev
uv run pytest --cov=case_cli
```

Gere a versão com o incremento escolhido. No exemplo, `patch` deve ser trocado por `minor` ou `major` se for o caso:

```bash
uv run bump-my-version bump patch
uv run bump-my-version show current_version
git show --stat HEAD
git tag --points-at HEAD
```

O `bump-my-version` atualiza a versão em `pyproject.toml` e em `case_cli/__init__.py` e cria o commit e a tag `v<versão>`. Se o push direto para `main` for permitido, envie o commit e a tag usando sua conta:

```bash
git push origin main --follow-tags
```

Se o repositório exigir pull request, crie uma branch a partir do commit de versão e envie-a para revisão. O merge em `main` aciona a CI. Se o merge reescrever o commit, como no squash, confira o commit efetivo em `main` e aponte a tag local da versão para ele antes de publicar a tag.

Em [Actions → CI](https://github.com/sigaocaue/case-cli/actions/workflows/ci.yml), acompanhe a execução do push para `main`. O [workflow de CI](.github/workflows/ci.yml) roda os testes, consulta a versão no PyPI e, quando recebe HTTP 404, gera o wheel e o pacote fonte com `uv build` e publica os dois no PyPI. Depois, busca o SHA-256 do pacote fonte e atualiza a fórmula na branch padrão do tap. A tag identifica o commit da versão. Os workflows atuais não criam uma GitHub Release.

### Limitação do workflow Release

O [workflow Release](.github/workflows/release.yml) pode ser iniciado manualmente em **Actions → Release → Run workflow**, selecionando `main` e o tipo de incremento. Ele cria o commit e a tag e envia ambos com `GITHUB_TOKEN`. [O GitHub não dispara workflows de push nesse caso](https://docs.github.com/en/actions/concepts/security/github_token#when-github_token-triggers-workflow-runs), por isso esse workflow sozinho não publica no PyPI nem atualiza o tap.

Se o workflow Release já enviou a versão para `main` e ela ainda não está no PyPI, sincronize sua cópia e envie, com sua conta, um novo commit baseado na `main` atual, seguindo as regras da branch. O push resultante aciona a CI para a versão que já está no código. Não incremente a versão novamente só para disparar a CI.

## Atualizar o tap manualmente

Use este procedimento se a versão já saiu no PyPI, mas o job `update-homebrew` falhou ou a fórmula remota ficou desatualizada. Se o problema no job já foi corrigido, também é possível reexecutar apenas o job com falha no run original. Um novo run da CI pula a publicação e a atualização do tap quando a versão já existe no PyPI.

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
