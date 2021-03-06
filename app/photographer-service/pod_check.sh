#!/bin/bash
tries=0
MAX_TRIES=9
while [ "$(kubectl get pods -l=app='photographer-service' -o jsonpath='{.items[*].status.containerStatuses[0].ready}')" != "true" ]; do
  if [[ $tries -gt $MAX_TRIES ]]; then
    kubectl describe pod photographer
    exit 1
  fi
  sleep 5
  echo "Waiting for photographer pod to be ready."
  ((tries++))
done
