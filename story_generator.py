
from transformers import pipeline, set_seed
from genres import GENRES

# Load text-generation pipeline with GPT-Neo
generator = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")
set_seed(42)

def generate_story(prompt, genre, num_samples=1):
    prefix = GENRES.get(genre, "")
    full_prompt = prefix + "\n" + prompt.strip()
    stories = []

    for _ in range(num_samples):
        result = generator(
            full_prompt,
            max_length=200,
            truncation=True,
            do_sample=True,
            temperature=0.9,
            pad_token_id=50256  # To suppress padding warning
        )
        story = result[0]['generated_text'].strip()
        stories.append(story)

    return stories
