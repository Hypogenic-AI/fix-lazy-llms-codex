# Fixing Lazy LLMs

This project tests whether harsher self‑critique prompts and response‑budget control reduce “lazy” LLM outputs on reasoning benchmarks. We evaluate prompt variants using real API calls on GSM8K and ARC‑Challenge.

## Key Findings (n=50 per dataset)
- Chain‑of‑Thought improves accuracy on GSM8K (+0.22 vs direct).
- Harsh‑critic prompting **decreases** accuracy on both datasets (worst with low budgets).
- Rude vs polite tone has minimal or inconsistent impact.

## How to Reproduce
1. Create/activate environment:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```
2. Run EDA:
   ```bash
   python src/eda.py
   ```
3. Run experiments (requires `OPENAI_API_KEY`):
   ```bash
   python src/run_experiments.py --gsm8k-n 50 --arc-n 50
   ```
4. Analyze results:
   ```bash
   python src/analysis.py
   ```

## Project Structure
- `src/` — experiment scripts and utilities
- `datasets/` — local dataset copies
- `results/` — outputs, metrics, and summaries
- `figures/` — plots for EDA
- `REPORT.md` — full research report

See `REPORT.md` for detailed methodology, results, and limitations.
