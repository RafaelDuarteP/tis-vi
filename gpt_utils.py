import requests
import json

url = 'https://api.openai.com/v1/engines/ada/completions'
api_key = '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'


def ask_gpt(prompt):

    params = {
        'prompt': prompt,
        'max_tokens': 100,
        'temperature': 0.2,
        'format': 'text',
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }

    response = requests.post(url, headers=headers, data=json.dumps(params))

    if response.status_code == 200:
        response_text = json.loads(response.text)['choices'][0]['text']
        return response_text
    else:
        print(f"Erro {response.status_code}: {response.text}")
