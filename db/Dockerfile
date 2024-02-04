FROM python:3.10-slim

WORKDIR /db

RUN pip install chromadb

COPY . .

CMD ["chroma","run","--path", "./chromadb" , "--host", "0.0.0.0", "--port", "8000"]

