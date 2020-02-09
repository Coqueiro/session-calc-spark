FROM coqueirotree/spark-submit2.4.4-hadoop2.7-aws-support:latest

LABEL maintainer="github.com/Coqueiro"

# ARG arg1

ENV SPARK_MASTER_NAME spark-master
ENV SPARK_MASTER_PORT 7077
ENV SPARK_APPLICATION_PYTHON_LOCATION /app/entrypoint.py
# ENV SPARK_APPLICATION_ARGS "--arg1 ${arg1}"

COPY session-calc.sh /

# Copy the requirements.txt first, for separate dependency resolving and downloading
COPY requirements.txt /app/
RUN cd /app \
      && pip3 install -r requirements.txt

# Copy the source code
COPY . /app

CMD ["/bin/bash", "/session-calc.sh"]