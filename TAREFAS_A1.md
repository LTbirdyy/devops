# Checklist — Avaliação A1 (09/09/2026)

Projeto: Encurtador de URLs
Stack: FastAPI + PostgreSQL + Redis

## ✅ Já feito (Backend)

- [x] Endpoints da API (`/shorten`, `/{short_code}`, `/health`)
- [x] Persistência com SQLAlchemy (modelo `URL`)
- [x] Cache com Redis (`app/cache.py`)
- [x] Suíte de testes automatizados (unitários + integração) — 9 testes
- [x] Pipeline de CI configurado (`.github/workflows/ci.yml`)
- [x] Front-end inicial funcional (`app/static/index.html`)

---

## 🎨 Front-end — [alex]

- [ ] Revisar/ajustar a interface em `app/static/index.html` (cores, textos, copy)
- [ ] Testar responsividade (celular, tablet, desktop)
- [ ] Melhorar mensagens de erro exibidas ao usuário (ex: link inválido)
- [ ] Testar o fluxo completo manualmente: encurtar → copiar → abrir o link curto → confirmar redirecionamento
- [ ] (Opcional) Adicionar mais testes automatizados do front em `tests/test_frontend.py`(Essa ultima o daniel pode fazer se quiser)
---

## 📄 Documentação / DevOps — [daniel]

### Git e branches
- [ ] Confirmar proteção da branch `main` ativada no GitHub:
  - [ ] Require pull request before merging
  - [ ] Require status checks to pass before merging (workflow `build-and-test`)
  - [ ] Block force pushes
- [ ] Documentar a estratégia de ramificação usada pelo grupo (ex: Trunk-Based: `main` protegida + `feature/*`)
- [ ] Garantir que os commits do grupo sigam um padrão (ex: `feat:`, `fix:`, `test:`, `docs:`, `chore:`)

### CI
- [ ] Confirmar que o pipeline roda com sucesso na aba **Actions** do GitHub a cada push/PR
- [ ] Tirar print do pipeline rodando (evidência pra entrega)

### Organização da entrega
- [ ] Revisar o `README.md` — garantir que alguém de fora do grupo consiga clonar e rodar só seguindo as instruções
- [ ] Documentar a divisão de papéis do grupo (Dev / Qualidade / Infra), conforme pedido no item 4 do PDF da disciplina
- [ ] Preparar um resumo curto do que foi entregue, caso o professor peça explicação do processo

---

## 👥 Todo o grupo

- [ ] Cada pessoa abrir pelo menos 1 Pull Request para a `main` (mesmo que pequeno) para validar que a proteção de branch está funcionando na prática
- [ ] Revisar o PR de alguém do grupo antes do merge (simula o fluxo real de revisão de código)

---

## Entregas esperadas pelo PDF da disciplina (conferência final)

- [x] Repositório Git estruturado (ramificação + proteção de branch + commits padronizados)
- [x] Código-fonte com testes automatizados
- [x] Pipeline de CI operacional (build + testes a cada PR/push)
