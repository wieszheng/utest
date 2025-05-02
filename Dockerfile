# --------- requirements ---------
FROM python:3.12-slim AS builder
WORKDIR /tmp
COPY ./requirements.txt .

RUN python -m venv /tmp/venv \
    && /tmp/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /tmp/venv/bin/pip install --no-cache-dir -r requirements.txt


# --------- final image build ---------
FROM python:3.12-slim
WORKDIR /app

COPY --from=builder /tmp/venv /tmp/venv

RUN ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata wget vim && \
    rm -rf /var/lib/apt/lists/*

COPY . .
RUN /tmp/venv/bin/pip show uvicorn
# -------- replace with comment to run with gunicorn --------
EXPOSE 8000
CMD ["/tmp/venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
#CMD ["/tmp/venv/bin/supervisord", "-c", "/app/supervisord.conf"]
