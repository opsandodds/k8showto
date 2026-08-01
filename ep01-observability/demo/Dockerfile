FROM python:3.12-slim
# setuptools<81 keeps pkg_resources (OTel needs it); install the instrumentations
# directly instead of the flaky `opentelemetry-bootstrap`.
RUN pip install --no-cache-dir --root-user-action=ignore \
    "setuptools<81" flask==3.0.3 requests==2.32.3 \
    opentelemetry-distro==0.48b0 opentelemetry-exporter-otlp==1.27.0 \
    opentelemetry-instrumentation-flask==0.48b0 \
    opentelemetry-instrumentation-requests==0.48b0 \
    opentelemetry-instrumentation-logging==0.48b0
COPY app.py /app/app.py
WORKDIR /app
ENV OTEL_TRACES_EXPORTER=otlp OTEL_METRICS_EXPORTER=none OTEL_LOGS_EXPORTER=none \
    FLASK_APP=app.py
CMD ["opentelemetry-instrument", "flask", "run", "--host=0.0.0.0", "--port=8080"]
