# step 1 = import API key 
import os
import getpass
from dotenv import load_dotenv
import google.generativeai as genai
import PIL.Image
import requests
from io import BytesIO
import base64


load_dotenv()
"""
the genai.configure() is conventional. However, the
api-key = os.getenv("GOOGLE_API_KEY") is the taking
from the .env file
Return:
    the api_key.
"""
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key")
#step 2 = get the prompt to take in an image and tell what it does
# model = genai.GenerativeModel(model_name="gemini-1.5-pro")
# prompt = "Describe the image"
image_url = "https://www.pexels.com/photo/dirt-road-in-colorful-forest-17874811/"
# content = requests.get(image_url).content
image = PIL.Image.open(image_url)
buffered = BytesIO()
image.save(buffered, format="JPEG")
img_bytes = buffered.getvalue()
img_base64 = base64.b64encode(img_bytes).decode('utf-8')
# PIL.Image(content)
# prompt_image = PIL.Image.open('public/images/image1.jpg')
# prompt = "Give a detailed description of what you find on the images"

# response = model.generate_content([prompt, prompt_image])

# print(response.text + "\n" + "Next to Langchain")


#attempting to use langchain
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI


llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
message = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "Give a detailed description of what you find on the images",
        },
        {
            "type": "image_url",
            "image_url": image_url,
        }
    ]
)
llm.invoke([message])