#------------ stage 1: Build dependecies ------------
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt 

# --------------- Stage 2 Production image ------------
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app","--host" ,"0.0.0.0" ,"--port" ,"8000"]