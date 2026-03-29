# Improve F1 Prediction Accuracy & Run Method

This implementation plan outlines the proposed improvements to the F1 race prediction engine to ensure it recognizes the current reality of the grid (e.g., Red Bull vs. Mercedes form) rather than falling back to historical biases in the LLM's frozen training data. Furthermore, we'll implement a simpler way to trigger these predictions.

## User Review Required

> [!IMPORTANT]
> Please review this logic to ensure it aligns with what you want:
> - I will modify `race_context.py` to calculate season-to-date points manually and pass them to the LLM. 
> - I will add "recent races from the previous season" logic if we are trying to predict the first few rounds of a new season. 
> - Are you okay with me adding a `predict.ps1` PowerShell script in the root directory and an optional Python CLI script for easier running?

## Proposed Changes

### F1 Prediction Context Upgrades

The main issue is that `build_prediction_context()` gives extremely sparse data to the LLM, particularly when guessing early races of a season (`target_round = 1`). We will enrich this by modifying `app/prediction/race_context.py`:

#### [MODIFY] `f1-app/backend/app/prediction/race_context.py`
1. **Current Constructor and Driver Standings**: Calculate actual F1 points for the current season based on `Lap.position` for previous races (1st=25, 2nd=18, etc.) and group them by `Driver.team`. This proves definitively to the LLM who is winning the current championship.
2. **End-of-Year Baseline (Form carryover)**: If `round_number <= 3`, we will automatically query the last 5 completed races from the *previous* season to help the LLM contextualize team momentum entering the new year.
3. **Starting Grid Injection**: We will query the `GridPosition` table for the upcoming target race. The starting layout of the cars is one of the biggest data points for an accurate prediction.

### Easier Execution 

You currently use `cmds.txt` to run an unwieldy one-liner. Let's build a dedicated runner.

#### [NEW] `predict.ps1`
A simple PowerShell script in the root folder that abstracts the REST API call and nicely outputs the predicted order to your console.
*Usage example:* `.\predict.ps1 -Season 2024 -Round 5`

#### [NEW] `run_prediction.py` (Optional CLI)
A Python-based CLI script inside `f1-app/` that does the same but can be run via standard `python run_prediction.py --season 2024 --round 5`.

## Open Questions

> [!question]
> Do you prefer the new `predict.ps1` to automatically open the results in `notepad` like your old workflow did, or just print the formatted JSON directly into the terminal window?

## Verification Plan

### Automated Tests
- Run `predict.ps1 -Season 2024 -Round 1` to ensure the context successfully fetches 2023 end-of-season data to verify Red Bull's form over Mercedes.
- Inspect the `/pre-race/context/2024/5` output on the backend via curl/browser to visually confirm points, standings, and grid positions show up correctly in the JSON context dump.
