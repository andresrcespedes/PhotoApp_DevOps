#!/bin/bash
tries=0
MAX_TRIES=9
while [ "$(kubectl get pods -l=app='photo-service' -o jsonpath='{.items[*].status.containerStatuses[0].ready}')" != "true" ]; do
  if [[ $tries -gt $MAX_TRIES ]]; then
    kubectl describe pod photo
    exit 1
  fi
  sleep 10
  echo "Waiting for photo pod to be ready."
  ((tries++))
done
