FROM coqueirotree/spark-base2.4.4-hadoop2.7-aws-support

LABEL maintainer="github.com/Coqueiro"

COPY master.sh /

ENV SPARK_MASTER_PORT 7077
ENV SPARK_MASTER_WEBUI_PORT 8080
ENV SPARK_MASTER_LOG /spark/logs

EXPOSE 8080 7077 6066

CMD ["/bin/bash", "/master.sh"]
