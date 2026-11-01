# Versionamento semântico e rollback

## Versionamento

Usamos [versionamento semântico](https://semver.org/lang/pt-BR/) (`MAJOR.MINOR.PATCH`):

| Mudança | Exemplo | Quando usar |
|---|---|---|
| PATCH | `1.0.0` → `1.0.1` | Correção de bug sem mudar o comportamento |
| MINOR | `1.0.1` → `1.1.0` | Funcionalidade nova compatível |
| MAJOR | `1.1.0` → `2.0.0` | Mudança que quebra compatibilidade |

Cada versão é uma **tag Git** (`v1.0.0`). Ao criar a tag, o pipeline `cd.yml`
publica no GitHub Container Registry as tags de imagem `1.0.0`, `1.0` e
`latest`, e cria uma Release no GitHub com as notas geradas automaticamente.

Um número de versão nunca é reutilizado: se a `1.0.1` sair com defeito, a
correção vira a `1.0.2`.

### Como lançar uma versão

Depois que o Pull Request foi aprovado e mergeado, com a `main` atualizada e o
CI verde:

```bash
git checkout main
git pull
git tag v1.0.0
git push origin v1.0.0
```

Acompanhe em **Actions → cd**: build, push da imagem, deploy em homologação e
smoke test.

## Fluxo de rollback (simulado)

Cenário: a `v1.0.1` foi publicada, mas apresenta falha em homologação.

1. O job `deploy-homologacao` falha no smoke test e imprime os logs dos
   containers, indicando que é preciso fazer rollback.
2. Em **Actions → cd → Run workflow**, informe a última versão estável
   (ex: `1.0.0`) no campo `version`.
3. O pipeline pula o build (a imagem `1.0.0` já existe no registry), faz o pull
   da imagem antiga, sobe o ambiente e roda o mesmo smoke test.
4. Com o smoke test verde, o ambiente está de volta à versão estável.
5. Corrija o problema em uma branch, abra o PR e lance a `v1.0.2`.

> Por que funciona: as imagens são imutáveis e versionadas. Voltar de versão é
> só apontar o `APP_IMAGE` do compose para uma tag anterior. O deploy sempre usa
> uma versão explícita, nunca `latest`, então o rollback não depende dessa tag.

## Como executar a simulação

Pré-requisitos: PR da A2 mergeado na `main`, Environment `homologacao` com o
secret `POSTGRES_PASSWORD` criado e *Workflow permissions* em *Read and write*
(Settings → Actions → General).

### Passo 1: lançar a versão estável

```bash
git checkout main
git pull
git tag v1.0.0
git push origin v1.0.0
```

Resultado esperado: `cd` verde, imagem `1.0.0` em Packages e Release `v1.0.0`.

### Passo 2: provocar a falha proposital

A falha é criada **fora da `main`**. Se a gente tentasse mergear um `/health`
quebrado, o teste `test_health_check` reprovaria o PR e a proteção de branch
bloquearia o merge, o que é o comportamento correto. Como o `cd.yml` dispara
por tag, é possível versionar o commit com defeito sem mergeá-lo:

```bash
git checkout main
git pull
git checkout -b test/falha-proposital
```

Em `app/main.py`, troque o corpo do `/health` por:

```python
@app.get("/health")
def health_check():
    raise HTTPException(status_code=500, detail="falha proposital para simular rollback")
```

```bash
git add app/main.py
git commit -m "test: injeta falha proposital no /health para simular rollback"
git tag v1.0.1
git push origin v1.0.1
```

Não abra Pull Request e não mergeie esse commit. Resultado esperado: o build
publica a imagem `1.0.1`, mas o `deploy-homologacao` fica **vermelho** (a
aplicação não responde ao `/health`).

### Passo 3: executar o rollback

**Actions → cd → Run workflow** (branch `main`), campo `version` = `1.0.0`.
Resultado esperado: o build é pulado, o deploy da `1.0.0` fica **verde** e o
resumo da execução mostra a versão implantada.

### Passo 4: voltar ao estado normal

```bash
git checkout main
git branch -D test/falha-proposital
```

A tag e a Release `v1.0.1` permanecem como evidência. A próxima versão real
será a `v1.0.2` (ou `v1.1.0`).

## Evidências da simulação (preencher antes da entrega)

| Etapa | Print / link da execução |
|---|---|
| Release `v1.0.0` publicada com sucesso (`cd` verde) | |
| Imagem `1.0.0` visível no GHCR (Packages) | |
| Release `v1.0.0` na página de Releases | |
| Release `v1.0.1` com falha proposital (deploy vermelho) | |
| Rollback executado manualmente para `1.0.0` (verde) | |

## Registro do incidente simulado

| Campo | Preenchimento |
|---|---|
| Versão com defeito | `1.0.1` |
| Como foi detectado | Smoke test do deploy (a aplicação não respondeu ao `/health`) |
| Impacto | Homologação indisponível com a `1.0.1`; nenhum usuário real afetado |
| Ação tomada | Rollback para a `1.0.0` via workflow `cd` (`workflow_dispatch`) |
| Início da falha | |
| Fim do rollback | |
| Tempo de recuperação | |
| Causa raiz | Falha injetada de propósito no endpoint `/health` |
| Ação preventiva | Smoke test obrigatório antes de considerar o deploy concluído; versões nunca reutilizadas |
