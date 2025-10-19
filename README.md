# ProspectSearchAgent

An AI-powered agent that finds B2B companies matching an **Ideal Customer Profile (ICP)**.

### 🧠 Project Overview
- Reads input from `icp.json` (industry, keywords, tech stack, revenue filters).
- Fetches company data from:
  - 🏢 Apollo (mock)
  - 💰 Crunchbase (mock)
  - 🔍 SerpAPI (real Google Jobs API)
- Merges all sources, removes duplicates, and assigns confidence scores.

### ⚙️ How to Run
```bash
python main.py
