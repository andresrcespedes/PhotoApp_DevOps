#!/bin/bash
tries=0
MAX_TRIES=9
while [ "$(kubectl get pods -l=app='tags-service' -o jsonpath='{.items[*].status.containerStatuses[0].ready}')" != "true" ]; do
  if [[ $tries -gt $MAX_TRIES ]]; then
    kubectl describe pod tags
    exit 1
  fi  sleep 5
  echo "Waiting for tags pod to be ready."
  ((tries++))
done
