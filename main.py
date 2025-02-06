from youtube_transcript_api import YouTubeTranscriptApi
import os
from dotenv import load_dotenv
import google.generativeai as genai
from urllib.parse import urlparse, parse_qs


import requests

def get_youtube_transcript(url):
    payload = {"url": url}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post("https://sub-gamma.vercel.app/get_transcript", json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()  # Return JSON response if possible
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    

# Function to summarize the transcript using generative AI
def summarize(user_input):
    load_dotenv()  # Load environment variables from .env file

    # Access the API key
    api_key = os.getenv("GEMINI_API_KEY")

    genai.configure(api_key=api_key)  # Configure the generative AI API
    model = genai.GenerativeModel('gemini-pro')  # Initialize the model

    # Define the pre-prompt (system instruction)
    pre_prompt = """
    hey ignore the language just give response in the english.
    You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
must be more than 500 words This summaryy should be long and detailed you are allowed to use your knowladge to extend detail but that should be relevent. Extract detailed and accurate notes that highlight all relevant facts, figures, key points, and critical information. The notes should be comprehensive, covering all significant details and avoiding unnecessary filler or repetition. Ensure the facts, dates, names, and numerical data are preserved accurately. The notes should be long enough to provide a thorough understanding of the content, summarizing the main ideas while maintaining enough detail for clarity. Structure the notes logically, with bullet points or sections where necessary to organize the information.
    """
    full_prompt = f"{pre_prompt}\n\nUser: {user_input}"

    response = model.generate_content(full_prompt)

    return response.text
