import asyncio
import re

from langchain_aws import ChatBedrock
from langchain.schema import StrOutputParser

from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)


template: str = """
    You are an assistant helping to craft text prompts which are to be fed into the image generation model.
    You will be given a topic along with a short image description in Swahili. Transform the description into 
    a long English prompt suitable for image generation. Find the matching topic below and follow 
    instructions on the given matching topic. The user requested the image of topic {topic} with description {description}.
    
    Topic 1. (Dhana ya maada). This topic describes the states of matter. Preceed the prompt you generated with the 
    word "dmaa". Only output the generated prompt and the given word and not any other word.

    *********

    Topic 2. (Namba nzima). 
    This topic talks about numbers. 
    You will only receive a set of numbers as description, for example 4325. 
    Break the number into individual numbers, e.g for our case: 4, 3, 2, and 5. 
    For each individual number, write a prompt which describes number of fruits totalling that number. 
    For example, "four yellow oranges on a table", "three green bananas on a table", "two red apples on a table", "five mangoes on a table". 
    Separate those individual prompts with a "*". 
    Don't include the word "dmaa" here. Don't include the "*" before the first prompt and after the last prompt. 
    Don't include the given numbers only write the prompts.
    FOLLOW THE ORDER PLEASE, start from the right digit and proceed to the left.
    """


system_message_prompt = SystemMessagePromptTemplate.from_template(
    template
)

human_message_prompt = HumanMessagePromptTemplate.from_template(
    template="{topic}"
)

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        system_message_prompt,
        human_message_prompt
    ]
)

model = ChatBedrock(
  # model_id="anthropic.claude-3-haiku-20240307-v1:0",
    model_id="us.meta.llama3-2-3b-instruct-v1:0",
    region="us-west-2",
    aws_access_key_id="AKIAT7JJU2YBJ2JM4O35",
    aws_secret_access_key="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"
    # model_kwargs=dict(temperature=0),
)

# history = InMemoryChatMessageHistory()

chain = chat_prompt_template | model | StrOutputParser()


topic = "Namba nzima"

description = "1111"


async def generate_prompt():
    response = await chain.ainvoke(
        {
            "topic": topic,
            "description": description
        }
    )
    return response


if __name__ == "__main__":
    result = asyncio.run(generate_prompt())
    print(result)
    result = [item.strip() for item in re.split(r'\*', result) if item.strip()]
    print(result)