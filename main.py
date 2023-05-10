import gpt_utils as gpt
import stack_overflow_utils as stack_overflow
import calculate_metrics as calc
import time
import pandas as pd

# questions = stack_overflow.get_questions(1500, 5)
# responses = []
# for question in questions:
#     gpt_question = "Generate a Java code to answer the following question: " + question[
#         'title']
#     print(gpt_question)
#     try:
#         response = gpt.ask_gpt(gpt_question)
#         question['answer_chatgpt'] = response
#         responses.append(question)
#     except:
#         time.sleep(360)

#     time.sleep(15)

# df = pd.DataFrame(data=responses)
# print(df)
# df.to_csv('responses.csv')

# Rodar só depois de minerar todos os dados
calc.calculate_all()