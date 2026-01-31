# Downloaded Datasets

This directory contains datasets for the research project. Data files are NOT
committed to git due to size. Follow the download instructions below.

## Dataset 1: GSM8K

### Overview
- **Source**: HuggingFace dataset `gsm8k` (config: `main`)
- **Size**: 7,473 train / 1,319 test (≈2.8 MB on disk)
- **Format**: HuggingFace Dataset
- **Task**: Grade-school math reasoning
- **Splits**: train, test
- **License**: Not verified (see dataset card)

### Download Instructions

**Using HuggingFace (recommended):**
```python
from datasets import load_dataset

dataset = load_dataset("gsm8k", "main")
dataset.save_to_disk("datasets/gsm8k")
```

### Loading the Dataset
```python
from datasets import load_from_disk

dataset = load_from_disk("datasets/gsm8k")
print(dataset["train"][0])
```

### Sample Data
Samples saved in `datasets/gsm8k/samples/sample.json`.

### Notes
- Common benchmark for chain-of-thought and self-refinement methods.

---

## Dataset 2: AI2 ARC (ARC-Challenge)

### Overview
- **Source**: HuggingFace dataset `ai2_arc` (config: `ARC-Challenge`)
- **Size**: 1,119 train / 299 validation / 1,172 test (≈600 KB on disk)
- **Format**: HuggingFace Dataset
- **Task**: Multiple-choice science reasoning
- **Splits**: train, validation, test
- **License**: Not verified (see dataset card)

### Download Instructions

**Using HuggingFace (recommended):**
```python
from datasets import load_dataset

dataset = load_dataset("ai2_arc", "ARC-Challenge")
dataset.save_to_disk("datasets/ai2_arc")
```

### Loading the Dataset
```python
from datasets import load_from_disk

dataset = load_from_disk("datasets/ai2_arc")
print(dataset["train"][0])
```

### Sample Data
Samples saved in `datasets/ai2_arc/samples/sample.json`.

### Notes
- ARC-Challenge is commonly used for reasoning and robustness evaluation.
