import gpt_utils as gpt
import stack_overflow_utils as stack_overflow
import time
import pandas as pd

dataset = stack_overflow.get_questions()
responses = []
for data in dataset:
    gpt_question = "Generate a Java code to answer the following question: " + data[
        'title']
    response = gpt.ask_gpt(gpt_question)
    responses.append({
        'title': data['title'],
        'response': response,
    })
    time.sleep(60)

df = pd.DataFrame(data=responses)
df.to_csv('responses.csv')