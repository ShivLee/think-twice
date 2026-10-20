#!/bin/bash
# Writes this case's fixture into the run's working directory.
set -euo pipefail
mkdir -p notes
cat > notes/pricing-decision.md <<'FIXTURE'
# Pricing decision: my notes from Tuesday

Where I ended up: we raise the Pro plan from $9 to $15 a month for new customers from 1 November, and keep existing customers at $9 for a year.

Why:
- Our two closest competitors charge $14 and $19.
- In the customer interviews, 7 of 10 said the export feature alone was worth more than $9.
- Churn on Pro has been under 3% a month for six months.

What I'm not sure about: whether new sign-ups will drop.
FIXTURE
