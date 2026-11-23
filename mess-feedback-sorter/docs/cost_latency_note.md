# Cost and latency note

> **Status: ESTIMATE.** Replace the measured values with real numbers after one live run. The run prints
> total time and the number of API calls, and `outputs/run_log.txt` keeps them.

## API calls for one day of input
- One API call per non-empty comment. Empty comments make **0** calls.
- A retry (only if the first reply is invalid) adds 1 call for that comment.
- **Sample file (20 comments, covers 7 days):** 20 calls if every reply is valid, at most 40 in the worst case (every reply invalid twice).
- **One real day:** the sample averages about 3 comments per day, so about 3 calls per day. Even a busy day of 30 comments is 30 calls.
- Eval harness: 5 + 3 test inputs, 7 calls (the empty one makes none).

## Latency
- Estimated 1 to 3 seconds per call for a small Flash-class model (**estimate, measure it**).
- The code waits 1.5 s between calls (`--delay`, `CALL_DELAY_SECONDS`) to stay inside free-tier rate limits.
- So the 20-comment file takes roughly 20 x (about 2 s call + 1.5 s wait) = about 70 seconds. Measured: ______ s.
- Python steps (validation, safety net, counting, reports) take well under a second.

## Cost per day
- **On the free tier: Rs 0.** A key from Google AI Studio is enough for this project.
- **If paid (assumed numbers, check the current price page before quoting):**
  - Tokens per call: system prompt about 700 input tokens + comment about 30 = about 730 in; reply about 45 out.
  - 20 calls = about 14,600 input + 900 output tokens.
  - With an assumed price of $0.30 per 1M input and $2.50 per 1M output tokens: 0.0044 + 0.0023 = **about $0.007 for the 20-comment file** (under Rs 1), so well under that for one day.
  - Formula: cost = (calls x 730 / 1,000,000 x input price) + (calls x 45 / 1,000,000 x output price).
- Cost is not the real constraint for this tool. Reading time saved and not missing a health risk matter more.
