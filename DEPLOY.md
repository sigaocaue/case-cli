# Deploy do case-cli

O código e os workflows ficam em [sigaocaue/case-cli](https://github.com/sigaocaue/case-cli). A distribuição Python fica no [PyPI](https://pypi.org/project/case-cli/), e a fórmula usada pelo Homebrew fica no repositório [sigaocaue/homebrew-case-cli](https://github.com/sigaocaue/homebrew-case-cli), em `Formula/case-cli.rb`.

## Pré-requisitos

- Tenha acesso para integrar mudanças ao repositório principal e para conferir as configurações no GitHub e no PyPI.
- No macOS, tenha o Homebrew instalado para validar a fórmula e a instalação.

## Conferir a configuração antes de publicar

### Permissões da main e das tags no GitHub

1. Abra **Settings → Rulesets** no repositório `sigaocaue/case-cli`. Na barra lateral, **Rulesets** fica logo acima de **Branches**. Expanda o menu e abra a lista de regras.
2. Abra as regras ativas que se aplicam à branch `main` ou às tags que começam com `v`, como `v0.1.2`. Uma regra pode usar um padrão, como `v*`, para abranger várias tags.
3. Confira se alguma regra exige pull request para gravar na `main` ou restringe a atualização da branch ou a criação de tags. Se houver uma restrição, verifique se a automação tem uma exceção que permita essas operações. Confira também **Settings → Branches**, onde ficam as regras clássicas de proteção da branch.
4. Em **Settings → Actions → General**, confirme que o GitHub Actions está habilitado. A permissão padrão pode ficar em leitura. O job `version` já pede `contents: write` para gravar o commit e a tag, e as regras do repositório ainda se aplicam.

### Token do tap do Homebrew

1. No repositório `sigaocaue/case-cli`, abra **Settings → Secrets and variables → Actions**. Em **Repository secrets**, procure `HOMEBREW_TAP_TOKEN`. Um *secret* guarda a credencial que o workflow usa.
2. Nas [configurações de tokens do GitHub](https://github.com/settings/personal-access-tokens), confira se o token está ativo. Para um token com permissões granulares, o repositório selecionado deve incluir `sigaocaue/homebrew-case-cli` e a permissão **Contents** deve estar em **Read and write**.
3. No repositório do tap, confira se as regras da branch padrão permitem que a conta dona do token grave a fórmula. Se o token tiver expirado ou sido substituído, atualize o valor do secret no repositório `case-cli`.

### Trusted Publishing no PyPI

Trusted Publishing autoriza o GitHub Actions a publicar no PyPI sem guardar uma senha ou um token do PyPI no repositório.

1. No GitHub, abra **Settings → Environments → pypi** no repositório `case-cli`. Confira se o ambiente permite publicar a partir da `main`. Se houver aprovação obrigatória, o job de publicação vai aguardar essa aprovação.
2. No PyPI, entre com uma conta mantenedora e abra **Seus projetos → case-cli → Gerenciar → Publicação**. Em **Adicionar um novo publicador**, selecione **GitHub** e preencha os campos abaixo.

   | Campo | Valor |
   | --- | --- |
   | Proprietário | `sigaocaue` |
   | Nome do repositório | `case-cli` |
   | Nome do fluxo de trabalho | `ci.yml` |
   | Environment name | `pypi` |

3. Clique em **Adicionar** e confirme que `ci.yml` aparece na lista de publicadores. Se ainda houver uma entrada para `release.yml`, você pode removê-la depois que a primeira publicação por `ci.yml` funcionar.

Na primeira publicação, acompanhe os jobs `version`, `publish-pypi` e `update-homebrew` para confirmar a gravação do commit e da tag, a publicação no PyPI e a atualização da fórmula, respectivamente.

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
