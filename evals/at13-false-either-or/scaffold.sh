#!/bin/bash
# Writes this case's fixture into the run's working directory.
set -euo pipefail
mkdir -p startup
cat > startup/runway.md <<'FIXTURE'
# Runway

Savings: $38,000
Monthly costs (rent, food, insurance): $3,100
Startup revenue so far: $450 a month
FIXTURE
