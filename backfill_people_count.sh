#!/usr/bin/env bash
set -e
docker compose run --rm parse_data
docker compose run --rm people_count_openmetrics
docker compose exec prometheus find /prometheus/people_count -name "metrics_*.txt" -exec promtool tsdb create-blocks-from openmetrics {} /prometheus \;
