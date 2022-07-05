# Builder
FROM python:3.8-slim as venv
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get -y install --no-install-recommends wget gzip && \
    python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY app/ttml/load-fine-tuned.sh .
RUN ./load-fine-tuned.sh
COPY requirements.txt app/ttml/load-tokenizer.py .
RUN pip install --no-cache-dir -r requirements.txt && \
    python load-tokenizer.py
 
# ELG app
FROM python:3.8-slim
RUN apt-get update && apt-get -y install --no-install-recommends tini && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    addgroup --gid 1001 "elg" && \
    adduser --disabled-password --gecos "ELG User,,," --home /elg --ingroup elg --uid 1001 elg && \
    chmod +x /usr/bin/tini
COPY --chown=elg:elg --from=venv /opt/venv /opt/venv
COPY --from=venv /app/models /elg/ttml/models

USER elg:elg
WORKDIR /elg
COPY --chown=elg:elg docker-entrypoint.sh app/app.py app/utils.py /elg
COPY --chown=elg:elg app/ttml/predict.py /elg/ttml

ENV PATH="/opt/venv/bin:$PATH"

ENV WORKERS=1
ENV TIMEOUT=300
ENV WORKER_CLASS=sync
ENV LOG_LEVEL=info
ENV PYTHON_PATH="/opt/venv/bin"

RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
