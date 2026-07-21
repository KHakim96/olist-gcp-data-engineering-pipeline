FROM apache/airflow:2.11.0-python3.11

COPY requirements.txt .

RUN pip install --no-cache-dir \
    apache-airflow==${AIRFLOW_VERSION} \
    -r requirements.txt