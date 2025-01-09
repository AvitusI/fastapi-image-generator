def get_image_model(value: str) -> str:
    match value:
        case 'miyafa':
            return 'harnessing-ai-project/miyafa:005a9ecd039552ff2dcce950f926cd893ee028e4cfd67469a9cf94b37f8012b0'
        case 'kazaaf':
            return 'harnessing-ai-project/kazaaf:6010b24abc582a3da48d64aadcdf377bc20158a92608b3141c3baa9c833b7765'
        case 'mwfz':
            return 'harnessing-ai-project/mwfz-flux:129947ef1820a641453ca09ff050cf832dac392737b3c9cae703bb18dfb846fa'

prompt = "a high quality image of a human eye"

trigger_words = ['miyafa', 'kazaaf', 'mwfz']
words_in_prompt = [word.lower() for word in prompt.split()]
print(f"words in prompt: {words_in_prompt}")

trigger_word = [word for word in trigger_words if word in words_in_prompt]
print(trigger_word)

if len(trigger_word) > 0:
    img_model = get_image_model(trigger_word[0])
else:
    img_model = "harnessing-ai-project/mwfz-flux:129947ef1820a641453ca09ff050cf832dac392737b3c9cae703bb18dfb846fa"

print(img_model)