<!-- Frozen test dialogue for at01b-during-in-progress. scripts/build-histories.py turns it into history.jsonl before each run. -->

### user
We're a team of eight and our Jenkins server keeps falling over. I'm wondering whether to move CI to GitHub Actions. What should I be thinking about?

### assistant
A few things usually decide this:

- **Cost:** Actions bills by the minute beyond the included quota, so your build volume matters.
- **Migration effort:** pipelines, plugins and secrets all need porting.
- **Runners:** GitHub-hosted runners need no maintenance; self-hosted runners are cheaper at volume but bring back some upkeep.
- **Integrations:** check that whatever your Jenkins plugins do has an equivalent.

How long are your builds, and roughly how many run a day?

### user
Builds take about 25 minutes, mostly Docker builds, and we run maybe 60 a day. We use a couple of Jenkins plugins for Slack notifications and test reports.

### assistant
That's about 1,500 build minutes a day, or roughly 33,000 a month. Your plan includes 3,000, so you'd pay for about 30,000 extra Linux minutes: around $240 a month at current rates. Slack notifications and test reports both have well-used Actions equivalents, so those shouldn't block you.

### user
Hmm, $240 a month is more than I expected. The Jenkins VM costs us about $80 a month, but I spend maybe four hours a month keeping it alive.

### assistant
Four hours of your time a month is a real cost too, and it's easy to leave out because it doesn't show up on an invoice. One middle path is self-hosted runners on a VM like the one you have now: you'd get the Actions workflow format and pay roughly what you pay today.

### user
Self-hosted runners would mean we still maintain machines, though. I keep going back and forth. Jenkins is annoying, but at least the time I spend on it is predictable.

### assistant
That's a reasonable thing to weigh: predictable effort against a bigger bill with less upkeep. It might help to look at what actually breaks on the Jenkins server, and whether that would go away with self-hosted runners.
