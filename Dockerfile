# ---------- Estágio 1: instala as dependências ----------
FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
# --prefix isola tudo em /install, para copiarmos só isso para a imagem final
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Estágio 2: imagem final, enxuta ----------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Usuário sem privilégios: boa prática de segurança (não rodar como root)
RUN useradd --create-home --uid 1000 appuser

WORKDIR /app
COPY --from=builder /install /usr/local
COPY app ./app

USER appuser
EXPOSE 8000

# Docker marca o container como "healthy" quando o /health responde
HEALTHCHECK --interval=15s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=2)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
