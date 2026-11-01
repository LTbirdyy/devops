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

### Como lançar uma versão

Com a `main` atualizada e o CI verde:

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
> só apontar o `APP_IMAGE` do compose para uma tag anterior.

## Evidências da simulação (preencher antes da entrega)

| Etapa | Print / link da execução |
|---|---|
| Release `v1.0.0` publicada com sucesso | |
| Imagem `1.0.0` visível no GHCR (Packages) | |
| Release `v1.0.1` com falha proposital no smoke test | |
| Rollback executado manualmente para `1.0.0` (verde) | |

### Como provocar a falha proposital

Em uma branch, quebre algo simples e visível ao smoke test (por exemplo, faça o
`/health` retornar erro 500), abra PR, faça merge e crie a tag `v1.0.1`. O
deploy vai falhar e você poderá demonstrar o rollback.
