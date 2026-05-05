#!/usr/bin/env bash
set -euxo pipefail

export HF_HOME="${HF_HOME:-/runpod-volume/hf-cache}"
export HUGGINGFACE_HUB_CACHE="${HUGGINGFACE_HUB_CACHE:-/runpod-volume/hf-cache}"
export TRANSFORMERS_CACHE="${TRANSFORMERS_CACHE:-/runpod-volume/hf-cache}"

lorax-launcher \
    --model-id "$MODEL_ID" \
    --port 80 &

python /app/handler.py