# Encurtador de URLs

Projeto da disciplina de Integração DevOps — Ciência da Computação 2026_2.

Encurta URLs longas em códigos curtos, com cache em Redis para acelerar os
redirecionamentos mais acessados e persistência em PostgreSQL.

## Stack

- **Backend:** FastAPI (Python)
- **Banco de dados:** PostgreSQL (via SQLAlchemy)
- **Cache:** Redis
- **Front-end:** HTML/CSS/JS simples, servido pelo próprio FastAPI
- **Testes:** pytest

## Estratégia de ramificação e workflow do time

Usamos **Trunk-Based Development**:

- A branch `main` é a única branch de longa duração e representa sempre o
  estado estável do projeto.
- Toda alteração é feita em uma branch curta a partir da `main`, nomeada por
  tipo de tarefa: `feature/nome-da-tarefa`, `fix/nome-do-bug`,
  `docs/nome-do-ajuste` ou `feature/nome-do-responsavel`.
- A `main` é protegida: não é possível dar push direto nela. Toda mudança
  entra via **Pull Request**, que exige:
  - Aprovação de pelo menos 1 outro membro do grupo
  - O pipeline de CI (`build-and-test`) passando
- Mensagens de commit seguem o padrão [Conventional Commits](https://www.conventionalcommits.org/)
  (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).

### Papéis do grupo

| Membro           | Papel | Responsabilidades |
|------------------|---|---|
| Gabriel Fernando | Desenvolvedor | Backend: API, persistência, cache, testes automatizados |
| Alex Xiwang      | Qualidade | Front-end e validação do fluxo de uso ponta a ponta |
| Daniel godoi     | Operações/Infraestrutura | Git, CI/CD, documentação técnica |

## Estrutura do projeto

```
url-shortener/
├── app/
│   ├── main.py            # rotas da API e do front-end
│   ├── models.py          # tabela de URLs (SQLAlchemy)
│   ├── schemas.py         # validação de entrada/saída (Pydantic)
│   ├── shortener.py       # geração do código curto
│   ├── cache.py           # integração com Redis
│   ├── config.py          # configurações via variáveis de ambiente
│   └── static/index.html  # front-end
├── tests/                 # testes automatizados (pytest)
└── .github/workflows/     # pipeline de CI
```

## Pré-requisitos

- Python 3.11 ou superior instalado ([python.org/downloads](https://www.python.org/downloads/))
- Git instalado

Você **não precisa** ter PostgreSQL nem Redis instalados na máquina para rodar
localmente em modo de desenvolvimento — veja a seção "Sobre o modo de
desenvolvimento" abaixo.

## Como rodar localmente

### 1. Clone o repositório e entre na pasta

```bash
git clone <url-do-seu-repositorio>
cd url-shortener
```

### 2. Crie e ative o ambiente virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```
> Se aparecer um erro dizendo que a execução de scripts está desabilitada, rode uma vez:
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, depois tente ativar de novo.

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Se estiver usando o PyCharm, ele pode já ter criado e ativado uma pasta
`.venv` automaticamente — nesse caso não é necessário criar outra, é só
seguir para o próximo passo com esse ambiente já ativo.

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Rode a aplicação

```bash
$env:TESTING='true'
uvicorn app.main:app --reload
```

Acesse **http://localhost:8000** no navegador — a página do encurtador
deve aparecer.

## Sobre o modo de desenvolvimento

Sem configurar as variáveis `DATABASE_URL` e `REDIS_URL`, a aplicação usa
um arquivo SQLite local (`test.db`) no lugar do Postgres, só para facilitar
testes manuais na sua máquina. Isso é temporário: a partir da A2, o projeto
vai subir com Postgres e Redis de verdade via `docker-compose`.

### ⚠️ Erro `redis.exceptions.ConnectionError` ao rodar o `uvicorn`

Se você **não tem o Redis instalado/rodando** na sua máquina, a aplicação vai
quebrar com um erro parecido com:

```
redis.exceptions.ConnectionError: Error 10061 connecting to localhost:6379.
```

Isso é esperado — a aplicação está tentando se conectar num Redis de verdade
que ainda não existe na sua máquina. Enquanto não tivermos o `docker-compose`
pronto (A2), suba a aplicação assim, usando um Redis "falso" em memória
(o mesmo usado pelos testes automatizados):

**Windows (PowerShell):**
```powershell
$env:TESTING='true'
uvicorn app.main:app --reload
```

**Mac/Linux:**
```bash
TESTING=true uvicorn app.main:app --reload
```

> **Atenção:** essa variável só vale para o terminal em que foi definida. Se
> você fechar o terminal ou abrir uma janela nova, precisa setar de novo antes
> de rodar o `uvicorn` — senão a aplicação volta a tentar conectar no Redis
> real e dá o mesmo erro.


## Como rodar os testes automatizados

**Windows (PowerShell):**
```powershell
$env:TESTING='true'; python -m pytest -v
```

**Mac/Linux:**
```bash
TESTING=true python -m pytest -v
```
(Usar `python -m pytest` em vez de só `pytest` evita erros de importação do
módulo `app` em algumas configurações.)

Os testes usam SQLite e um Redis falso (`fakeredis`) internamente, então
rodam rápido e não exigem nenhum serviço externo rodando.

## Endpoints da API

| Método | Rota            | Descrição                                                |
|--------|-----------------|-----------------------------------------------------------|
| GET    | `/`             | Página do front-end                                        |
| POST   | `/shorten`      | Recebe `{"url": "https://..."}` e retorna o código curto  |
| GET    | `/{short_code}` | Redireciona para a URL original                            |
| GET    | `/health`       | Healthcheck (usado pelo CI/monitoramento)                  |

## Problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| `'python' não foi encontrado` | Python não instalado ou não está no PATH | Reinstale o Python marcando "Add Python to PATH", e desative os aliases da Microsoft Store em Configurações → Aplicativos → Aliases de execução de aplicativo |
| `ModuleNotFoundError: No module named 'fastapi'` (ou outro pacote) | Ambiente virtual não ativado, ou dependências não instaladas nele | Confirme que `(venv)` ou `(.venv)` aparece no prompt, depois rode `pip install -r requirements.txt` de novo |
| Erro ao instalar `psycopg2-binary` (`pg_config not found`) | A versão do pacote não tem wheel pronto para a sua versão do Python | Use uma versão mais recente do pacote (`psycopg2-binary==2.9.10` ou superior) |
| `ModuleNotFoundError: No module named 'app'` ao rodar `pytest` | O pytest não está enxergando a pasta raiz do projeto | Rode `python -m pytest -v` em vez de apenas `pytest -v` |
| `PermissionError` ao final dos testes no Windows (arquivo `test_ci.db` em uso) | O Windows trava o arquivo SQLite até a conexão ser fechada | Já corrigido no `tests/conftest.py` com `engine.dispose()` antes de apagar o arquivo |

## Roadmap do projeto (A1 → A3)

- [x] A1: Repositório estruturado, código com testes automatizados, pipeline de CI
- [ ] A2: Dockerfile, docker-compose, pipeline de CD, gestão de segredos, versionamento/rollback
- [ ] A3: Pipeline DevSecOps (SAST + scan de vulnerabilidades), observabilidade (Grafana), documentação técnica completa, live demo
