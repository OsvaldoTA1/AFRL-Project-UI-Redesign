personality_prompts = {
    "openness": {
        "profession": "place holder",
        "attire": "place holder",
        "expression": "place holder",
        "setting": "place holder"
    },
    "conscientiousness": {
        "profession": "place holder",
        "attire": "place holder",
        "expression": "place holder",
        "setting": "place holder"
    },
    "extraversion": {
        "profession": "place holder",
        "attire": "place holder",
        "expression": "place holder",
        "setting": "place holder"
    },
    "agreeableness": {
        "profession": "place holder",
        "attire": "place holder",
        "expression": "place holder",
        "setting": "place holder"
    },
    "neuroticism": {
        "profession": "place holder",
        "attire": "place holder",
        "expression": "place holder",
        "setting": "place holder"
    }
}

gender_prompts = {
    "Male": {
        "subject": "woman",
        "pose": "place holder"
    },
    "Female": {
        "subject": "man",
        "pose": "place holder"
    }
}

default_prompts = {
    "art_style": "realistic",
    "quality": "high quality",
    "age-range": "25-35 years old",
    "attractiveness": "place holder",
    "lighting": "neutral lighting, soft shadows",
    "composition": "place holder"
}

cultural_progression_prompts = {
    "level_0": {
        "setting": "place holder",
        "styling": "place holder",
        "accessories": "place holder"
    },
    "level_1": {
        "setting": "place holder",
        "styling": "place holder",
        "accessories": "place holder"
    },
    "level_2": {
        "setting": "place holder",
        "styling": "place holder",
        "accessories": "place holder"
    },
    "level_3": {
        "setting": "place holder",
        "styling": "place holder",
        "accessories": "place holder"
    },
    "level_4": {
        "setting": "place holder",
        "styling": "place holder",
        "accessories": "place holder"
    },
}

def prompt_generator(user_data, gender):
    highest_trait = max(user_data, key=user_data.get)

    personality_configuration = personality_prompts[highest_trait]
    gender_configuration = gender_prompts[gender]

    prompts = []

    for level in range(5):
        cultural_config = cultural_progression_prompts[f"level_{level}"]
        
        prompt = build_prompt(personality_configuration, gender_configuration, cultural_config, default_prompts)
        prompts.append(prompt)
    
    return prompts

def build_prompt(personality, gender, cultural, defaults):
    # Change the order of the prompt parts to match the desired structure
    prompt_parts = [
        defaults["art_style"],
        gender["subject"],
        personality["profession"],
        personality["attire"],
        personality["expression"],
        cultural["setting"],
        cultural["styling"],
        cultural["accessories"],
        defaults["quality"],
    ]

    final_prompt = ", ".join(filter(prompt_parts))
    return final_prompt