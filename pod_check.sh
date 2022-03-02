#!/bin/bash
tries=0
while [ "$(kubectl get pods -l=app='activemq' -o jsonpath='{.items[*].status.containerStatuses[0].ready}')" != "true" ]; do
  sleep 5
  echo "Waiting for Broker to be ready."
  ((tries++))
  if [[ $tries -gt 4 ]]; then
    kubectl describe pod photographer
    exit 1
  fi
done
