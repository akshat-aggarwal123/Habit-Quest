from fastapi import APIRouter
from app.db.mongo import habit_collection
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

router = APIRouter()

@router.get("/recommend/{habit_title}")
def recommend_habits(habit_title: str):
    # Fetch habits
    habits = list(habit_collection.find({}, {"_id": 0, "title": 1, "tags": 1}))
    df = pd.DataFrame(habits)

    if df.empty:
        return {"error": "No habits found in database"}

    # Join tags
    df["tags_joined"] = df["tags"].apply(lambda x: " ".join(x))

    # TF-IDF + Cosine Similarity
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df["tags_joined"])

    idx = df[df["title"] == habit_title].index
    if idx.empty:
        return {"error": "Habit not found"}

    cosine_sim = cosine_similarity(tfidf_matrix[idx[0]], tfidf_matrix).flatten()
    df["similarity"] = cosine_sim

    # Sort by similarity and exclude the queried habit
    df_sorted = df[df["title"] != habit_title].sort_values(by="similarity", ascending=False)

    # Top 5 recommendations
    top_recommendations = df_sorted.head(5)[["title", "tags", "similarity"]].to_dict(orient="records")

    return top_recommendations
