#!/usr/bin/env bash
# Sourced by pixi activation to load local secrets (e.g. ADS_API_TOKEN) from .env
if [ -f "$PIXI_PROJECT_ROOT/.env" ]; then
    set -a
    # shellcheck disable=SC1091
    source "$PIXI_PROJECT_ROOT/.env"
    set +a
fi
