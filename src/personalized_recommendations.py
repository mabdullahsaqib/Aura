import firebase_admin
from firebase_admin import credentials, firestore
import google.generativeai as genai
from datetime import datetime, timedelta
from config import FIREBASE_CREDENTIALS_PATH, GEMINI_API_KEY
import random
from weather_and_news import get_news

# Initialize Firestore
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Gemini model
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Example categories for recommendations
INTEREST_CATEGORIES = ["technology", "health", "entertainment", "business", "sports"]

# Store user preferences
def update_preferences(user_id, preference_type, preference):
    doc_ref = db.collection("user_preferences").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.update({preference_type: preference})
    else:
        doc_ref.set({preference_type: preference})

# Fetch user preferences
def fetch_preferences(user_id):
    doc_ref = db.collection("user_preferences").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return {}

# Recommend news based on preferences
def recommend_news(user_id):
    preferences = fetch_preferences(user_id)
    news_category = preferences.get("news_category", random.choice(INTEREST_CATEGORIES))
    return get_news(category=news_category)

# Recommend tasks based on user's activity
def recommend_tasks(user_id):
    doc_ref = db.collection("tasks").where("user_id", "==", user_id).stream()
    tasks = [doc.to_dict() for doc in doc_ref]

    # Filter high-priority or urgent tasks
    recommended_tasks = [
        task for task in tasks if task.get("priority") == "high" or
                                  (task.get("deadline") and datetime.strptime(task["deadline"],
                                                                              "%Y-%m-%d %H:%M") < datetime.now() + timedelta(
                                      days=1))
    ]
    return recommended_tasks if recommended_tasks else ["No urgent tasks!"]

# Recommend general activities (e.g., personalized greetings)
def general_recommendations(user_id):
    preferences = fetch_preferences(user_id)
    if not preferences:
        return "Welcome! Set some preferences to get personalized recommendations."

    # Example greeting based on weather interest
    if "weather_updates" in preferences and preferences["weather_updates"]:
        return "Would you like the latest weather update?"

    # Use Gemini to suggest personalized recommendations
    try:
        response = model.generate_content(f"User preferences are: {preferences}. Suggest some activities or recommendations, don't ask any questions.")
        gemini_recommendation = response.text
    except Exception as e:
        gemini_recommendation = f"Could not generate recommendation due to an error: {e}"

    return gemini_recommendation

# Example usage
if __name__ == "__main__":
    user_id = "example_user"

    # Set preferences
    update_preferences(user_id, "news_category", "technology")
    update_preferences(user_id, "weather_updates", True)

    # Recommend based on preferences
    news = recommend_news(user_id)
    tasks = recommend_tasks(user_id)
    greeting = general_recommendations(user_id)

    print("News Recommendation:", news)
    print("Task Recommendation:", tasks)
    print("Gemini Recommendation:", greeting)
