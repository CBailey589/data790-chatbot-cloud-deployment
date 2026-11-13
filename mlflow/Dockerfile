FROM python:3.12-slim
WORKDIR /mlflow
RUN pip install --no-cache-dir mlflow
EXPOSE 5000
CMD ["mlflow", "server", \
     "--host", "0.0.0.0", \
     "--port", "5000", \
     "--workers", "1", \
     "--backend-store-uri", "sqlite:////tmp/mlflow.db", \
     "--artifacts-destination", "/tmp/mlartifacts"]