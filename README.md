## Understanding the Issue Types in Open Source Blockchain-based Software Projects with the Transformer-based BERTopic

This repository contains the code, dataset, topic modeling models, and experimental outputs of the above research.

---

## 📌 Overview

We conduct a large-scale empirical study of **497,742 GitHub issues** mined from **1,209 blockchain-related repositories**. Using the transformer-based **BERTopic** model, we extract **49 semantically coherent topics**, organize them into a **hierarchical structure** of **11 major subcategories**, and analyze their **temporal trends** and **resolution times**.

This repository shares everything needed to **replicate**, **extend**, or **reuse** our study.

---

## 📁 Dataset
The dataset is built from two sources:
1. We reused dataset from a prior study [Das et al.](https://github.com/disa-lab/BlockchainEmpiricalEASE2022) on blockchain repositories.
2. Extended the dataset by adding issues from repositories created post 2021.

The `Data/` directory contains all the issue-level and repository-level data used for topic modeling and analysis. Below is a description of each key file:

```text
Data/
├── AllIssues.csv
├── AllIssues-New.csv
├── AllIssues-Old-Actives.csv
├── BlockchainAppRepositories-New.csv
├── BlockchainAppRepositories-Old-Actives.csv
```

🔹 Issue Files
AllIssues.csv
→ The full dataset of around half a million issues used in our study.
This file combines:

Issues from the Das et al. study

Issues from newly collected repositories (post-2021)

AllIssues-New.csv
→ Contains issues mined from newly added repositories that were not included in the Das et al. dataset.
These repositories were identified using a GitHub keyword search and filtered based on activity, relevance, and popularity.

AllIssues-Old-Actives.csv
→ Contains issues from the active subset of repositories originally included in the Das et al. dataset.
Inactive or archived projects were removed during filtering.

🔹 Repository Files
BlockchainAppRepositories-New.csv
→ Newly added GitHub Repository information (post-2021), filtered using keyword queries, GitHub REST API, and manual verification.

BlockchainAppRepositories-Old-Actives.csv
→ Filtered list of active blockchain repositories retained from the original Das et al. dataset.
This includes only those projects that met our criteria for activeness and relevance.


## 🧠 Topic Modeling

The topic modeling workflow is implemented in **`TopicModeling.ipynb`** using the BERTopic framework.

### 🔹 Key Steps:
- **Input**: Cleaned issue titles from `AllIssues.csv`
- **Embeddings**: Generated using `all-mpnet-base-v2` from SentenceTransformers
- **Dimensionality Reduction**: UMAP (100 dimensions)
- **Clustering**: HDBSCAN (min cluster size = 1000)
- **Topic Representation**: c-TF-IDF + Maximal Marginal Relevance (MMR)
- **Output**: 49 topics saved to `model/Topics-BERTopic/`


## 📊 Research Analysis

The notebook **`RQs.ipynb`** contains the analysis and visualizations that answer the study’s three core research questions.

### 🎯 Research Questions

- **RQ1: What are the key issue categories in blockchain projects as identified through topic analysis?**  
  → 49 BERTopic-generated topics are grouped into 11 subcategories using open card sorting.

- **RQ2: How do resolution times vary across different subcategories of issues?**  
  → Wallet-related issues show the longest resolution times, while mechanism-related ones are resolved the fastest.

- **RQ3: How have different types of issues evolved over time in terms of frequency?**  
  → Temporal analysis shows a spike in issue reports post-2016 (rise of Ethereum) and a decline after 2022.


## 🗃️ Git Large File Storage (LFS)

This project uses **Git Large File Storage (LFS)** to manage large CSVs.

### 🔧 Setup Instructions

#### Windows
1. Download and install Git LFS from [https://git-lfs.com](https://git-lfs.com)
2. Run in terminal:
   ```bash
   git lfs install

## ⚙️ Prerequisites

Before running the notebooks or collecting data, ensure the following setup:

### 🐍 Python
- Python **3.8** is recommended.

### 📦 Install Dependencies
Install required Python packages:
```bash
pip install -r requirements.txt

```
### 🔐 GitHub Access Token

To collect GitHub issues or extend the dataset:

1. Create a file named `config.json` in the root directory.
2. Add your GitHub personal access token in the following format:

```json
{
    "access_token": "your_github_access_token"
}
