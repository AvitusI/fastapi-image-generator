import base64
import random
import boto3
import json
import replicate
from typing import Callable, Any

class TextToImage:

    def load_process(self) -> None:
        print("Ready to generate images")
    
    def generate(
            self,
            prompt: str,
            *,
            negative_prompt: str | None = None,
            num_steps = 80,
            callback: Callable[[int, int, Any], None] | None = None
    ) -> bytes | None:
        output = replicate.run(
            "harnessing-ai-project/mwfz-flux:129947ef1820a641453ca09ff050cf832dac392737b3c9cae703bb18dfb846fa",
            input={"prompt": f"MWFZ, {prompt}"}
        )

        if isinstance(output, list) and len(output) > 0:
            file_output = output[0]

            image_data = file_output.read()

            return image_data
        
        return None
