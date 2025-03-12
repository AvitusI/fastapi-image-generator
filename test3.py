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
