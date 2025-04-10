def get_disease_prompt(disease: str):
    match disease:
        case 'mlr':
            return  [
                    "A mosquito sitting on the surface of the human face, the person's eyes are closed"
            ]
        case 'kcc':
            return  [
                    "People doing activities across the river, swimming and collecting water from the river"
            ]
        case 'kpu':
            return  [
                    """A sick person with smooth skin violently vomiting into a bucket, their mouth wide open, 
                    their face pale and sweaty, eyes watery, and body trembling. The scene captures extreme 
                    nausea, fatigue, and discomfort, with visible beads of sweat on their forehead. The 
                    person posture is weak, slightly hunched over, and their hand grips their stomach 
                    in pain. The background suggests a hospital or home setting, with a concerned family 
                    member or nurse nearby. The lighting is dim, emphasizing the distress and severity of 
                    illness. Hyper-realistic details show the hair sticking to the forehead due to sweat, 
                    and the motion of vomit leaving the mouth"""
            ]
        case 'tete':
            return  [
                    "A child face covered with big measles"
            ]
        case 'ppp':
            return  [
                    """A sick child lying on a simple wooden bed with a blue mattress, wearing a green shirt 
                    and pink shorts. The child appears weak and in distress, with an open mouth and a slightly 
                    twisted posture, one hand raised. The setting is a modest room with a green curtain on the 
                    window, light yellow walls, and a gray floor. The art style is semi-realistic with a cartoonish 
                    touch, clean linework, and smooth shading, emphasizing the child's discomfort and illness"""
            ]
        
def get_insect_growth_promt(insect: str) -> list[str]:
    match insect:
        case 'roach':
            return [
                "A photo of a cockroach egg in brown color with a white background",
                "A photo of a small cockroach with a white background",
                "A  photo of a full grown cockroach in a white background"
            ]
        case 'fly':
            return [
                "WDDNZI Photo of a pile of white rice, captured in a close-up shot with a macro lens, in a white and black style. The rice is scattered all over the image, with some grains overlapping and others standing alone. The composition is minimalistic, focusing on the texture and details of the rice. There is no text in the image",
                "WDDNZI Photo of a small white caterpillar with a brown head, sitting on a white surface. The caterpillar has a brown head and is covered in white and brown fur. The caterpillar is sitting on a white surface, which is the background of the photo. The photo is taken in a close-up style, focusing on the details of the caterpillar",
                "WDDNZI Photo of a red caterpillar with a black head, sitting on a white surface. The caterpillar is long and skinny, with a red body and black head. The caterpillar is sitting on a white background, with no other objects or elements in the image",
                "WDDNZI A photo of a large fly with a brown body and a white wing. The fly is sitting on a white background. The fly has long antennae and a pair of wings. The fly is looking to the left"
            ]
        case 'quito':
            return [
                "WDDMBU A drawing of a row of teeth, each tooth is white and has a sharp edge. The teeth are lined up in a row, with some teeth overlapping each other. The drawing is in black and white, giving it a classic and timeless appearance",
                "WDDMBU Photo of a caterpillar with a brown head and a long brown body, standing on its head in a white background, close-up, macro, detailed, a sense of nature, a science documentary scene rendered in the Canon EOS R5",
                "WDDMBU A cartoon illustration of a brown and tan bug with a long antennae and a brown head. The bug is standing on a white background",
                "WDDMBU Photo of a mosquito in a futuristic style with futuristic design, white background, soft lighting, dynamic pose, a sense of future technology, a science fiction movie scene rendered in the Unreal Engine"
            ]


prompts = ['ppp']

# prompts for maambukizi
trigger_words = ['mlr', 'kcc', 'kpu', 'tete', 'ppp']
og_arr_prompt = prompts
# Capture the matching element
matches = [item for item in trigger_words if item in og_arr_prompt]
if matches:
    match = matches[0]  # Get the first matching element
    # print(f"Matching element: {match}")
    result = get_disease_prompt(match)
    print(result)
else:
    print("No matching element")


