# Movie Script Classification and Generation

This project studies movie scripts as a large-scale **NLP** problem, covering **genre classification**, **text generation**, and corpus-level analysis on a dataset of more than **37k scripts**.

## What This Project Demonstrates

- End-to-end work on long-form text data: preprocessing, analysis, modeling and evaluation
- Comparison of **classical ML**, **feed-forward neural networks**, **RNNs** and **Transformers**
- Both **multi-class** and **multi-label** genre prediction
- Benchmarking of generation approaches from n-grams to fine-tuned GPT-2 models
- Clear reporting of results, limitations and future directions

## Main Results

- Best **multi-class accuracy**: **77%**
- Best **multi-label F1-score**: **70%**
- **GPT-2 based** models produced the strongest generation metrics among the tested approaches

## Repository Structure

```text
Movie-Script-Classification-and-Generation/
â”œâ”€â”€ scripts/               # Training and data-processing utilities
â”œâ”€â”€ project/               # Experimentation code and notebooks
â”œâ”€â”€ img/                   # Figures used in the analysis
â”œâ”€â”€ data/                  # Dataset-related assets
â”œâ”€â”€ Report_NLP.pdf         # Detailed report in English
â”œâ”€â”€ Rapport_NLP.pdf        # Detailed report in French
â”œâ”€â”€ requirements.txt       # Python dependencies
â””â”€â”€ README.md
```

## Dataset

The experiments are based on the Kaggle dataset **40k movie scripts from Springfield Springfield**, enriched with IMDb genre metadata and synopses when available.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The repository keeps both the implementation code and the full project reports. The reports are the best place to inspect the detailed experimental protocol, metrics and discussion.

## Technical Scope

The project includes work on:

- script preprocessing and exploratory analysis
- class imbalance handling
- unigram / TF-IDF / Word2Vec / Doc2Vec pipelines
- supervised multi-class and multi-label classification
- unsupervised clustering experiments
- text generation with n-grams, FFNNs, RNNs and Transformers

## Why This Repo Matters

This repository shows the ability to:

- work on a non-trivial NLP dataset at scale
- compare multiple modeling families rigorously
- communicate results clearly with proper reports and figures
- connect research-style experimentation with implementation details

