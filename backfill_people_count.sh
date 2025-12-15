#!/usr/bin/env bash
set -e
SCRIPT_DIRECTORY="$(dirname "$BASH_SOURCE")"

docker compose -f ${SCRIPT_DIRECTORY}/docker-compose.yml run --rm parse_data
docker compose -f ${SCRIPT_DIRECTORY}/docker-compose.yml run --rm people_count_openmetrics
docker compose -f ${SCRIPT_DIRECTORY}/docker-compose.yml exec prometheus find /prometheus/people_count -name "metrics_*.txt" -exec promtool tsdb create-blocks-from openmetrics {} /prometheus \;
