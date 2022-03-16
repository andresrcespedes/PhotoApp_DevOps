#!/bin/bash
>- /kaniko/executor \
    --context "${CI_PROJECT_DIR}/app/filter-service" \
    --dockerfile "${CI_PROJECT_DIR}/app/filter-service/Dockerfile" \
    --destination "${CI_REGISTRY_IMAGE}/filter:${CI_COMMIT_SHORT_SHA}" \
    --build-arg HTTP_PROXY=${HTTP_PROXY} \
    --build-arg HTTPS_PROXY=${HTTPS_PROXY}
