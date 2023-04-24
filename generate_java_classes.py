import pandas as pd
import markdown
from bs4 import BeautifulSoup

def createJava(name, code_blocks):
    with open(f'java/{name}.java', "w") as f:
        for j, code in enumerate(code_blocks):
            code_text = code.get_text()
            if "class" in code_text:
                f.write(code_text)
            elif code_text.count("\n") > 1:
                f.write(f"public class MyClass{j} {{\n{code_text}\n}}")
            f.write("\n\n")


def generate_files():
    df = pd.read_csv('responses.csv')
    for i, row in df.iterrows():
        html = markdown.markdown(row['answer_chatgpt'],
                                 extensions=["fenced_code"])
        soup = BeautifulSoup(html, "html.parser")
        code_blocks = soup.find_all("code")
        createJava(f'RespostaGPT{i}',code_blocks)
        html = row['answer_stackoverflow']
        soup = BeautifulSoup(html, "html.parser")
        code_blocks = soup.find_all("code")
        createJava(f'RespostaStackOverflow{i}',code_blocks)


        
