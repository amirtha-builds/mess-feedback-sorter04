# Judgment Framework

> **Check before submitting:** the three questions below are my working version. Replace the column
> headings with the exact three questions from your Week-11 class slides if they are worded differently.

| Part of the tool | 1. What could go wrong? | 2. How would we notice or limit it? | 3. Who decides / who checks? |
|---|---|---|---|
| **LLM category label** | Wrong category, e.g. "mudi" read as "other" | Python validates allowed values; the category is only used for counts, never for urgency | Mess committee reads the original comments, not only the counts |
| **LLM sentiment label** | Sarcasm or mixed language misread | Only used for the "% negative" figure, which is labelled as approximate | Committee treats the % as a rough indicator |
| **Urgent flag (most critical)** | **False negative**: a health risk is missed, e.g. an instruction hidden in the comment, an unfamiliar Tamil word, "expired" not linked to "spoiled". **False positive**: a harmless comment flagged | Python safety net scans the original text for health words and can only RAISE urgency. Unit tests and red-team cover injection and Tanglish. False positives only cost the warden a few seconds | **Warden reads every original comment in urgent.csv** and decides the action (check the kitchen, check on the sick student). The tool never acts by itself |
| **Reply validator + retry + fallback** | Malformed JSON, wrong fields, API error, crash | `is_valid()` rejects bad replies, one retry, then `needs_manual_review`. All API errors are caught, so one bad reply never crashes the run | Committee reads the needs_manual_review list in summary.txt by hand |
| **Empty comments** | Model invents a label for nothing | Never sent to the LLM, straight to `needs_manual_review` | Committee decides if the empty entry matters |
| **Counting and %** | LLM miscounts | Python does all counting; the LLM is never asked to count | Anyone can recount from results.csv |
| **Recurring Complaint Spotlight** | Keywords miss differently worded complaints, or group unrelated comments | Predefined themes, needs at least 2 comments, shows the IDs so they can be opened. Labelled "rule-based highlight, not a decision" | **Committee member reads the listed original comments** before acting |
| **Meal-Time Check** | Schedule treated as proof of an actual delay | Shows scheduled times only. A delay is calculated only if the comment states a clear actual serving time, and is labelled "student's statement, not verified" | Committee verifies the actual serving time (kitchen/counter record) before acting |
| **Whole tool** | People over-trust the output | Tool only labels and sorts. Summary ends with a limitations note | Warden (health risks) and mess committee (patterns, timing) make every decision |

**Human checkpoints (named):** (1) the warden reads every comment in urgent.csv; (2) the mess committee reviews recurring issues, timing information and needs_manual_review comments before any action.
