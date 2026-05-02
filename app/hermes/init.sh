#!/bin/sh
set -e

. /opt/hermes/.venv/bin/activate

if [ -f /opt/data/config.yaml ]; then
  sed -i \
    -e "s|^  default: \".*\"\$|  default: \"$HERMES_MODEL\"|" \
    -e "s|^  provider: \".*\"\$|  provider: \"$HERMES_PROVIDER\"|" \
    -e "s|^  base_url: \".*\"\$|  base_url: \"$HERMES_BASE_URL\"|" \
    /opt/data/config.yaml

  if grep -q '^  api_key: ' /opt/data/config.yaml; then
    sed -i "s|^  api_key: \".*\"\$|  api_key: \"$HERMES_API_KEY\"|" /opt/data/config.yaml
  else
    sed -i "s|^  # api_key: \"your-key-here\".*\$|  api_key: \"$HERMES_API_KEY\"|" /opt/data/config.yaml
  fi
fi

exec hermes gateway run
