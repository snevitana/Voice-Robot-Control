#!/usr/bin/env bash
set -euo pipefail

voice-robot list-commands --config configs/pc_simulation.yaml
voice-robot test-match "поверни налево" --config configs/pc_simulation.yaml
voice-robot demo-text --text "стоп" --config configs/pc_simulation.yaml
