import base64
import random
import boto3
import json
import replicate
from typing import Callable, Any
from dotenv import load_dotenv

from config import BaseConfig

load_dotenv()

settings = BaseConfig()

REPLICATE_API_TOKEN = settings.REPLICATE_API_TOKEN

class TextToImage:

    def load_process(self) -> None:
        print("Ready to generate images")

    def get_image_model(self, value: str) -> str:
        match value:
            case 'miyafa':
                return 'harnessing-ai-project/miyafa:005a9ecd039552ff2dcce950f926cd893ee028e4cfd67469a9cf94b37f8012b0'
            case 'kazaaf':
                return 'harnessing-ai-project/kazaaf:6010b24abc582a3da48d64aadcdf377bc20158a92608b3141c3baa9c833b7765'
            case 'dmaa':
                return 'harnessing-ai-project/dmaa:190146f38302eb47f038198782aa30352e60c58c7b2860ca3e02216557553bf5'
            case 'usakir': # roach
                return 'harnessing-ai-project/usakir:a5386ae4230b7c6a325d0c00f53cc0fb596ff726635b57551536e65ba97bdb36'
            case 'usakif': # fly, circular pictures
                return 'harnessing-ai-project/usakif:f9cdcbbf8133f1e51bb7c6012c14e0e9015d79c41e395aa4eecfbdf60a9c8515'
            case 'usakim': # mosquito, circular pictures
                return 'harnessing-ai-project/usakim:8a035481dabdf43ad6a88d9b9a66542bf860015385e2973f5dd439b41e9270fd'
            case 'mwfz':
                return 'harnessing-ai-project/mwfz-flux:129947ef1820a641453ca09ff050cf832dac392737b3c9cae703bb18dfb846fa'
    
    def generate(
            self,
            prompt: str,
            *,
            negative_prompt: str | None = None,
            num_steps = 80,
            callback: Callable[[int, int, Any], None] | None = None
    ) -> bytes | None:
        trigger_words = ['miyafa', 'kazaaf', 'mwfz', 'dmaa', 'usakir', 'usakim', 'usakif']
        words_in_prompt = [word.lower() for word in prompt.split()]

        trigger_word = [word for word in trigger_words if word in words_in_prompt]
        print(trigger_word)

        if len(trigger_word) > 0:
            img_model = self.get_image_model(trigger_word[0])
        else:
            img_model = "harnessing-ai-project/mwfz-flux:129947ef1820a641453ca09ff050cf832dac392737b3c9cae703bb18dfb846fa"
        
        output = replicate.run(
            img_model,
            input={"prompt": f"{prompt}"}
        )

        if isinstance(output, list) and len(output) > 0:
            file_output = output[0]

            image_data = file_output.read()

            return image_data
        
        return None
