import openai
import config

openai.api_key = config.OPENAI_API_KEY

def get_gpt_response(prompt):
    response = openai.Completion.create(
        engine="davinci-codex",  # Используйте нужную вам модель
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
