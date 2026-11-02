# Checklist — Avaliação A2 (04/11/2026)

## Código já pronto neste pacote
- [x] `Dockerfile` (multi-stage, usuário não-root, healthcheck)
- [x] `docker-compose.yml` (app + Postgres + Redis, com volume e healthchecks)
- [x] `.env.example` e `.dockerignore`
- [x] `ci.yml` valida o build do Dockerfile
- [x] `cd.yml` publica no GHCR, cria release e faz deploy simulado
- [x] `docs/ROLLBACK.md` com o fluxo de versionamento e rollback

## Backend — Gabriel
- [ ] Rodar `docker compose up --build` na máquina e testar no navegador
- [ ] Abrir PR com estes arquivos (branch `feature/docker-cd`)

## DevOps / Documentação
- [ ] Criar o Environment `homologacao` (Settings → Environments)
- [ ] Criar o secret `POSTGRES_PASSWORD` nesse environment
- [ ] Conferir em Settings → Actions → General que "Workflow permissions" está em *Read and write*
- [ ] Lançar `v1.0.0` e conferir imagem em Packages e Release criada
- [ ] Simular falha (`v1.0.1`) e executar o rollback, tirando prints
- [ ] Preencher a tabela de evidências em `docs/ROLLBACK.md`

## Qualidade / Front
- [ ] Validar o app subindo via compose (encurtar, copiar, abrir o link curto)
- [ ] Conferir que o front continua funcionando na imagem Docker
