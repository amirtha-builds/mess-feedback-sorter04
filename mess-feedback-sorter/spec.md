# Project Specification: Mess Feedback Sorter

*Improvement: Recurring Complaint Spotlight and Meal-Time Check*

(Markdown copy of `spec/Mess_Feedback_Sorter_Specification_Final.docx`. The .docx is the signed-off original.)

## 1. Problem and Objective
The hostel mess committee receives student feedback in English, Tamil and Tanglish. Manually reading every comment can delay the identification of food-safety concerns and repeated service problems. This small console-based Python tool classifies feedback, highlights possible health risks and prepares reports. It only sorts and highlights information; the warden and mess committee decide what action to take.

## 2. Input Files
The application uses two CSV input files. `feedback_input.csv` contains at least 20 student comments with columns id, date, meal and comment. `mess_schedule_input.csv` contains meal, scheduled_start, scheduled_end and serving_counter. The schedule is reference information used to show scheduled meal times; it does not prove the actual serving time.

## 3. LLM Classification Rules
For each non-empty comment, the LLM must return one JSON object with exactly four fields: category, sentiment, urgent and summary. category must be taste, hygiene, quantity, timing or other. sentiment must be positive, negative or neutral. urgent must be true or false. summary must contain no more than 12 words. The LLM must return JSON only.

## 4. Definition of Urgent
A comment is urgent only when it indicates a possible health risk, such as a foreign object in food, stale or spoiled food, or someone becoming sick after eating. Taste, quantity and timing complaints are never urgent, however strongly they are expressed.

## 5. Validation and Safety Net
Python validates every LLM reply for the required fields and allowed values. An invalid reply is retried once; if it is still invalid, the comment is labelled needs_manual_review. Empty or whitespace-only comments are not sent to the LLM and go directly to needs_manual_review. A Python safety net scans the original comment for health-risk terms such as insect, cockroach, hair, expired, vomit, poochi and mudi. It may change urgent from false to true, but never from true to false. Python performs all counting and percentage calculations.

## 6. Unique Improvement: Recurring Complaint Spotlight
Python checks a small set of predefined issue keywords or themes. When the same theme appears in at least two different feedback comments, summary.txt lists it as a recurring issue with its count and feedback IDs. This is a rule-based highlight, not an automatic decision. A committee member checks the original comments because keyword matching may miss differently worded complaints or group unrelated comments together.

## 7. Meal-Time Check
The program uses mess_schedule_input.csv to display the scheduled start and end time for the meal mentioned in a timing complaint. It will not calculate an actual delay unless the feedback contains a clear actual serving time. This avoids treating an unverified complaint as measured data.

## 8. Output Files and Human Checkpoint
The program creates results.csv (all comments and labels), urgent.csv (urgent comments with original text) and summary.txt (category counts, percentage of negative comments, urgent list, recurring issue highlights and relevant scheduled meal times). The warden reads every original comment in urgent.csv. The mess committee reviews recurring issue highlights and timing information before deciding what action to take.

## 9. Scope and Limitation
The application remains a small console-based tool with two input CSV files and three output files. It does not require a database or graphical interface. LLM labels and keyword-based highlights may be incorrect, especially for ambiguous or mixed-language comments, so human review remains essential.

---

## Implementation decisions that go beyond the wording of the spec
The spec leaves these details open. The code makes these choices; edit this list if you change them.

| Topic | Choice in the code |
|---|---|
| Safety-net word list | The spec says "such as". The code uses a longer list (insect, cockroach, hair, stone, plastic, expired/expiry, stale, spoiled, smelled sour, vomit, fell sick, stomach pain, poochi, mudi, vaanthi and more). Words are matched as whole words, so "mudi" does not match "mudiyala". |
| % negative | Negative comments divided by ALL comments, including needs_manual_review ones. |
| needs_manual_review row | category and sentiment are both `needs_manual_review`, urgent is False. The safety net still runs on non-empty ones, so a health word in a comment the LLM failed on still reaches urgent.csv. |
| Recurring theme | Appears in at least 2 different comment IDs, matched by predefined phrases (late/delayed service, food running short, foreign object, spoiled/expired food, illness, salt/spice, cold food, counter closing early). Phrases like "minutes late" are used instead of bare "late" so "the late lunch batch" is not counted as a delay complaint. |
| Meal-time check | Applies to comments the LLM labelled `timing` that are not positive. Delay is calculated only for phrases like "started only at 8:15". |
| Model and key | Gemini API (free tier). Key is read from the `GEMINI_API_KEY` environment variable or a git-ignored `.env`. |
