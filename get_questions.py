import requests
import pandas as pd

API_KEY = "l5CGpdxYUIe)fWzFwjwKrw(("
ACCESS_TOKEN = "V0F6hGzmto2gncuYJ0YiYw))"

API_URL = "https://api.stackexchange.com/2.3/questions"

params = {
    'pagesize': 10,
    'page': 1,
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

data_set = []

while len(data_set) < 100:
    try:
        response = requests.get(API_URL, params=params)
        questions = response.json()
        for question in questions['items']:
            question["answers"] = answers = list(
                filter(lambda item: item['is_accepted'], question["answers"]))
            if len(answers) >= 1 and answers[0]['body'].find('</code>') > -1:
                data_set.append({
                    'title': question['title'],
                    'question_id': question['question_id'],
                    'answer_id': answers[0]['answer_id'],
                    'question_url': question['link'],
                    'answer_url': answers[0]['link'],
                    'answer_body': answers[0]['body'],
                })
        params['page'] += 1
    except Exception as e:
        print('erro', e)

df = pd.DataFrame(data=data_set)
df.to_csv('data_set.csv')
print('done')
