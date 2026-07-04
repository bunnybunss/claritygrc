# ClarityGRC

AI Governance & Compliance Assessment Tool for the European market.

ClarityGRC assesses AI systems against 6 European regulatory frameworks and delivers structured compliance reports — free, instant, built on real frameworks.

## Frameworks Covered

- **EU AI Act** — risk classification across 4 levels: unacceptable, high, limited, minimal
- **GDPR** — data protection obligations, DPIA requirements, individual rights
- **NIS2** — cybersecurity obligations for essential and important entities
- **DORA** — digital operational resilience for financial sector entities
- **ISO 27001** — information security controls mapped to risk profile
- **ISO 42001** — AI management system controls for responsible AI deployment

## Features

- 4-step assessment form with sector and size classification
- Visual compliance risk gauge (0-100 score)
- AI plain English explainer powered by Groq/Llama
- PDF compliance report download
- Statement of Applicability (SoA) export
- Versioned assessment history with permanent links
- SQLite-backed assessment storage

## Tech Stack

Python · Flask · SQLite · ReportLab · Groq API · HTML · CSS · JavaScript

## How to Run Locally

```bash
git clone https://github.com/bunnybunss/claritygrc.git
cd claritygrc
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Add your Groq API key to a `.env` file:

GROQ_API_KEY=your_key_here

Then open `http://127.0.0.1:5000`

## Built By

Aya Hadri — Master's student in Computer Science & Technology at Harbin Institute of Technology Shenzhen. Built as a portfolio project for GRC and AI Governance roles in the European market.

[LinkedIn](https://linkedin.com/in/aya-hadri)
