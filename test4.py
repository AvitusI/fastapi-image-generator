import re

def get_number_prompt(number_str_tr: str):
    colors = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "black", "white", "gray"]
    groups = ["MAMOJA", "MAKUMI", "MAMIA", "MAELFU"]

    # Extract the numeric part from the input
    number_str = re.sub(r'^\D+\s', '', number_str_tr)
    number_str = number_str.replace(',', '').strip()

    # Split the number into digits
    digits = list(map(int, number_str))
    print("digits", digits)

    result = []

    # Generate the prompt for each digit based on place value
    for i, digit in enumerate(digits):
        group = groups[len(digits) - i - 1] if len(digits) - i - 1 < len(groups) else "MAELFU"
        
        if digit == 0:
            result.append(f"a word \"{group}\" written in black on a white background")
        else:
            color = colors[i % len(colors)]
            ball_word = "ball" if digit == 1 else "balls"

            if digit > 5:
                result.append(f"5 {color} {ball_word} horizontally aligned on a white background, the word \"{group}\" written in black at the very top of the image")
                result.append(f"{digit - 5} {color} {ball_word} horizontally aligned on a white background, the word \"{group}\" written in black at the very top of the image")
            else:
                result.append(f"{digit} {color} {ball_word} horizontally aligned on a white background, the word \"{group}\" written in black at the very top of the image")

    # Ensure the highest place value appears first
    # result.reverse()
    print(result)


get_number_prompt("namba 4631")

def get_number_prompt_2(number_str: str):
    colors = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "black", "white", "gray"]
    groups = ["MAMOJA", "MAKUMI", "MAMIA", "MAELFU"]

    # removing any word from the string("namba" in this case)
    new_number_str = re.sub(r'^\D+\s', '', number_str)
    new_number_str = new_number_str.replace(',', '').strip()

    numbers = list(map(int, new_number_str))
    print(numbers)

    result = []

    for i, digit in enumerate(numbers):
        group = groups[len(numbers) - i - 1] if len(numbers) - i - 1 < len(groups) else "MAELFU"
        
        if digit == 0:
            result.append(f"a word \"{group}\" written in black on a white background")
        else:
            color = colors[i % len(colors)]
            ball_word = "ball" if digit == 1 else "balls"

            if digit > 5:
                result.append(f"5 {color} {ball_word} horizontally aligned on a white background, the word \"{group}\" written in black at the very top of the image")
                result.append(f"{digit - 5} {color} {ball_word} horizontally aligned on a white background, the word \"{group}\" written in black at the very top of the image")
            else:
                result.append(f"{digit} {color} {ball_word} horizontally aligned on a white background, the word \"{group}\" written in black at the very top of the image")

    return result

print(get_number_prompt_2("namba 4631"))

