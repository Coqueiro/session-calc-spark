ARG SPARK_VERSION
ARG HADOOP_VERSION
ARG SUBMIT_VERSION

FROM coqueirotree/spark-submit${SPARK_VERSION}-hadoop${HADOOP_VERSION}-aws-support:${SUBMIT_VERSION}

LABEL maintainer="github.com/Coqueiro"

ENV SPARK_MASTER_NAME spark-master
ENV SPARK_MASTER_PORT 7077
ENV SPARK_APPLICATION_PYTHON_LOCATION /app/entrypoint.py

# Copy the requirements.txt first, for separate dependency resolving and downloading
COPY requirements.txt /app/
RUN cd /app \
      && pip3 install -r requirements.txt

# Copy the source code
COPY . /app

CMD ["/bin/bash", "/submit.sh"]