# AI Decision Journal

> **This is a DRAFT.** The "AI suggested" column records what Claude proposed while building the starter code
> from your spec. The last two columns are for YOU: decide whether you accept it, and why. Delete or rewrite
> any entry that is not true for your own work. You must be able to explain every line in the Q&A.

| # | Decision point | What the AI suggested | My decision (accept / change / reject) | Why |
|---|---|---|---|---|
| 1 | Which LLM API | Gemini API, free tier, key from an environment variable or git-ignored `.env` | | |
| 2 | How strict the validator is | Exactly 4 fields, allowed values, `urgent` must be a real boolean, summary 12 words or fewer; code fences tolerated, prose around JSON is not | | |
| 3 | What happens when validation fails twice | `needs_manual_review` label, and the safety net still runs on the original text | | |
| 4 | Safety-net word list | A longer list than the spec examples (stone, plastic, stale, spoiled, smelled sour, stomach pain, vaanthi...), matched as whole words | | |
| 5 | % negative denominator | All comments, including needs_manual_review ones | | |
| 6 | Recurring-theme rules | Fixed phrase lists; "minutes late" instead of bare "late" so "late lunch batch" is not a delay complaint | | |
| 7 | Meal-time check | Show scheduled times only; calculate a delay only when the comment states a clear actual time, labelled unverified | | |
| 8 | Prompt injection defence | Comment wrapped in `<<< >>>` as data, a CONSTRAINT line, an injection example in the prompt, and the Python safety net as the final layer | | |
| 9 | Offline `--mock` mode | A fake LLM so the code can be tested without a key. It is clearly labelled and must not be reported as a live result | | |
| 10 | Eval and red-team inputs | 5 normal + 3 red-team cases, including "expiry date" to test the safety net | | |

## Things I checked or corrected myself
- 
