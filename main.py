import json, random
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

#Load ICP (Input)

def load_icp(file_path):
    with open(file_path, "r") as f:
        return json.load(f)
    
# Step 2: Mock API Fetchers

def fetch_from_apollo(icp):
    # Simulate fetching companies
    return [
        {"company_name": "DataIQ Inc", "domain": "dataiq.com",
         "revenue": 75000000, "industry": "Software",
         "employee_count": 200,
         "contacts": [{"name": "Sarah Green", "title": "VP Data Science",
                       "email": "sarah@dataiq.com", "linkedin": "linkedin.com/in/sarahgreen"}],
         "signals": {"new_funding": True}, "source": ["Apollo"]},
        {"company_name": "FinWise Tech", "domain": "finwise.ai",
         "revenue": 40000000, "industry": "FinTech",
         "employee_count": 150,
         "contacts": [{"name": "David Miller", "title": "Head of AI",
                       "email": "david@finwise.ai", "linkedin": "linkedin.com/in/davidm"}],
         "signals": {"new_funding": False}, "source": ["Apollo"]}
    ]

def fetch_from_crunchbase(icp):
    # Simulate company funding data
    return [
        {"company_name": "DataIQ Inc", "domain": "dataiq.com",
         "funding_stage": "Series B", "signals": {"recent_hiring": True},
         "source": ["Crunchbase"]},
        {"company_name": "AutoAI Corp", "domain": "autoai.com",
         "funding_stage": "Seed", "signals": {"recent_hiring": False},
         "source": ["Crunchbase"]}
    ]



load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def fetch_from_serpapi(icp):
    print("🔍 Fetching job signals from SerpAPI...")

    companies = []
    for keyword in icp["keywords"]:
        params = {
            "engine": "google_jobs",
            "q": f"{keyword} data jobs in USA",
            "api_key": SERPAPI_KEY
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        # Extract job titles and companies
        jobs = results.get("jobs_results", [])
        for job in jobs[:3]:  # limit for demo
            companies.append({
                "company_name": job.get("company_name"),
                "domain": "",
                "signals": {"recent_hiring": True},
                "source": ["SerpAPI"]
            })

    print(f"✅ Found {len(companies)} hiring signals from SerpAPI.")
    return companies


def merge_results(*sources):
    combined = {}
    for src in sources:
        for comp in src:
            domain = comp["domain"]
            if domain not in combined:
                combined[domain] = comp
            else:
                # merge signals & sources
                combined[domain]["signals"].update(comp.get("signals", {}))
                combined[domain]["source"] = list(set(combined[domain]["source"] + comp.get("source", [])))
                # merge funding_stage if missing
                if "funding_stage" in comp:
                    combined[domain]["funding_stage"] = comp["funding_stage"]
    return list(combined.values())


def compute_confidence(company, icp):
    industry_match = 1 if any(ind.lower() in company.get("industry", "").lower()
                              for ind in icp.get("industry", [])) else 0
    funding_signal = 1 if company.get("signals", {}).get("new_funding") else 0
    hiring_signal = 1 if company.get("signals", {}).get("recent_hiring") else 0
    tech_match = 1 if any(t in " ".join(icp["signals"]["tech_stack"])
                          for t in ["AWS", "Snowflake"]) else 0
    score = 0.4*industry_match + 0.3*funding_signal + 0.2*hiring_signal + 0.1*tech_match
    return round(score, 2)

# Save Output JSON

def save_output(results, file_path="output.json"):
    with open(file_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Output saved to {file_path}")

# Main Flow

def main():
    print("🚀 Prospect Search Agent Starting...\n")
    icp = load_icp("icp.json")

    apollo_data = fetch_from_apollo(icp)
    crunch_data = fetch_from_crunchbase(icp)
    serp_data = fetch_from_serpapi(icp)

    merged = merge_results(apollo_data, crunch_data, serp_data)
    for comp in merged:
        comp["confidence"] = compute_confidence(comp, icp)

    save_output(merged)
    print("\n🎯 Found", len(merged), "companies:")
    for c in merged:
        print("-", c["company_name"], ":", c["confidence"])

if __name__ == "__main__":
    main()
