FROM python:3.11-slim

WORKDIR /app

# Copiar ficheiros do projeto
COPY . /app

# Variáveis de ambiente padrão
ENV PORT=8000
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Executar servidor
CMD ["python3", "servidor_simulacao.py"]
