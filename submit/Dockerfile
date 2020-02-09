FROM coqueirotree/spark-base2.4.4-hadoop2.7-aws-support

LABEL maintainer="github.com/Coqueiro"

ENV SPARK_MASTER_NAME spark-master
ENV SPARK_MASTER_PORT 7077
ENV SPARK_APPLICATION_JAR_LOCATION /app/application.jar
ENV SPARK_APPLICATION_PYTHON_LOCATION /app/app.py
ENV SPARK_APPLICATION_MAIN_CLASS my.main.Application
ENV SPARK_APPLICATION_ARGS ""

COPY submit.sh /

CMD ["/bin/bash", "/submit.sh"]
