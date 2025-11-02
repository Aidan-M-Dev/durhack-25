import google.generativeai as genai
from enum import Enum
import os

MODEL_ID = "gemini-2.5-flash-lite"

f = open("sentiment_analysis_prompt.txt", "r")
master_prompt = f.read()
f.close()

def sentiment_review(text):
    full_prompt = master_prompt + text
    count = 0
    while count < 3:
        response = query(full_prompt)
        if response == "Yes":
            return True
        elif response == "No":
            return False
        count += 1
    raise Exception("Gen AI not raising binary answers.")

def query(prompt):
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel(MODEL_ID)
    response = model.generate_content(prompt)
    return response.text


def notify_admins_of_reported_review(review_id):
    """
    Skeleton function to notify admins of a reported review.

    Args:
        review_id (int): The review ID
    """
    # TODO: Implement admin notification system
    # This could send emails, create notifications in admin panel, etc.
    print(f"ADMIN NOTIFICATION: Review {review_id} has been reported and requires moderation")
    pass