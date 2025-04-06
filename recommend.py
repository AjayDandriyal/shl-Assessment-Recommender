import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
import os

# Load Gemini API key
genai.configure(api_key=os.getenv("gemini-2.5-pro-exp-03-25"))

# Load and prepare data
df = pd.read_csv("data/shl_assessments.csv")
df["text_blob"] = df["Assessment Name"].fillna("") + " " + \
                  df["Test Type"].fillna("") + " " + \
                  df["Duration"].fillna("")

# Fit TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["text_blob"])


def rerank_with_gemini(query, candidates_df):
    items_text = "\n".join([
        f"{i+1}. {row['Assessment Name']} - {row['Test Type']} - {row['Duration']}"
        for i, row in candidates_df.iterrows()
    ])

    prompt = f"""
You are an expert in recommending assessments to users.

User query: "{query}"

Here are 10 candidate assessments:
{items_text}

Please return the numbers of the most relevant assessments ordered by relevance. 
Return a valid Python list, e.g. [3, 1, 5, ...]
    """

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        ranked_indices = eval(response.text.strip())
    except Exception as e:
        print("Gemini reranking failed, falling back to original order:", e)
        ranked_indices = list(range(1, len(candidates_df) + 1))

    reranked = candidates_df.iloc[[i - 1 for i in ranked_indices]].copy()
    reranked["Score"] = [round(1 - 0.05 * i, 2) for i in range(len(reranked))]
    return reranked[[  # Same format
        "Assessment Name", "URL", "Remote Testing Support",
        "Adaptive/IRT Support", "Duration", "Test Type", "Score"
    ]]


def recommend_assessments(query, top_n=10):
    query_vec = vectorizer.transform([query])
    similarity_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    
    top_indices = similarity_scores.argsort()[::-1][:top_n]
    candidates = df.loc[top_indices].copy()
    return rerank_with_gemini(query, candidates)


if __name__ == "__main__":
    q = "data warehouse"
    results = recommend_assessments(q)
    print(results)
