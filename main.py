import gpt_utils as gpt
import stack_overflow_utils as stack_overflow
import generate_java_classes as generator
import time
import pandas as pd

questions = stack_overflow.get_questions(1)
responses = []
for question in questions:
    gpt_question = "Generate a Java code to answer the following question: " + question[
        'title']
    response = gpt.ask_gpt(gpt_question)
    question['answer_chatgpt'] = response
    responses.append(question)
    time.sleep(20)

df = pd.DataFrame(data=responses)
df.to_csv('responses.csv')

generator.generate_files()