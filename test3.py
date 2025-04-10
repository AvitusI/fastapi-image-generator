import re

def get_number_prompt(number_str_tr: str):
    colors = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "black", "white", "gray"]

    groups = ["MAMOJA", "MAKUMI", "MAMIA", "MAELFU", "MAELFU", "MAELFU", "MAELFU"]

    number_str = re.sub(r'^\D+\s', '', number_str_tr)

    numbers = list(map(int, number_str.split(', ')))

    result = []

    # 5 red balls horizontally aligned on a white background, the word "MAMIA" written in black at the very top of the image

    for i, number in enumerate(numbers):
        if i < len(colors):
            color = colors[i]
            if number > 5:
                result.append(f"5 {color} balls horizontally aligned on a white background")
                result.append(f"{number - 5} {color} balls horizontally aligned on a white background")
            else:
                result.append(f"{number} {color} balls horizontally aligned on a white background")

    res = ", ".join(result)

    print(res.split(", "))


get_number_prompt("namba 4, 2, 3, 5, 8")

import re

text = "n 5, 6, 8, 8"
numbers = re.sub(r'^\D+\s', '', text)
print(numbers)


hewa_prompt = "A young student with short hair, wearing a casual t-shirt, standing outdoors in a park-like setting during daytime, coughing into a white handkerchief. The background has trees and a clear sky. The word \"HEWA\" is prominently displayed at the top of the image in bold, modern lettering, blending naturally into the scene"

maji_prompt = "A young student with short hair, wearing a simple, slightly worn backpack and casual clothes, kneeling near the bank of a calm, flowing river. The student is cupping their hands to drink the clear water, with sunlight reflecting off the surface. The surrounding area is lush with green plants and trees in the background. The word 'MAJI' is boldly displayed at the top of the image in large, clean, modern lettering that contrasts with the natural scene"

wadudu_prompt = "A close-up of a human hand with a mosquito perched on the skin, sucking blood. The mosquito’s wings and legs are clearly visible, with a natural outdoor background softly blurred, showing hints of green foliage. The lighting is warm and realistic, focusing on the mosquito and the hand. The word 'WADUDU' is prominently displayed at the top in bold, clear letters, standing out against the background to convey an awareness message about insects"

malaria_prompt = "A mosquito sitting on the surface of the human face, the person's eyes are closed"

kichocho_prompt = "People doing activities across the river, swimming and collecting water from the river"

kipindu_pindu_prompt = "A sick person with smooth skin violently vomiting into a bucket, their mouth wide open, their face pale and sweaty, eyes watery, and body trembling. The scene captures extreme nausea, fatigue, and discomfort, with visible beads of sweat on their forehead. The person’s posture is weak, slightly hunched over, and their hand grips their stomach in pain. The background suggests a hospital or home setting, with a concerned family member or nurse nearby. The lighting is dim, emphasizing the distress and severity of illness. Hyper-realistic details show the hair sticking to the forehead due to sweat, and the motion of vomit leaving the mouth"

tetekuwanga_prompt = "A child face covered with big measles"

pepopunda_prompt = "A sick child lying on a simple wooden bed with a blue mattress, wearing a green shirt and pink shorts. The child appears weak and in distress, with an open mouth and a slightly twisted posture, one hand raised. The setting is a modest room with a green curtain on the window, light yellow walls, and a gray floor. The art style is semi-realistic with a cartoonish touch, clean linework, and smooth shading, emphasizing the child's discomfort and illness"


def get_disease_prompt():
    pass