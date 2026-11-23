# Mess Feedback Sorter

Console-based Python tool for the CIT AI-Native Engineering Programme capstone (Assessment 5).
It reads hostel mess feedback in English, Tamil and Tanglish. An LLM labels each comment
(category, sentiment, urgent, summary). **Python checks every reply**, adds a safety net for
health-risk words, does all the counting, and writes reports. **The tool only labels and sorts.
The warden and the mess committee decide what action to take.**

Improvement added to the base project: **Recurring Complaint Spotlight** and **Meal-Time Check**.

## Folder layout

```
mess-feedback-sorter/
  README.md  .gitignore  .env.example  requirements.txt
  spec.md                       spec (markdown copy)
  spec/                         signed-off spec (.docx)
  feedback_input.csv            input: id, date, meal, comment (20 comments)
  mess_schedule_input.csv       input: meal, scheduled_start, scheduled_end, serving_counter
  system_prompt.txt             LLM prompt (Authority, Exemplar, Constraint, Rubric, Metadata)
  mess_sorter.py                the program
  eval_harness.py               5 normal tests + 3 red-team inputs
  test_units.py                 24 offline unit tests
  outputs/                      results.csv, urgent.csv, summary.txt, run_log.txt, eval_log.txt
  docs/                         eval results, red-team, judgment framework, cost note, journal, checklist
```

## Setup

1. Python 3.10 or newer.
2. `pip install -r requirements.txt`
3. Get a free key from Google AI Studio. Copy `.env.example` to `.env` and put the key in it:
   `GEMINI_API_KEY=your-key-here`  (`.env` is in `.gitignore`. **Never write the key inside the code.**)

## Run

```
python mess_sorter.py               # live run, writes the three reports to outputs/
python eval_harness.py              # live eval: 5 normal tests + 3 red-team inputs
python -m unittest test_units -v    # offline unit tests, no key needed
```

No key yet? Add `--mock` to either program. This uses a fake offline "LLM" so you can see the
whole pipeline work. **Mock results are only a demo. Do not submit them as live results.**

## What the program does

| Step | Function | Notes |
|---|---|---|
| Read files | `load_feedback()`, `load_schedule()` | csv module |
| Empty comment | `classify()` | never sent to the LLM, goes to `needs_manual_review` |
| Call the LLM | `classify()` -> `client.generate()` | one call per non-empty comment |
| Parse and check | `parse_reply()`, `is_valid()` | exact 4 fields, allowed values, `urgent` must be a boolean, summary 12 words or fewer |
| Retry and fallback | `classify()` | one retry, then `needs_manual_review`. API errors are caught |
| Safety net | `apply_safety_net()` | health word in the original text raises urgent to true, never lowers it |
| Count | `count_by_category()`, `percent_negative()` | all Python, the LLM never counts |
| Recurring spotlight | `find_recurring_issues()` | theme in at least 2 different comments, with IDs |
| Meal-time check | `meal_time_check()` | shows scheduled time; delay only if the comment states an actual time |
| Reports | `write_reports()` | results.csv, urgent.csv, summary.txt |

## Outputs

- `results.csv`: every comment with category, sentiment, urgent, summary (plus whether the safety net raised it).
- `urgent.csv`: only urgent comments with the original text. **The warden reads every row.**
- `summary.txt`: counts per category, % negative, urgent list, recurring issues, timing complaints with scheduled meal times.

## IMPORTANT: the files currently in `outputs/` and `docs/`

They were generated with the offline **mock** LLM (the first line of `run_log.txt` and `summary.txt` says so).
Before submitting, run `python mess_sorter.py` and `python eval_harness.py` with your real key,
then write your own notes in `docs/red_team.md` and `docs/eval_results.md`.
Re-running the eval harness overwrites those two files.

## Suggested commits (you need at least 3 meaningful ones)

```
git init
git add .gitignore .env.example README.md spec spec.md feedback_input.csv mess_schedule_input.csv
git commit -m "Add spec, input files and .gitignore"
git add system_prompt.txt mess_sorter.py requirements.txt
git commit -m "Add LLM classifier, validator, retry, fallback and safety net"
git add eval_harness.py test_units.py
git commit -m "Add eval harness, red-team inputs and unit tests"
git add outputs docs
git commit -m "Add live outputs, judgment framework and cost note"
git status          # .env must NOT be listed
```

## Limitations

LLM labels and keyword highlights can be wrong, especially for ambiguous or mixed-language comments.
Keyword matching can miss differently worded complaints or group unrelated ones.
Human review remains essential.
