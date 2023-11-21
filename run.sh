#!/bin/bash
cd $(dirname "$(realpath "$0")")
docker cp back_django:/app/media .
docker compose up -d --build