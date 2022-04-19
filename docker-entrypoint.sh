#!/bin/sh

# Set failure
set -e

# Activate our virtual environment here
. /opt/pysetup/.venv/bin/activate

# Evaluating passed command:
exec "$@"
