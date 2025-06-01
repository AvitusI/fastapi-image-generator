import asyncio
import re
from typing import List

from cohere import AsyncClient, ChatMessage
from cohere.core.api_error import ApiError

from config import BaseConfig

from message import SYSTEM_MESSAGE


settings = BaseConfig()

COHERE_API_KEY = settings.COHERE_API_KEY

"""
SYSTEM_MESSAGE = (
    ""
    You are an assistant helping to craft prompts which will be sent to the Flux model to
    generate high quality images. You will be given a topic to generate image about. Make
    sure you craft two separate not too long prompts.The prompts should be numbered. 
    The prompts should be well crafted for the Flux model to generate compelling images. 
    The result should only contain the prompts, do not add any other word. Make sure the
    prompts make the model to generate more scenery features.
    ""
)
"""

client = AsyncClient(api_key=COHERE_API_KEY)

# prompt = "Kuzidisha kuzidisha 56 na 7"

async def generate_image_prompt(
     topic: str,
#    topic = prompt,
    messages=[]
) -> List[str]:
    try:
        response = await client.chat(
            message=topic,
            model="command-r-plus",
            preamble=SYSTEM_MESSAGE,
            chat_history=messages
        )

        messages.extend(
            [
                ChatMessage(
                    role="USER",
                    message=topic
                ),
                ChatMessage(
                    role="CHATBOT",
                    message=response.text
                )
            ]
        )
        
        prompts = (
            # [re.sub(r"[^a-zA-Z0-9\s,]", "", response.text.strip())]
            [response.text.strip()]
            if "*" not in response.text
            else [
                re.sub(r"[^a-zA-Z\s]", "", prompt.strip())
                for prompt in response.text.split("*")
                if prompt.strip()
            ]
        )

        print("text", response.text)

        # matches = re.findall(r"\d+ \w+", response.text)
        # print('matches', matches)

        return prompts
    
    except ApiError as e:
        return "An error occured"
    

def get_number_prompt(number_str: str):
    colors = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "black", "white", "gray"]
    groups = ["MAMOJA", "MAKUMI", "MAMIA", "MAELFU"]

    # removing any word from the string("namba" in this case)
    new_number_str = re.sub(r'^\D+\s', '', number_str)
    new_number_str = new_number_str.replace(',', '').strip()

    # Ensure no extra spaces or invalid characters
    new_number_str = ''.join(filter(str.isdigit, new_number_str))

    numbers = list(map(int, new_number_str))
    print(numbers)

    result = []

    for i, digit in enumerate(numbers):
        group = groups[len(numbers) - i - 1] if len(numbers) - i - 1 < len(groups) else "MAELFU"
        
        if digit == 0:
            result.append(f"a word \"{group}\" written in black on a white background namba")
        else:
            color = colors[i % len(colors)]
            ball_word = "ball" if digit == 1 else "balls"

            if digit > 5:
                result.append(f"5 {color} {ball_word} horizontally aligned on a white background, the word \"{group}\" written in black at the very top of the image namba")
                result.append(f"{digit - 5} {color} {ball_word} horizontally aligned on a white background, the word \"{group}\" written in black at the very top of the image namba")
            else:
                result.append(f"{digit} {color} {ball_word} horizontally aligned on a white background, the word \"{group}\" written in black at the very top of the image namba")

    return result

def get_disease_prompt(disease_str: str):
    pass

if __name__ == "__main__":
    result = asyncio.run(generate_image_prompt())
    print(result)