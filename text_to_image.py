import base64
import random
import boto3
import json
import replicate
from typing import Callable, Any
from dotenv import load_dotenv
import requests

from config import BaseConfig
from generative import get_number_prompt

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
            case 'mlochakl':
                return 'harnessing-ai-project/mlochkl:8553c1bf71aaeb2a525470679364d04a2296b94ab1bc0af17447387de1db6a2f'
            case 'kazaaf':
                return 'black-forest-labs/flux-dev'
              #  return 'harnessing-ai-project/kazaaf:6010b24abc582a3da48d64aadcdf377bc20158a92608b3141c3baa9c833b7765'
            case 'dmaa':
                return 'harnessing-ai-project/dmaa:190146f38302eb47f038198782aa30352e60c58c7b2860ca3e02216557553bf5'
            case 'usakir': # roach
                return 'harnessing-ai-project/usakir:a5386ae4230b7c6a325d0c00f53cc0fb596ff726635b57551536e65ba97bdb36'
            case 'usakif': # fly, circular pictures
                return 'harnessing-ai-project/usakif:f9cdcbbf8133f1e51bb7c6012c14e0e9015d79c41e395aa4eecfbdf60a9c8515'
            case 'usakim': # mosquito, circular pictures
                return 'harnessing-ai-project/usakim:8a035481dabdf43ad6a88d9b9a66542bf860015385e2973f5dd439b41e9270fd'
            case 'kazanil':
                return 'harnessing-ai-project/kazanil:27e1a4eaa3df9bd2c9c52ca86c80b25663d3a33bea56cb63a4df41fa53866b8e'
            case 'kazanis':
                return 'harnessing-ai-project/kazanis:b9ad953ec02ad90cdf8947ea6179779d3938e36a486c0a12512b948e55140843'
            case 'mwfz':
                return 'harnessing-ai-project/mwfz-flux:129947ef1820a641453ca09ff050cf832dac392737b3c9cae703bb18dfb846fa'
            case 'namba':
                return 'harnessing-ai-project/mwfz-flux:129947ef1820a641453ca09ff050cf832dac392737b3c9cae703bb18dfb846fa'
            case 'vpmmes':
                return 'harnessing-ai-project/vpmmes:f27290c0d1076d0c04d67062c5f918cd9bcf2a5bf29495bb34bbd078c0a9aa8e'
            case 'umbomrab':
                return 'harnessing-ai-project/umbomrab:f4c21a0a4fa5f6dc8a1b09ee3f18921a2b6be20e9b66fb825c5d8f3b1cd8bfba'
            case 'umbomstat':
                return 'harnessing-ai-project/umbomstat:ddcc3508c838ecc0f7d83848dafe979f9a216b1d4697c28638864faf9fcc2801'
            case 'umboptt':
                return 'harnessing-ai-project/umboptt:98fc502472cf639fb8bb7743fd2fdf5664a4a4b329b25b744beb53e9219cf6d6'
            case 'matumz':
                return 'harnessing-ai-project/matumizi-nishati:41370a4f6638dc7ccd2dbb72c9e3485c88a60f2f8f01a05157179f95dc3818e2'
            case 'kingamwl':
                return 'harnessing-ai-project/kingamwili:1a6ebdd35cf31e9c2eb65e1e8e7662bc05873120895b36565f08d9692166929a'
            case 'hls':
                return 'black-forest-labs/flux-dev'
            case 'mwsl':
                return 'harnessing-ai-project/kazanis:b9ad953ec02ad90cdf8947ea6179779d3938e36a486c0a12512b948e55140843'
            

            # money urls
            case 'hamsinifr':
                return 'https://res.cloudinary.com/dlpbfst4n/image/upload/v1738273376/money/50-front_con1qh.jpg'
            case 'hamsinibk':
                return 'https://res.cloudinary.com/dlpbfst4n/image/upload/v1738273376/money/50-back_iaimkb.jpg'
            case 'miafr':
                return 'https://res.cloudinary.com/dlpbfst4n/image/upload/v1738273377/money/100-front_km6ktl.jpg'
            case 'miabk':
                return 'https://res.cloudinary.com/dlpbfst4n/image/upload/v1738273376/money/100-back_eamkn6.jpg'
            case 'miambilifr':
                return 'https://res.cloudinary.com/dlpbfst4n/image/upload/v1738273376/money/200-front_mohmlp.jpg'
            case 'miambilibk':
                return 'https://res.cloudinary.com/dlpbfst4n/image/upload/v1738273376/money/200-back_u1faty.jpg'
            case 'miatanofr':
                return 'https://res.cloudinary.com/dlpbfst4n/image/upload/v1738273377/money/500-front_dqqybe.jpg'
            case 'miatanobk':
                return 'https://res.cloudinary.com/dlpbfst4n/image/upload/v1738273377/money/500-back_hl2wax.jpg'
            case 'elfufr':
                return 'https://res.cloudinary.com/dlpbfst4n/image/upload/v1738273384/money/1000-front_bm8zew.jpg'
            case 'elfubk':
                return 'https://res.cloudinary.com/dlpbfst4n/image/upload/v1738273379/money/1000-back_ephwow.jpg'
            case 'elfumbilifr':
                return 'https://res.cloudinary.com/dlpbfst4n/image/upload/v1738273379/money/2000-front_cvs3sx.jpg'
            case 'elfumbilibk':
                return 'https://res.cloudinary.com/dlpbfst4n/image/upload/v1738273379/money/2000-back_yoko8s.jpg'
            case 'elfutanofr':
                return 'https://res.cloudinary.com/dlpbfst4n/image/upload/v1738273385/money/5000-front_rsqewd.jpg'
            case 'elfutanobk':
                return 'https://res.cloudinary.com/dlpbfst4n/image/upload/v1738273379/money/5000-back_xvnok8.jpg'
            case 'elfukumifr':
                return 'https://res.cloudinary.com/dlpbfst4n/image/upload/v1738273380/money/10000-front_jqa3yd.jpg'
            case 'elfukumibk':
                return 'https://res.cloudinary.com/dlpbfst4n/image/upload/v1738273380/money/10000-back_qnzcbp.jpg'

            # disease urls
            case 'ambkz':
                return 'https://res.cloudinary.com/dlpbfst4n/image/upload/v1742506341/magonjwa/yakuambukizwa_mic6wj.png'
            case 'dddd':
                return 'https://res.cloudinary.com/dlpbfst4n/image/upload/v1742505530/magonjwa/yasiyoambukizwa_vertpd.png'
            
            # infections urls
            case 'mlr':
                return 'harnessing-ai-project/mamabi:1166cf4666f98af21099cdb6af43417f7dd1000e4e0f44baaa85d7ea539943e2'
            case 'ppp':
                return 'harnessing-ai-project/mamabi:1166cf4666f98af21099cdb6af43417f7dd1000e4e0f44baaa85d7ea539943e2'
            case 'kcc':
                return 'harnessing-ai-project/mamabi:1166cf4666f98af21099cdb6af43417f7dd1000e4e0f44baaa85d7ea539943e2'
            case 'kpu':
                return 'harnessing-ai-project/mamabi:1166cf4666f98af21099cdb6af43417f7dd1000e4e0f44baaa85d7ea539943e2'
            case 'tete':
                return 'harnessing-ai-project/mamabi:1166cf4666f98af21099cdb6af43417f7dd1000e4e0f44baaa85d7ea539943e2'
            case 'mamabi':
                return 'harnessing-ai-project/mamabi:1166cf4666f98af21099cdb6af43417f7dd1000e4e0f44baaa85d7ea539943e2'
            
            # insect growth urls
            case 'fly':
                return 'harnessing-ai-project/wddnzi:776ff495be406c63ecc9b0defe55c4d6ff70ba2d7687679ac78caf9535b3ee83'
            case 'quito':
                return 'harnessing-ai-project/wddmbu:fe02248e96ee67b5c9bb80b2fe1b17576d597c8bfe01d961c0af8dbd527e3e1b'
            case 'roach':
                return ''
            
            # good for math
            case 'zz':
                return 'ideogram-ai/ideogram-v2a-turbo'
            
            # default url
            case 'noop':
                return 'https://res.cloudinary.com/dlpbfst4n/image/upload/v1743067327/no_image/no_image_k2qjla.png'
    
    def generate(
            self,
            prompt: str,
            *,
            negative_prompt: str | None = None,
            num_steps = 80,
            callback: Callable[[int, int, Any], None] | None = None
    ) -> bytes | None:
        trigger_words = ['miyafa', 'kazaaf', 'mwfz','matumz', 'mwsl', 'mamabi','kingamwl', 'mlochakl', 'zz', 'ambkz', 'hls', 'dddd', 'roach', 'quito', 'fly', 'mlr', 'ppp', 'kcc', 'kpu', 'tete', 'noop', 'dmaa', 'usakir', 'usakim', 'usakif', 'kazanil', 'kazanis', 'vpmmes', 'umbomrab', 'umbomstat', 'umboptt', 'hamsinifr', 'hamsinibk', 'miafr', 'miabk', 'miambilifr', 'miambilibk', 'miatanofr', 'miatanobk', 'elfufr', 'elfubk', 'elfumbilifr', 'elfumbilibk', 'elfutanofr', 'elfutanobk', 'elfukumifr', 'elfukumibk', 'namba']
        words_in_prompt = [word.lower() for word in prompt.split()]

        print('prompt', prompt)

        trigger_word = [word for word in trigger_words if word in words_in_prompt]
        print(trigger_word)

        if len(trigger_word) > 0:
            img_model = self.get_image_model(trigger_word[0])
        else:
            img_model = "harnessing-ai-project/mwfz-flux:129947ef1820a641453ca09ff050cf832dac392737b3c9cae703bb18dfb846fa"

        money_words = ['hamsinifr', 'hamsinibk', 'miafr', 'miabk', 'miambilifr', 'miambilibk', 'miatanofr', 'miatanobk', 'elfufr', 'elfubk', 'elfumbilifr', 'elfumbilibk', 'elfutanofr', 'elfutanobk', 'elfukumifr', 'elfukumibk']
        # also in "disease type" like in money, we return the image from the cloud
        disease_words = ['ambkz', 'dddd']

        # case for no image
        no_image = ['noop']

        print('trigger_w', trigger_word)

        if (trigger_word[0] not in money_words) and (trigger_word[0] not in disease_words) and (trigger_word[0] not in no_image):
          #  prompt = get_number_prompt(prompt) if (trigger_word[0] == "namba") else prompt
            print('prompt near replicate', prompt)

            output = replicate.run(
                img_model,
                input={"prompt": f"{prompt}"}
            )

            print('checking output', output)
            print('type', type(output))

            # some models return this class containing image url instead of bytes
            if isinstance(output, replicate.helpers.FileOutput):
                return str(output)

            if isinstance(output, list) and len(output) > 0:
                file_output = output[0]

                image_data = file_output.read()

                return image_data
            
        elif trigger_word[0] in money_words:
            response = requests.get(img_model, stream=True)
            img_data = response.content
            return img_data
        
        elif trigger_word[0] in disease_words:
            response = requests.get(img_model, stream=True)
            img_data = response.content
            return img_data
        
        elif trigger_word[0] in no_image:
            response = requests.get(img_model, stream=True)
            img_data = response.content
            return img_data
        
        return None
