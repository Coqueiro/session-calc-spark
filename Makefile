
HUB_PUBLISHER=coqueirotree
HUB_PASSWORD?=$(shell cat .hub_password)
CLUSTER_COMPONENT?=base
APP_IMAGE=${HUB_PUBLISHER}/spark-session-calc2.4.4-hadoop2.7-aws-support
APP_VERSION=$(shell cat session-calc/VERSION)
IMAGE=$(shell \
	([ "${CLUSTER_COMPONENT}" = "base" ] && echo "${HUB_PUBLISHER}/spark-base2.4.4-hadoop2.7-aws-support") || \
	([ "${CLUSTER_COMPONENT}" = "master" ] && echo "${HUB_PUBLISHER}/spark-master2.4.4-hadoop2.7-aws-support" || \
	([ "${CLUSTER_COMPONENT}" = "worker" ] && echo "${HUB_PUBLISHER}/spark-worker2.4.4-hadoop2.7-aws-support" || \
	([ "${CLUSTER_COMPONENT}" = "submit" ] && echo "${HUB_PUBLISHER}/spark-submit2.4.4-hadoop2.7-aws-support" || \
	([ "${CLUSTER_COMPONENT}" = "session-calc" ] && echo "${APP_IMAGE}" \
)))))
VERSION=$(shell cat ${CLUSTER_COMPONENT}/VERSION)
BUMP_LEVEL?=patch # patch minor major
GIT_BRANCH=$(shell git branch | sed -n -e 's/^\* \(.*\)/\1/p')

ARG1?=arg1

build:
	@cd ${CLUSTER_COMPONENT} ; docker build -t "${IMAGE}:${VERSION}" .
	@docker tag ${IMAGE}:${VERSION} ${IMAGE}:latest

# CLUSTER_COMPONENT=base make build; CLUSTER_COMPONENT=worker make build; CLUSTER_COMPONENT=master make build; CLUSTER_COMPONENT=submit make build; CLUSTER_COMPONENT=session-calc make build

login:
	@docker login --username ${HUB_PUBLISHER} --password ${HUB_PASSWORD}

push: login
	@docker push ${IMAGE}:${VERSION}
	@docker push ${IMAGE}:latest

pull:
	@docker pull ${IMAGE}:${VERSION}
	@docker pull ${IMAGE}:latest

bump:
	@bumpversion --current-version ${VERSION} ${BUMP_LEVEL} ${CLUSTER_COMPONENT}/VERSION
	@git add ${CLUSTER_COMPONENT}/VERSION
	@git commit -m "${CLUSTER_COMPONENT} version bump to ${VERSION}"
	@git push origin ${GIT_BRANCH}

run:
	# @docker-compose -f docker-compose.yml up -d
	@docker run --name session-calc -e ENABLE_INIT_DAEMON=false --link spark-master:spark-master --net spark-cluster_default ${APP_IMAGE}:${APP_VERSION}

clean:
	@docker rm -f $(shell docker ps -a -q --filter 'name=session-calc')
	# @docker-compose -f docker-compose.yml down

debug:
	@docker run -it ${IMAGE}:${VERSION} bash
