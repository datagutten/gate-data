#!/usr/bin/env bash
docker compose run --rm export_metrics
docker compose exec prometheus promtool tsdb create-blocks-from openmetrics /metrics.txt /prometheus
docker compose restart prometheus