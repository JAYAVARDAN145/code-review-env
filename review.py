import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_UP"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_UP"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_UP"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_UP"
    },
]

async def review(code: str, language: str):
    """
    Review code using a large language model.
    """
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    chat = model.start_chat()
    gemini_response = await chat.send_message_async(
        f"Act as a code reviewer of a senior software engineer and review the following {language} code."
        f"Give feedback on the code with some code to implement the suggested changes."
        f"Make sure to follow the google python style guide if the language is python."
        f"The code is:\n\n{code}\n"
    )
    return {"response": gemini_response.text}
