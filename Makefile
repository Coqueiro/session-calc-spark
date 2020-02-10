HUB_PUBLISHER?=coqueirotree
HUB_PASSWORD?=$(shell cat .hub_password)
SPARK_VERSION?=2.4.4
HADOOP_VERSION?=3.1.2
APP_IMAGE=${HUB_PUBLISHER}/spark-session-calc${SPARK_VERSION}-hadoop${HADOOP_VERSION}-aws-support
SUBMIT_VERSION=$(shell cat docker-spark/submit/VERSION)
APP_VERSION=$(shell cat session-calc/VERSION)


build_app:
	@cd session-calc ; \
	docker build \
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

bump:
	@python3 -m pip install bumpversion==0.5.3
	@bumpversion --current-version ${APP_VERSION} ${BUMP_LEVEL} session-calc/VERSION
	@git add ${session-calc}/VERSION
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

# Support currently available for local docker spark execution only
run_app:
	@cd docker-spark; docker-compose -f docker-compose.yml up -d
	@echo "Waiting 10 seconds for docker-spark cluster setup"; sleep 10
	@docker run --name session-calc -e ENABLE_INIT_DAEMON=false --link spark-master:spark-master --net docker-spark_default ${APP_IMAGE}:${APP_VERSION}

clean_app:
	@docker rm -f $(shell docker ps -a -q --filter 'name=session-calc')
	@cd docker-spark; docker-compose -f docker-compose.yml down

session_calc: run_app clean_app
