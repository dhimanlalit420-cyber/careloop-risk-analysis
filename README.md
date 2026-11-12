# CareLoop Clinics: No-Show Risk Analysis

> Public repository: https://github.com/dhimanlalit420-cyber/careloop-risk-analysis

## Four-part summary

- **Part 1:** Cleaned 1,020 raw bookings to 990 usable rows; 218 were no-shows (22.0%), with 26 distance and 3 fee values capped.
- **Part 2:** No-shows rose to 60.5% for bookings made 31+ days ahead; Gomti Nagar was 33.3% across 90 bookings, so its small volume matters.
- **Part 3:** Logistic regression won on training cross-validation (ROC-AUC 0.774); at threshold 0.35 it flagged 49/198 test bookings, with 57.1% recall and 0.789 ROC-AUC.
- **Part 4:** Gemini and Pydantic validated the nine nonblank notes among the first ten (one note was blank). The resulting categories were 2 forgot/reminder, 2 distance/transport, 1 cost, 1 illness/emergency, 2 work/schedule, and 1 other. Five of ten bookings had no reminder recorded. See `notes_analysed.csv` and `04_genai.ipynb`.

## Recommendation

Start a small front-desk call pilot for bookings with risk probability at least 0.35. This training-selected threshold produced 57.1% recall on the test set and flagged 49 of 198 bookings while the overall no-show rate was 22.0%. Prioritize longer lead times: the no-show rate was 30.0% for 15–30 days and 60.5% for 31+ days, compared with 16.2% for 1–7 days. The first ten follow-up records contain five bookings without a reminder; among the note reasons, forgetting and distance/transport each appeared twice. Use these as script ideas for a limited pilot, then review call outcomes before expanding. The note sample is illustrative, not clinic-wide. Adjust the 0.35 threshold to evening call capacity and the cost of an empty slot. These patterns are associations, not proof of cause.

## Model selection

The final model is logistic regression with a 0.35 threshold. It had the highest training-only five-fold ROC-AUC (0.774; tuned forest 0.767, random forest 0.747, depth-3 tree 0.678). The out-of-fold training F1 was 0.489 at 0.35 versus 0.347 at 0.50, with recall increasing from 0.249 to 0.467. The single final test evaluation at 0.35 gave precision 0.571, recall 0.571, 49 flagged bookings, and ROC-AUC 0.789. `test_risk_scores.csv` contains one score per test booking.

## Part 4 prompt and validation review

For the Hinglish note N007, the minimal V1 prompt returned `forgot`, outside the allowed categories; the structured CRAFT V2 prompt returned `forgot_or_no_reminder`. For ambiguous N009, V1 returned `unreachable`, also outside the allowed categories; V2 returned `other`, following the instruction not to guess. Pydantic checked required fields and the confidence range. A separate pair of deliberately malformed examples confirmed that it rejects an out-of-range confidence and a missing recommended action. The reminder cross-tab covers ten note-linked bookings only: five had a reminder recorded and five did not.

## Limitations

1. Cleaning medians, quartiles, and outlier fences were calculated on all 990 rows before the split, so test rows had a small indirect influence on cleaning.
2. The split is random rather than past-to-future, and the same patient can appear in both training and test sets.
3. The threshold depends on how many calls the front desk can make in an evening; the note sample of ten is only an illustration and cannot establish clinic-wide reasons.
4. The AI summaries and suggested actions are generated from brief notes and require human review. They are administrative suggestions, not clinical advice or evidence of why an individual patient missed care.

## Reproducing the work

The source CSVs are preserved unchanged in `data/`. Run `01_ingest_clean.ipynb` from the repository root to reproduce Part 1 and the SQL load file. Run `02_python_check.py` alongside the queries in `02_queries.sql` to compare clinic counts. Run `03_model.ipynb` to reproduce the split, comparisons, selection, and `test_risk_scores.csv`. Open `04_genai.ipynb` in Colab from this public GitHub repository, run the setup cell, and enter a Gemini API key at the masked run-time prompt; never place the key in a notebook or repository file. The notebook uses Gemini Flash-Lite, validates structured JSON with Pydantic, processes the first ten notes, compares prompts for N007 and N009, and writes `notes_analysed.csv`.

The SQL file creates the schema for MySQL Workbench, then documents the queries. When using SQLiteOnline, skip the `CREATE DATABASE` and `USE` lines as indicated in the file.

## Dependencies

See `requirements.txt`. The Gemini notebook installs `google-genai` and Pydantic in Colab and pauses between calls to respect the free-tier rate limit.
