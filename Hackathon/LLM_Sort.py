import pandas as pd
from fonction import llm_rank # hypothetical module for LLM-based ranking
import re
import json
# Load dataset
df = pd.read_csv("nyt_ai_subject_articles_2025.csv")

# For each article, combine headline + snippet for analysis
texts = (df['headline'] + ". " + df['snippet']).tolist()


# Step 3 & 4: For each description, rank reference documents using LLM
results = []
for description in texts:
    # Assume you have a function llm_rank(description, documents, top_k=2) 
    # that returns top_k references ranked by relevance
    top_refs = llm_rank(description)
    results.append({
        "description": description,
        "top_references": top_refs
    })
    
# Step 5: Save results

results_df = pd.DataFrame(results)
results_df['pub_date']=df['pub_date']
df=results_df.copy()
# Function to parse JSON string safely
def parse_json(json_str):
    try:
        # Replace doubled double quotes if any, and parse JSON
        cleaned = json_str.replace('""', '"')
        return json.loads(cleaned)
    except:
        return None

df["parsed"] = df["top_references"].apply(parse_json)

# Filter only articles about AI
df_ai = df[df["parsed"].apply(lambda x: x is not None and x.get("about_ai") == "Yes")]

# Extract sentiment and main_concern
df_ai["sentiment"] = df_ai["parsed"].apply(lambda x: x.get("sentiment"))
df_ai["main_concern"] = df_ai["parsed"].apply(lambda x: x.get("main_concern"))

# Drop the parsed column if not needed
df_ai = df_ai.drop(columns=["parsed"])

df_ai=df_ai[['description','sentiment','main_concern','pub_date']]
# Optionally save to CSV
df_ai.to_csv("filtered_ai_articles.csv", index=False)