
import os
import json
import openai
from openai import OpenAI
from rake_nltk import Rake

from dotenv import load_dotenv 
load_dotenv()  

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_completion(system_prompt: str) -> str :
    """ Function takes in a list of messages in openai format and returns openai text response"""
    messages = [ { "role": "system", "content": system_prompt  } ]
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        return response.choices[0].message.content
    except openai.APIError as e:
        return (f"OpenAI API returned an API Error: {e}")

def get_image(question_text: str) -> str:
    """takes a list of keywords, uses DAL-E to generate an image
     and returns an image URL"""


    prompt = f"Generate an image that represents this sentence: {question_text}. \
                Image is for educational purposes. There should be NO TEXT in the image\
            Exclude any text that does not adhere to ethical guidelines\
            and avoids any inappropriate or offensive material."
    try:
        response = client.images.generate(
                                        model="dall-e-2",
                                        prompt=prompt,
                                        size="256x256",
                                        quality="standard",
                                        n=1,
                                        )
        return response.data[0].url

    except openai.APIError as e:
        return (f"OpenAI API returned an API Error: {e}")

def get_keywords(text_prompt: str) -> list:
    """ Takes a text string and extracts keywords 
        Returns a list of keywords"""
    r = Rake()
    r.extract_keywords_from_text(text_prompt)
    keywords = r.get_ranked_phrases()
    return keywords

def q_n_a_validation(ques, ans):
    """ Takes a question and an answer. 
    Checks if the answer is appropriate for the question
    Return true if yes, otherwise returns false"""

    prompt = f"Here is a question: ```{ques}```, here is its answer: ```{ans}```.\
             Return 'True' if the answer is adequate and \
            return 'False' if it is not. Do not give any other detail. Answer in [True, False] only"

    response = get_completion(prompt)

    if response.lower() == 'true':
        return True
    else:
        return False

def is_json(json_str):
    """Recieves a json string
        checks if it is valid JSON, returns True
        returns false if not valid json"""

    try:
        json.loads(json_str)
    except ValueError:
        return False
    return True
