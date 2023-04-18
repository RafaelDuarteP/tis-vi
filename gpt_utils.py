import openai

url = 'https://api.openai.com/v1/engines/ada/completions'
api_key = ''

openai.api_key = api_key


def ask_gpt(prompt):

    response = openai.ChatCompletion.create(model='gpt-3.5-turbo',
                                            max_tokens=2048,
                                            n=1,
                                            stop=None,
                                            temperature=0.5,
                                            messages=[{
                                                'role': 'user',
                                                'content': prompt
                                            }])

    response_text = response['choices'][0]['message']['content']
    return response_text
