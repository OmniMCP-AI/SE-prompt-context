#!/bin/bash

ENV=$1

if [ "$ENV" = "dev" ]; then
  echo "Refreshing cache on DEV..."
  curl -X 'POST' \
    'https://be-dev.omnimcp.ai/api/v1/tool/cache/refresh' \
    -H 'accept: application/json' \
    -d ''
else
  echo "Refreshing cache on PROD..."
  curl -X 'POST' \
    'https://be.omnimcp.ai/api/v1/tool/cache/refresh' \
    -H 'accept: application/json' \
    -d ''
fi

