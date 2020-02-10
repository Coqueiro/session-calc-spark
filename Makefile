READ_PATH?=s3a://grupozap-data-engineer-test/
WRITE_PATH?=session-calc/output
USER_KEY?=anonymous_id
TIMESTAMP_KEY?=device_sent_timestamp
MAX_SESSION_SECONDS?=1800
GROUP_KEY?=device_family # [browser_family, device_family, os_family]

HUB_PUBLISHER?=coqueirotree
HUB_PASSWORD?=$(shell cat .hub_password)
SPARK_VERSION?=2.4.4
HADOOP_VERSION?=3.1.2
BUMP_LEVEL?=patch # [patch, minor, major]

APP_IMAGE=${HUB_PUBLISHER}/spark-session-calc${SPARK_VERSION}-hadoop${HADOOP_VERSION}-aws-support
SUBMIT_VERSION=$(shell cat docker-spark/submit/VERSION)
APP_VERSION=$(shell cat session-calc/VERSION)
GIT_BRANCH=$(shell git branch | sed -n -e 's/^\* \(.*\)/\1/p')


test_app:
	@docker run --rm --name docker-pyspark \
	-v $(shell pwd)/session-calc:/app:ro \
	-e READ_PATH=test/data/part0.json \
	-e WRITE_PATH=/output \
	-e USER_KEY=user_key \
	-e TIMESTAMP_KEY=timestamp_key \
	-e MAX_SESSION_SECONDS=3600 \
	-e GROUP_KEY=group_field1 \
	coqueirotree/docker-pyspark:0.0.1 \
	python3 -m unittest

build_app:
	@cd session-calc ; \
	docker build \
	--build-arg HUB_PUBLISHER="${HUB_PUBLISHER}" \
	--build-arg SPARK_VERSION="${SPARK_VERSION}" \
	--build-arg HADOOP_VERSION="${HADOOP_VERSION}" \
	--build-arg SUBMIT_VERSION="${SUBMIT_VERSION}" \
	-t "${APP_IMAGE}:${APP_VERSION}" .
	@docker tag ${APP_IMAGE}:${APP_VERSION} ${APP_IMAGE}:latest

login:
	@docker login --username ${HUB_PUBLISHER} --password ${HUB_PASSWORD}

push_app: login
	@docker push ${APP_IMAGE}:${APP_VERSION}
	@docker push ${APP_IMAGE}:latest

bump_app:
	@python3 -m pip install bumpversion==0.5.3
	@bumpversion --current-version ${APP_VERSION} ${BUMP_LEVEL} session-calc/VERSION
	@git add session-calc/VERSION
	@git commit -m "session-calc version bump to ${VERSION}"
	@git push origin ${GIT_BRANCH}

release_app: build_app push_app

pull_app:
	@docker pull ${APP_IMAGE}:${APP_VERSION}
	@docker pull ${APP_IMAGE}:latest

release_docker_spark:
	@cd docker-spark/base; CLUSTER_COMPONENT=base make release
	@cd docker-spark/master; CLUSTER_COMPONENT=master make release
	@cd docker-spark/worker; CLUSTER_COMPONENT=worker make release
	@cd docker-spark/submit; CLUSTER_COMPONENT=submit make release

build_docker_spark:
	@CLUSTER_COMPONENT=base make build
	@CLUSTER_COMPONENT=master make build
	@CLUSTER_COMPONENT=worker make build
	@CLUSTER_COMPONENT=submit make build

pull_docker_spark:
	@CLUSTER_COMPONENT=base make pull
	@CLUSTER_COMPONENT=master make pull
	@CLUSTER_COMPONENT=worker make pull
	@CLUSTER_COMPONENT=submit make pull

# Support currently available for local docker spark execution only
run_docker_spark:
	@cd docker-spark; docker-compose -f docker-compose.yml up -d
	@echo "Waiting 10 seconds for docker-spark cluster setup."; sleep 10

run_app: run_docker_spark
	@docker run --rm --name session-calc \
	-e ENABLE_INIT_DAEMON=false \
	-e READ_PATH=${READ_PATH} \
	-e WRITE_PATH=${WRITE_PATH} \
	-e USER_KEY=${USER_KEY} \
	-e TIMESTAMP_KEY=${TIMESTAMP_KEY} \
	-e MAX_SESSION_SECONDS=${MAX_SESSION_SECONDS} \
	-e GROUP_KEY=${GROUP_KEY} \
	-v $(shell pwd)/session-calc/output:/app/output:rw \
	--link spark-master:spark-master \
	--net docker-spark_default ${APP_IMAGE}:${APP_VERSION}

clean_app:
	@echo "Removing dangling containers."
	@cd docker-spark; docker-compose -f docker-compose.yml down

session_calc: run_app clean_app

run_eda: run_docker_spark
	@docker run --rm --name eda \
	-e ENABLE_INIT_DAEMON=false \
	-e READ_PATH=${READ_PATH} \
	-v $(shell pwd)/eda:/app:ro \
	--link spark-master:spark-master \
	--net docker-spark_default ${APP_IMAGE}:${APP_VERSION}

eda: run_eda clean_app

debug_app:
	@docker run -it \
	-v $(shell pwd)/session-calc/output:/app/output:rw \
	${APP_IMAGE}:${APP_VERSION} bash
