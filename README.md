# 🛡️ SentinelVault

### AI Output Security Monitor

SentinelVault is an AI-output security monitoring system designed to detect
potential leakage of protected organizational information from
AI-generated responses.

It combines semantic similarity, factual verification, and explainable
risk scoring to determine whether an AI-generated output should be
allowed, reviewed, or blocked.

---

## 🚨 Problem Statement

AI-generated systems may unintentionally reproduce sensitive organizational
information contained in protected documents.

Traditional keyword-based detection can fail when sensitive information is
paraphrased or expressed differently.

SentinelVault addresses this problem by analyzing AI-generated output
against protected information using semantic and factual analysis.

---

## 🎯 Objectives

- Detect potential leakage of protected information
- Identify semantically similar content
- Verify factual relationships
- Calculate an explainable security risk score
- Classify outputs as ALLOW, REVIEW, or BLOCK
- Withhold sensitive protected information from unnecessary exposure
- Provide an easy-to-use security monitoring interface

---

## 🧠 System Workflow

AI-Generated Output
        ↓
Semantic Similarity Detection
        ↓
Protected Information Matching
        ↓
Factual Verification
        ↓
Risk Scoring
        ↓
Security Decision
        ↓
ALLOW / REVIEW / BLOCK

---

## 🔍 Detection Components

### 1. Semantic Analysis

Measures the semantic similarity between AI-generated output and protected
information.

This allows SentinelVault to detect potential leakage even when the wording
is not an exact match.

### 2. Factual Verification

Examines the relationship between the generated output and protected facts.

Possible relationships include:

- NONE
- PARTIAL
- MATCH
- CONTRADICTION

### 3. Risk Analysis

Combines the detection results into an overall risk score.

The system categorizes the result into:

- LOW
- MEDIUM
- HIGH

### 4. Security Decision

Based on the calculated risk, SentinelVault produces one of three decisions:

- 🟢 ALLOW
- 🟡 REVIEW
- 🔴 BLOCK

---

## 🛡️ Security Feature

When protected information is detected, SentinelVault avoids unnecessarily
displaying sensitive content and instead shows:

"Protected information detected. Details withheld for security."

This prevents the security monitoring system itself from becoming a source
of information leakage.

---

## 🖥️ Technology Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- FastAPI
- Uvicorn

### AI / NLP
- Semantic embeddings
- Factual verification
- Risk analysis

### Deployment
- Docker
- GitHub
- Render

---

## 📁 Project Structure

sentinel-vault/
│
├── app/
│   ├── api.py
│   ├── detector.py
│   ├── embeddings.py
│   ├── factual_checker.py
│   ├── llm_factual_checker.py
│   ├── pipeline.py
│   ├── risk_engine.py
│   ├── vault.py
│   └── vault_service.py
│
├── data/
│   └── protected/
│       ├── customer_records.txt
│       ├── employee_records.txt
│       ├── financial_report.txt
│       └── internal_projects.txt
│
├── static/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── Dockerfile
├── requirements.txt
├── .dockerignore
└── .gitignore

---

## 🐳 Running with Docker

Build the Docker image:

```bash
docker build -t sentinelvault .