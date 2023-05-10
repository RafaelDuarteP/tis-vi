import requests
from dotenv import load_dotenv
import os

load_dotenv()


def get_questions(qtd_perguntas, initial_page):
    API_KEY = os.getenv('STACKEXCHANGE_API_KEY')
    ACCESS_TOKEN = os.getenv('STACKEXCHANGE_ACCESS_TOKEN')

    API_URL = "https://api.stackexchange.com/2.3/questions"

    params = {
        'pagesize': 100,
        'page': initial_page,
        'order': 'desc',
        'sort': 'votes',
        'tagged': 'java',
        'filter': '!-NHuCSYRitEzONDEFYLjR4dIIOte0KfzL',
        'site': 'stackoverflow',
        'key': API_KEY,
        'answers': 1,
        'hasaccepted': 'yes',
        'score': 1000,
        'views': 1000,
        'access_token': ACCESS_TOKEN,
    }

    data = []

    while len(data) < qtd_perguntas:
        try:
            response = requests.get(API_URL, params=params)
            questions = response.json()
            for question in questions['items']:
                if len(question['answers']) >= 1:
                    answers = [
                        answer for answer in question['answers']
                        if answer.get('is_accepted')
                    ]
                if len(answers) >= 1 and answers[0]['body'].find(
                        '</code>') > -1:
                    data.append({
                        'title': question['title'],
                        'question_id': question['question_id'],
                        'answer_id': answers[0]['answer_id'],
                        'question_url': question['link'],
                        'answer_url': answers[0]['link'],
                        'answer_stackoverflow': answers[0]['body'],
                    })
            params['page'] += 1
        except Exception as e:
            print('erro', e)
            params['page'] += 1

    return data[:qtd_perguntas]
