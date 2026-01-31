# Fixing Lazy LLMs — Research Report

## 1. Executive Summary
**Research question**: Do harsher self‑critique prompts and response‑budget controls reduce “lazy” LLM outputs and improve reasoning accuracy compared to standard prompts?

**Key finding**: On GSM8K and ARC‑Challenge (n=50 each), CoT improves accuracy, while harsh‑critic prompting (with or without low budget) substantially **reduces** accuracy; rude vs. polite tone has minimal impact.

**Practical implication**: Simply telling models to be harsh critics (and constraining budgets) is not a reliable fix for “lazy” behavior; standard CoT remains the most robust low‑effort improvement in this setting.

## 2. Goal
We tested the hypothesis that LLM “laziness” can be mitigated by (a) asking the model to act as a harsher critic and (b) controlling response budget. We also tested the common claim that rudeness improves outputs. This matters because test‑time prompting is the cheapest intervention for improving reasoning quality without retraining.

## 3. Data Construction

### Dataset Description
- **GSM8K (test split)**: 1,319 problems; grade‑school math reasoning. Stored at `datasets/gsm8k/`.
- **ARC‑Challenge (test split)**: 1,172 questions; multiple‑choice science reasoning. Stored at `datasets/ai2_arc/`.

### Example Samples
**GSM8K**
```
Q: Janet’s ducks lay 16 eggs per day... How much in dollars does she make every day at the farmers' market?
Gold: 18
```

**ARC‑Challenge**
```
Q: An astronomer observes that a planet rotates faster after a meteorite impact. Which is the most likely effect?
Choices: A/B/C/D
Gold: C
```

### Data Quality
- **Missing values**: 0% for all fields in both datasets (see `results/data_summary.json`).
- **Question length distribution**: saved in `figures/question_length_hist.png`.

### Preprocessing Steps
1. Load datasets from disk with HuggingFace `load_from_disk`.
2. Sample a fixed evaluation subset from the test split (`n=50`) with seed 42.
3. Parse GSM8K final answers via the `####` marker.

### Train/Val/Test Splits
- **Evaluation only**: test splits used (no training).
- **Subset size**: 50 per dataset for cost and runtime control.

## 4. Experiment Description

### Methodology
#### High‑Level Approach
Run controlled prompt variants on the same sample set using the same model and decoding parameters. Compare accuracy, response length, and bootstrap CIs vs. a direct baseline.

#### Why This Method?
This isolates prompt interventions (critic severity, response budget, tone) while holding model and data constant, directly targeting the “lazy output” hypothesis.

### Implementation Details
#### Tools and Libraries
- `openai` 2.16.0
- `datasets` 4.5.0
- `numpy` 2.4.1, `pandas` 3.0.0
- `scipy` 1.17.0
- `matplotlib` 3.10.8, `seaborn` 0.13.2

#### Model
- **Model**: `gpt-4.1` (OpenAI API)
- **Temperature**: 0.0 (deterministic for accuracy)
- **Max output tokens**: 256 (baseline) / 128 (low‑budget condition)

#### Hyperparameters
| Parameter | Value | Selection Method |
|-----------|-------|------------------|
| temperature | 0.0 | standard eval default |
| max_output_tokens | 256 / 128 | budget control ablation |
| seed | 42 | reproducibility for sampling |

#### Experimental Protocol
- **Conditions**:
  1. `direct-neutral` (baseline)
  2. `cot-neutral`
  3. `critic-harsh`
  4. `critic-harsh-lowbudget`
  5. `rude-direct`
  6. `polite-direct`
- **Runs**: 1 run per condition per example (deterministic).
- **Hardware**: RTX 3090 GPUs available (24GB); API‑based inference used (GPU not utilized).

### Evaluation Metrics
- **GSM8K**: exact‑match accuracy on final numeric answer.
- **ARC‑Challenge**: multiple‑choice accuracy (letter match).
- **Response length**: average word count as a proxy for “effort.”

### Output Locations
- Raw outputs: `results/model_outputs/raw_outputs.jsonl`
- Accuracy summary: `results/evaluations/accuracy_summary.csv`
- Bootstrap CIs: `results/evaluations/diff_bootstrap_ci.csv`
- Length summary: `results/evaluations/length_summary.csv`
- Plots: `results/plots/`, `figures/`

## 5. Result Analysis

### Raw Results (Accuracy)
**GSM8K (n=50)**
| Condition | Accuracy |
|-----------|----------|
| direct-neutral | 0.52 |
| cot-neutral | 0.74 |
| critic-harsh | 0.40 |
| critic-harsh-lowbudget | 0.14 |
| rude-direct | 0.48 |
| polite-direct | 0.48 |

**ARC‑Challenge (n=50)**
| Condition | Accuracy |
|-----------|----------|
| direct-neutral | 0.88 |
| cot-neutral | 0.90 |
| critic-harsh | 0.32 |
| critic-harsh-lowbudget | 0.24 |
| rude-direct | 0.92 |
| polite-direct | 0.88 |

### Hypothesis Testing (Paired Bootstrap vs. direct-neutral)
**GSM8K**
- CoT: +0.22 (95% CI [0.08, 0.36])
- Harsh critic: −0.12 (95% CI [−0.26, 0.02])
- Harsh critic + low budget: −0.38 (95% CI [−0.52, −0.22])
- Rude vs direct: −0.04 (95% CI [−0.12, 0.04])
- Polite vs direct: −0.04 (95% CI [−0.12, 0.04])

**ARC‑Challenge**
- CoT: +0.02 (95% CI [−0.04, 0.08])
- Harsh critic: −0.56 (95% CI [−0.72, −0.40])
- Harsh critic + low budget: −0.64 (95% CI [−0.78, −0.50])
- Rude vs direct: +0.04 (95% CI [0.00, 0.10])
- Polite vs direct: 0.00 (95% CI [0.00, 0.00])

### Response Length (Avg words)
- **Direct prompts**: ~2 words (mostly “Final: X”).
- **CoT**: ~103–123 words (longer, but higher accuracy).
- **Harsh critic**: ~155–191 words (longer, but lower accuracy).
- **Harsh critic + low budget**: ~85–99 words (shorter, but lowest accuracy).

### Key Findings
1. **CoT improves GSM8K accuracy** substantially (+0.22 vs direct), and slightly improves ARC.
2. **Harsh‑critic prompting harms accuracy** on both datasets, especially with low budgets.
3. **Rudeness is not a reliable boost**; effects are near‑zero on GSM8K and small on ARC.
4. **Budget control reduces length but can significantly degrade accuracy** when paired with harsh critique.

### Visualizations
- Accuracy by condition: `results/plots/gsm8k_accuracy.png`, `results/plots/arc_accuracy.png`
- Question length distribution: `figures/question_length_hist.png`

### Surprises and Insights
- Critic prompting was expected to help; instead it consistently degraded performance, suggesting the critic‑revise loop may distract or introduce errors without strong external feedback.

### Error Analysis (Qualitative)
A cursory inspection suggests critic outputs sometimes introduce unnecessary changes, and low‑budget revisions frequently omit necessary steps. A deeper error taxonomy is a priority for follow‑up.

### Limitations
- **Sample size** limited to 50 per dataset due to API cost/time.
- **Single model** tested (gpt‑4.1). Results may not generalize to other models.
- **No self‑consistency or multi‑round self‑refine** due to cost.
- **No human preference evaluation** for perceived “laziness.”

## 6. Conclusions
Harsh‑critic prompting with budget control does **not** appear to fix “lazy” LLM outputs on GSM8K or ARC‑Challenge; it reduces accuracy despite longer responses. Standard CoT is a stronger, cheaper intervention. Rude tone provides no consistent benefit.

## 7. Next Steps
1. Test **self‑consistency** and **least‑to‑most** prompting on the same samples for stronger baselines.
2. Run **multi‑round self‑refine** (2–4 iterations) to check if iterative feedback recovers the critic‑prompt losses.
3. Add **LLM‑judge or human eval** for output quality beyond accuracy.
4. Expand to **anti‑shortcut datasets** from “Lazy Learners” for more direct laziness detection.

## References
- Tang et al. 2023 — *Large Language Models Can Be Lazy Learners: Analyze Shortcuts in In‑Context Learning*.
- Madaan et al. 2023 — *Self‑Refine: Iterative Refinement with Self‑Feedback*.
- Shinn et al. 2023 — *Reflexion: Language Agents with Verbal Reinforcement Learning*.
- Wang et al. 2022 — *Self‑Consistency Improves Chain of Thought Reasoning in Language Models*.
- Zhou et al. 2022 — *Least‑to‑Most Prompting Enables Complex Reasoning in LLMs*.
- Wei et al. 2022 — *Chain‑of‑Thought Prompting Elicits Reasoning in LLMs*.
- Wang et al. 2023 — *Self‑Critique Prompting with LLMs for Inductive Instructions*.
- Xie et al. 2023 — *Self‑Evaluation Guided Beam Search for Reasoning*.
