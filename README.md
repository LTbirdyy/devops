# Encurtador de URLs

Projeto da disciplina de Integração DevOps — Ciência da Computação 2026_2.

**Stack:** FastAPI + PostgreSQL (persistência) + Redis (cache)

## Como rodar localmente (sem Docker, para desenvolvimento)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

A aplicação sobe em `http://localhost:8000`. Sem configurar `DATABASE_URL`/`REDIS_URL`,
ela usa SQLite local como fallback só para facilitar testes manuais — em produção
(via docker-compose, na A2) ela usará Postgres e Redis de verdade.

## Como rodar os testes

```bash
TESTING=true pytest -v
```

## Endpoints

- `POST /shorten` — recebe `{"url": "https://..."}` e retorna o código curto
- `GET /{short_code}` — redireciona para a URL original
- `GET /health` — healthcheck

## Roadmap do projeto (A1 → A3)

- [x] A1: CI + testes automatizados
- [ ] A2: Dockerfile, docker-compose, pipeline de CD, secrets, rollback
- [ ] A3: SAST/scan de vulnerabilidades, observabilidade (Grafana), documentação final
