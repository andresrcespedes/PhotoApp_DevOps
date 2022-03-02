#!/bin/bash
tries=0
while [ "$(kubectl get pods -l=app='photo-service' -o jsonpath='{.items[*].status.containerStatuses[0].ready}')" != "true" ]; do
  sleep 5
  echo "Waiting for photo pod to be ready."
  ((tries++))
  if [[ $tries -gt 4 ]]; then
    kubectl describe pod photo
    exit 1
  fi
done
