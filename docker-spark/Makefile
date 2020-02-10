
HUB_PUBLISHER?=coqueirotree
HUB_PASSWORD?=$(shell cat ../.hub_password)
CLUSTER_COMPONENT?=base # [base, master, worker, submit]

# Beware, changes in Spark and Hadoop versions may require additional changes in the project
SPARK_VERSION?=2.4.4
HADOOP_VERSION?=3.1.2

BUMP_LEVEL?=patch # [patch, minor, major]

IMAGE=$(shell \
	([ "${CLUSTER_COMPONENT}" = "base" ] && echo "${HUB_PUBLISHER}/spark-base${SPARK_VERSION}-hadoop${HADOOP_VERSION}-aws-support") || \
	([ "${CLUSTER_COMPONENT}" = "master" ] && echo "${HUB_PUBLISHER}/spark-master${SPARK_VERSION}-hadoop${HADOOP_VERSION}-aws-support" || \
	([ "${CLUSTER_COMPONENT}" = "worker" ] && echo "${HUB_PUBLISHER}/spark-worker${SPARK_VERSION}-hadoop${HADOOP_VERSION}-aws-support" || \
	([ "${CLUSTER_COMPONENT}" = "submit" ] && echo "${HUB_PUBLISHER}/spark-submit${SPARK_VERSION}-hadoop${HADOOP_VERSION}-aws-support" \
))))
BASE_VERSION=$(shell cat base/VERSION)
VERSION=$(shell cat ${CLUSTER_COMPONENT}/VERSION)
GIT_BRANCH=$(shell git branch | sed -n -e 's/^\* \(.*\)/\1/p')


build:
	@cd ${CLUSTER_COMPONENT} ; \
	docker build \
	--build-arg HUB_PUBLISHER="${HUB_PUBLISHER}" \
	--build-arg SPARK_VERSION="${SPARK_VERSION}" \
	--build-arg HADOOP_VERSION="${HADOOP_VERSION}" \
	--build-arg BASE_VERSION="${BASE_VERSION}" \
	-t "${IMAGE}:${VERSION}" .
	@docker tag ${IMAGE}:${VERSION} ${IMAGE}:latest

login:
	@docker login --username ${HUB_PUBLISHER} --password ${HUB_PASSWORD}

push: login
	@docker push ${IMAGE}:${VERSION}
	@docker push ${IMAGE}:latest

bump:
	@python3 -m pip install bumpversion==0.5.3
	@bumpversion --current-version ${VERSION} ${BUMP_LEVEL} ${CLUSTER_COMPONENT}/VERSION
	@git add ${CLUSTER_COMPONENT}/VERSION
	@git commit -m "${CLUSTER_COMPONENT} version bump to ${VERSION}"
	@git push origin ${GIT_BRANCH}

release: bump build push

pull:
	@docker pull ${IMAGE}:${VERSION}
	@docker pull ${IMAGE}:latest

debug:
	@docker run -it ${IMAGE}:${VERSION} bash
