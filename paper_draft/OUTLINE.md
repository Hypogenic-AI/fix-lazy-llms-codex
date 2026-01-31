# Outline: Fixing Lazy LLMs

## Title
- Emphasize main finding: harsh-critic + budget control hurts accuracy; CoT helps.

## Abstract
- Problem: lazy/low-effort outputs in LLM reasoning.
- Gap: limited controlled evidence on critic harshness + budget control.
- Approach: prompt variants on GSM8K/ARC-Challenge with fixed model/decoding.
- Results: CoT improves GSM8K (+0.22), harsh-critic degrades; tone minimal effect.
- Significance: simple harsh-critic prompts are not reliable fixes.

## Introduction
- Hook: prompting is the cheapest lever for reasoning quality.
- Importance: lazy outputs reduce reliability.
- Gap: controlled tests of critic severity and budget control are scarce.
- Approach: compare direct, CoT, harsh-critic, harsh+budget, rude/polite.
- Quant preview: GSM8K +0.22 for CoT; harsh+budget -0.38; ARC harsh -0.56.
- Contributions (3-4 bullets).

## Related Work (themes)
- Effort-inducing prompting: CoT, least-to-most.
- Multi-sample / decoding control: self-consistency, self-eval guided beam.
- Self-critique/refinement: Self-Refine, Reflexion, dual-critique prompting.
- Lazy learner evidence: Tang et al. 2023.

## Methodology
- Problem setup + task definition.
- Datasets: GSM8K, ARC-Challenge; sampling n=50; preprocessing.
- Prompt conditions (6).
- Model: GPT-4.1; temperature 0; max tokens 256/128.
- Metrics: accuracy (EM, MC), response length.
- Statistical test: paired bootstrap CIs vs direct.

## Results
- Table: accuracy by condition per dataset.
- Table: diff vs direct with CIs.
- Figures: accuracy plots; question length histogram.
- Text: CoT gains; harsh-critic and low budget losses; tone near-zero; length tradeoffs.

## Discussion
- Interpretation: critic prompts without external signal can distract; budget constraints harm.
- Limitations: n=50, single model, no multi-round refine, no human eval.
- Broader implications: cheap prompts should be validated; caution on "rude helps".

## Conclusion
- Summarize findings; key takeaway.
- Future work: self-consistency, least-to-most, multi-round self-refine, human eval.

## Figures/Tables
- tables/accuracy_main.tex
- tables/diff_ci.tex
- figures/gsm8k_accuracy.png
- figures/arc_accuracy.png
- figures/question_length_hist.png

## Citations Needed
- Tang et al. 2023; Madaan et al. 2023; Shinn et al. 2023;
- Wang et al. 2022 (Self-Consistency); Zhou et al. 2022; Wei et al. 2022;
- Wang et al. 2023 (dual-critique); Xie et al. 2023.
