import os
import time
from dotenv import load_dotenv
import requests
from PIL import Image
import io
import google.generativeai as genai
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted, InternalServerError

load_dotenv()

# Check if the API key is being loaded correctly
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    print("API key loaded successfully.")
else:
    print("Failed to load API key.")

# Configure genai with the API key from the .env file
genai.configure(api_key=api_key)

# Fetch the image content from the URL
# image_url = "public/images/image1.jpg"
# content = requests.get(image_url).content

# Open the image using PIL
# image = Image.open(io.BytesIO(content))

# Configure the language model
llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")

# Create the message with correct formatting
message = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "What is in the image?",
        },
        {
            "type": "image_url",
            "image_url": "public/images/image1.jpg",
        }
    ]
)

# Function to call the API with retries
def invoke_with_retries(llm, messages, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            response = llm.invoke(messages)
            return response.content
        except (ResourceExhausted, InternalServerError) as e:
            retries += 1
            wait_time = 2 ** retries
            print(f"Error: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    print("Max retries reached. Please check your API quota or report the issue.")
    return None

# Invoke the language model with retries
response = invoke_with_retries(llm, [message])
if response:
    print(response)
else:
    print("Failed to get a response from the API.")
