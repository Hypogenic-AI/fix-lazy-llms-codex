# Planning: Fixing Lazy LLMs

## Motivation & Novelty Assessment

### Why This Research Matters
LLM outputs that appear “lazy” (shortcuts, shallow reasoning, or under-explained answers) reduce reliability in high‑stakes reasoning tasks and frustrate users who need thorough explanations. If lightweight prompting interventions can measurably improve reasoning quality without retraining, that provides a practical, low‑cost path to more dependable LLM behavior.

### Gap in Existing Work
Prior work demonstrates self‑critique/self‑refine and structured prompting can improve reasoning, and “lazy learner” shortcuts exist in in‑context learning. However, there is limited controlled evidence directly testing (a) critic harshness as a continuous intervention, and (b) explicit response‑budget control as a lever for effort/quality trade‑offs, across standard reasoning benchmarks.

### Our Novel Contribution
We test a controllable “harsh critic + budget control” prompting scheme and compare it to established baselines (direct, CoT, self‑consistency, least‑to‑most, self‑refine). We also evaluate the common belief that rudeness improves performance by isolating rude vs. neutral vs. polite framing, holding all other variables constant.

### Experiment Justification
- **Experiment 1 (Baselines)**: Establish floor/ceiling performance on GSM8K and ARC‑Challenge for direct, CoT, least‑to‑most, and self‑consistency prompting to anchor comparisons.
- **Experiment 2 (Harsh Critic + Budget Control)**: Test whether increasing critic severity and constraining response budgets improves answer quality and reduces shortcutting.
- **Experiment 3 (Rudeness vs. Politeness)**: Isolate tone effects to test the “rude helps” hypothesis under otherwise identical prompts.
- **Experiment 4 (Iterative Self‑Refine)**: Compare multi‑round critique/refine to single‑round harsh critic to test whether iterative feedback yields additional gains.
- **Experiment 5 (Robustness/Ablation)**: Vary temperature and max_tokens to check sensitivity; analyze failure cases for lazy‑style errors.

## Research Question
Do prompting interventions that increase critical self‑evaluation and control response budget reduce “lazy” LLM outputs and improve reasoning accuracy, compared to standard prompting baselines?

## Background and Motivation
LLMs often shortcut tasks by relying on shallow cues or minimal reasoning. Prior work on self‑refine and structured prompting suggests that explicit reasoning and critique can improve outcomes, but few studies test critic harshness and response budgets as controlled knobs. This study evaluates these interventions on standard reasoning benchmarks to clarify effectiveness and practical trade‑offs.

## Hypothesis Decomposition
- **H1**: Harsh‑critic prompting improves accuracy over direct and standard CoT baselines.
- **H2**: Constraining response budgets (max tokens, step limits) reduces verbosity without harming accuracy when paired with critique.
- **H3**: Rude framing alone does not consistently improve accuracy once other variables are controlled.
- **H4**: Iterative self‑refinement outperforms single‑round critique at the cost of higher latency/cost.

## Proposed Methodology

### Approach
Use real LLM APIs (GPT‑4.1 or GPT‑5) to run controlled prompt variants on GSM8K and ARC‑Challenge. Measure accuracy, cost, and output length. Compare baselines against critic/budget interventions and tone variations.

### Experimental Steps
1. **Dataset prep**: Load GSM8K and ARC‑Challenge from `datasets/`; create fixed evaluation splits (n=100–200 per dataset) with a random seed for reproducibility.
2. **Baseline prompting**: Direct answer (no reasoning), CoT, least‑to‑most, self‑consistency (k=3 samples). Rationale: establish standard effort‑elicitation baselines.
3. **Harsh critic + budget control**: Generate answer → critique (vary critic severity: mild/harsh) → revise; vary max_tokens for critique/revision. Rationale: isolate critic harshness and budget effects.
4. **Tone ablation**: Rude vs. neutral vs. polite framing for the same task and constraints. Rationale: test “rude helps” hypothesis.
5. **Iterative self‑refine**: Two refinement rounds; compare to single‑round critic. Rationale: test if extra iterations provide additional gains.
6. **Evaluation & stats**: Compute accuracy/EM and run paired tests vs. baselines; log cost, tokens, and latency.

### Baselines
- Direct answer (no CoT)
- Chain‑of‑Thought (few‑shot)
- Least‑to‑Most prompting
- Self‑Consistency (k=3)

### Evaluation Metrics
- **GSM8K**: exact‑match accuracy on final numeric answer
- **ARC‑Challenge**: multiple‑choice accuracy
- **Efficiency**: tokens per question, cost estimate
- **Length**: response length (tokens/words) as a proxy for “effort”

### Statistical Analysis Plan
- Paired bootstrap or McNemar’s test for accuracy differences (paired samples)
- Effect size: difference in accuracy with 95% bootstrap CI
- Significance level: α = 0.05 (Holm‑Bonferroni for multiple comparisons)

## Expected Outcomes
Support for the hypothesis would be: harsh‑critic + budget control improves accuracy or maintains accuracy with reduced verbosity; rudeness alone yields little or inconsistent gains; iterative self‑refine improves accuracy but increases cost.

## Timeline and Milestones
- **Phase 0–1**: Planning and setup (complete)
- **Phase 2**: Environment + data loading + prompt templates
- **Phase 3**: Implement evaluation harness
- **Phase 4**: Run experiments and collect outputs
- **Phase 5–6**: Analysis and reporting

## Potential Challenges
- API cost/latency; mitigate by limiting evaluation set size and caching outputs.
- Prompt leakage or unparseable outputs; mitigate with robust parsers and retries.
- Variance due to stochastic sampling; mitigate with fixed seeds and low temperature for accuracy eval.

## Success Criteria
- Statistically significant improvements for critic/budget interventions over direct baseline on at least one dataset.
- Clear evidence on rudeness effect (positive, null, or negative) with controlled conditions.
- Reproducible code and documented outputs in `results/` and REPORT.md.
