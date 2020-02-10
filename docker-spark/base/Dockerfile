FROM alpine:3.10

LABEL maintainer="github.com/Coqueiro"

ARG SPARK_VERSION
ARG HADOOP_VERSION

ENV ENABLE_INIT_DAEMON true
ENV INIT_DAEMON_BASE_URI http://identifier/init-daemon
ENV INIT_DAEMON_STEP spark_master_init

ENV SPARK_HOME=/spark
ENV HADOOP_HOME=/hadoop
ENV SPARK_DIST_CLASSPATH=/hadoop/etc/hadoop:/hadoop/share/hadoop/common/lib/*:/hadoop/share/hadoop/common/*:/hadoop/share/hadoop/hdfs:/hadoop/share/hadoop/hdfs/lib/*:/hadoop/share/hadoop/hdfs/*:/hadoop/share/hadoop/yarn/lib/*:/hadoop/share/hadoop/yarn/*:/hadoop/share/hadoop/mapreduce/lib/*:/hadoop/share/hadoop/mapreduce/*:/hadoop/contrib/capacity-scheduler/*.jar

COPY wait-for-step.sh /
COPY execute-step.sh /
COPY finish-step.sh /

RUN apk add --no-cache curl bash openjdk8-jre python3 py-pip nss libc6-compat \
      && ln -s /lib64/ld-linux-x86-64.so.2 /lib/ld-linux-x86-64.so.2 \
      && chmod +x *.sh \
      && wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-without-hadoop.tgz \
      && tar -xvzf spark-${SPARK_VERSION}-bin-without-hadoop.tgz \
      && mv spark-${SPARK_VERSION}-bin-without-hadoop spark \
      && rm spark-${SPARK_VERSION}-bin-without-hadoop.tgz

RUN wget -q https://archive.apache.org/dist/hadoop/core/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
      && tar -xvzf hadoop-${HADOOP_VERSION}.tar.gz \
      && mv hadoop-${HADOOP_VERSION} hadoop \
      && rm hadoop-${HADOOP_VERSION}.tar.gz

RUN  wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/1.11.718/aws-java-sdk-1.11.718.jar -P $SPARK_HOME/jars/ \
      && wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-core/1.11.718/aws-java-sdk-core-1.11.718.jar -P $SPARK_HOME/jars/ \
      && wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-s3/1.11.718/aws-java-sdk-s3-1.11.718.jar -P $SPARK_HOME/jars/ \
      && wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-kms/1.11.718/aws-java-sdk-kms-1.11.718.jar -P $SPARK_HOME/jars/ \
      && wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-dynamodb/1.11.718/aws-java-sdk-dynamodb-1.11.718.jar -P $SPARK_HOME/jars/ \
      && wget https://repo1.maven.org/maven2/org/apache/httpcomponents/httpclient/4.5.9/httpclient-4.5.9.jar -P $SPARK_HOME/jars/ \
      && wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION}/hadoop-aws-${HADOOP_VERSION}.jar -P $SPARK_HOME/jars/ \
      && echo "spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem" >> $SPARK_HOME/conf/spark-defaults.conf.template \
      && echo "spark.hadoop.fs.s3a.aws.credentials.provider=org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider" >> $SPARK_HOME/conf/spark-defaults.conf.template \
      && echo "spark.hadoop.fs.s3a.multiobjectdelete.enable=false" >> $SPARK_HOME/conf/spark-defaults.conf.template \
      && cp $SPARK_HOME/conf/spark-defaults.conf.template $SPARK_HOME/conf/spark-defaults.conf \
      && cd /

#Give permission to execute scripts
RUN chmod +x /wait-for-step.sh && chmod +x /execute-step.sh && chmod +x /finish-step.sh

# Fix the value of PYTHONHASHSEED
# Note: this is needed when you use Python 3.3 or greater
ENV PYTHONHASHSEED 1
