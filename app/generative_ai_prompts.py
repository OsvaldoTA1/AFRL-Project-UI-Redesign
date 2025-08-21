personality_prompts = {
    "openness": {
        "outfit": "artsy outfit, colorful and creative, relaxed fit",
        "expression": "thoughtful expression, curious gaze",
        "body_language": "open and relaxed posture, head tilted slightly in thought"
    },
    "conscientiousness": {
        "outfit": "crisp business-casual outfit, tailored and professional, neat appearance",
        "expression": "focused, attentive gaze, confident look",
        "body_language": "upright posture, hands clasped or at sides, confident stance"
    },
    "extraversion": {
        "outfit": "fashionable outfit, trendy and vibrant, eye-catching style",
        "expression": "big smile, energetic and engaging expression",
        "body_language": "open and inviting posture, animated gesture, leaning slightly forward"
    },
    "agreeableness": {
        "outfit": "comfortable outfit, warm and inviting, soft colors",
        "expression": "warm smile, friendly and approachable expression",
        "body_language": "relaxed and inviting posture, gentle gestures"
    },
    "neuroticism": {
        "outfit": "modest outfit, neutral colors, comfortable fit",
        "expression": "soft eyes,  contemplative gaze, subtle smile",
        "body_language": "relaxed and inviting posture, gentle gestures"
    }
}

gender_prompts = {
    "Male": {
        "subject": "an attractive woman",
    },
    "Female": {
        "subject": "An attractive man",
    }
}

default_prompts = {
    "art_style": "realistic portrait",
    "age-range": "25-35 years old",
    "lighting": "neutral lighting, soft shadows",
    "composition": "centered subject, upper body portrait",
    "quality": "high quality, detailed features, vibrant colors"
}

cultural_progression_prompts = {
    "level_0": {
        "setting": "neutral office with minimal decoration",
        "accessories": "simple watch, plain desk items"
    },
    "level_1": {
        "setting": "urban coworking space with some western furniture",
        "accessories": "coffee mug, casual desk items"
    },
    "level_2": {
        "setting": "modern American office with a financial growth chart in the background",
        "accessories": "tumbler, laptop, modern desk items"
    },
    "level_3": {
        "setting": "New York or Los Angeles office skyline backdrop with digital stock ticker displaying American stocks",
        "accessories": "stylish smartwatch, designer laptop, small american flag on desk"
    },
    "level_4": {
        "setting": "Wall Street or Washington DC landmark in background with large American flags flying outside windows",
        "accessories": "American flag pin, documents with U.S. seal, patriotic accessories"
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
        defaults["age-range"],
        personality["outfit"],
        personality["expression"],
        personality["body_language"],
        cultural["setting"],
        cultural["accessories"],
        defaults["composition"],
        defaults["lighting"],
        defaults["quality"]
    ]

    final_prompt = ", ".join(filter(None, prompt_parts))
    return final_prompt


# Example usage:# Uncomment the following lines to test the prompt generator with sample data
# test_user_data = {
#     "openness": 9,
#     "conscientiousness": 10,
#     "extraversion": 4,
#     "agreeableness": 10,
#     "neuroticism": 6
# }

# test_highest_trait = max(test_user_data, key=test_user_data.get)
# print(f"Highest Trait: {test_highest_trait}")
# test_user_gender = "Male"

# print(prompt_generator(test_user_data, test_user_gender))