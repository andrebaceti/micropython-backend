#!/bin/bash
set -e

echo "############################"
echo "Waiting fot kong to kick in!"
echo "############################"

until curl -sSf ${API_GATEWAY_URL} > /dev/null; do
  >&2 echo "Kong is not ready"
  sleep 1
done
echo "Kong is ok!"
