#!/usr/bin/env bash
set -euo pipefail

MODEL_NAME="vosk-model-small-ru-0.22"
MODEL_ZIP="${MODEL_NAME}.zip"
MODEL_URL="https://alphacephei.com/vosk/models/${MODEL_ZIP}"

mkdir -p models

if [ -d "models/${MODEL_NAME}" ]; then
  echo "Model already exists: models/${MODEL_NAME}"
  exit 0
fi

echo "Downloading ${MODEL_URL}"
curl -L "${MODEL_URL}" -o "models/${MODEL_ZIP}"

echo "Unpacking model"
unzip -q "models/${MODEL_ZIP}" -d models

echo "Model path: models/${MODEL_NAME}"
echo "Set vosk_model_path in config to: models/${MODEL_NAME}"
