ARG SPARK_VERSION
ARG HADOOP_VERSION
ARG BASE_VERSION

FROM coqueirotree/spark-base${SPARK_VERSION}-hadoop${HADOOP_VERSION}-aws-support:${BASE_VERSION}

LABEL maintainer="github.com/Coqueiro"

COPY worker.sh /

ENV SPARK_WORKER_WEBUI_PORT 8081
ENV SPARK_WORKER_LOG /spark/logs
ENV SPARK_MASTER "spark://spark-master:7077"

EXPOSE 8081

CMD ["/bin/bash", "/worker.sh"]
