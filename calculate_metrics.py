import pandas as pd
import markdown
import os
import shutil
import re
import math
import time
from bs4 import BeautifulSoup

CLOC = r'tools\cloc.exe  ./files/ --csv  --report-file metrics/clocMetrics.csv'
DESIGNITE = 'java -jar tools/DesigniteJava.jar -i ./files/ -o metrics/'
PMD = 'pmd -d ./files/ -f csv --report-file metrics/pmdMetrics.csv -R tools\pmd-report.xml -shortnames'


def onerror(func, path, exc_info):
    import stat
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


def delete_dirs():
    if os.path.exists(r'metrics'):
        shutil.rmtree(r'metrics', onerror=onerror)
    if os.path.exists(r'files'):
        shutil.rmtree(r'files', onerror=onerror)


def create_dirs():
    if not os.path.exists(r'metrics'):
        os.makedirs(r'metrics')
    if not os.path.exists(r'files'):
        os.makedirs(r'files')


def create_java(name, dir, code_blocks):
    with open(f'{dir}/{name}.java', "w") as f:
        for j, code in enumerate(code_blocks):
            code_text = code.get_text()
            if "class" in code_text:
                f.write(code_text)
            elif code_text.count("\n") > 1:
                f.write(f"public class MyClass{j} {{\n{code_text}\n}}")
            f.write("\n\n")


def find_on_pmd(df, value, regex):
    df = df[df['Rule'] == value]
    soma = 0
    for i, row in df.iterrows():
        match = re.search(regex, row['Description'])
        if match:
            soma += int(match.group(1))
    resultado = soma if soma != 0 else 1
    return resultado


def avg_variables_names(df):
    df_variable = df[df['Rule'] == 'Variable']
    regex = r"Avoid excessively long variable names like (\w+)"
    soma_len_var = 0
    count_var = 0
    for i, row in df_variable.iterrows():
        match = re.search(regex, row['Description'])
        if match:
            soma_len_var += len(match.group(1))
            count_var += 1
    resultado = soma_len_var / count_var if count_var != 0 else 1
    return resultado


def calcular_mi(V, G, L):
    return 171 - 5.2 * math.log(V) - 0.23 * G - 16.2 * math.log(L)


def run_tools():
    os.system(DESIGNITE)
    os.system(PMD)
    os.system(CLOC)


def get_metrics():
    designite_metrics = pd.read_csv('metrics/methodMetrics.csv')
    pmd_metrics = pd.read_csv('metrics/pmdMetrics.csv')
    cloc_metrics = pd.read_csv('metrics/clocMetrics.csv')
    # Métricas do cloc
    loc = cloc_metrics.loc[cloc_metrics['language'] == 'SUM', 'code'].values[0]
    loc = loc if loc > 0 else 1
    comments = cloc_metrics.loc[cloc_metrics['language'] == 'SUM',
                                'comment'].values[0]
    # Métricas do designite
    cc = designite_metrics['CC'].sum()
    cc = cc if cc > 0 else 1
    # Métricas do pmd
    npath = find_on_pmd(
        pmd_metrics, 'NPath',
        r"The method '[^']+' has an NPath complexity of (\d+),")
    cogntive = find_on_pmd(
        pmd_metrics, 'Cognitive',
        r"The method '[^']+' has a cognitive complexity of (\d+),")
    var_names = avg_variables_names(pmd_metrics)
    return loc, comments, cc, npath, cogntive, var_names


def create_columns(df):
    df['loc_gpt'] = pd.NA
    df['comments_gpt'] = pd.NA
    df['comments_density_gpt'] = pd.NA
    df['cc_gpt'] = pd.NA
    df['npath_gpt'] = pd.NA
    df['cognitive_gpt'] = pd.NA
    df['var_names_gpt'] = pd.NA
    df['mi_gpt'] = pd.NA
    df['loc_stackoverflow'] = pd.NA
    df['comments_stackoverflow'] = pd.NA
    df['comments_density_stackoverflow'] = pd.NA
    df['cc_stackoverflow'] = pd.NA
    df['npath_stackoverflow'] = pd.NA
    df['cognitive_stackoverflow'] = pd.NA
    df['var_names_stackoverflow'] = pd.NA
    df['mi_stackoverflow'] = pd.NA


def calculate_all():
    df = pd.read_csv('responses.csv', index_col='index')

    delete_dirs()
    for i, row in df.iterrows():
        try:
            if i % 10 == 0:
                df.to_csv('responses_final.csv')
                print(f'salvou {i}:', df)
            create_dirs()
            html = markdown.markdown(row['answer_chatgpt'],
                                     extensions=["fenced_code"])
            soup = BeautifulSoup(html, "html.parser")
            code_blocks = soup.find_all("code")
            create_java(name=f'RespostaGPT{i}',
                        dir='files',
                        code_blocks=code_blocks)
            run_tools()
            loc, comments, cc, npath, cogntive, var_names = get_metrics()
            mi = calcular_mi(loc, cc, var_names)
            df.loc[i, 'loc_gpt'] = loc
            df.loc[i, 'comments_gpt'] = comments
            df.loc[i, 'comments_density_gpt'] = comments / loc
            df.loc[i, 'cc_gpt'] = cc
            df.loc[i, 'npath_gpt'] = npath
            df.loc[i, 'cogntive_gpt'] = cogntive
            df.loc[i, 'var_names_gpt'] = var_names
            df.loc[i, 'mi_gpt'] = mi

            delete_dirs()

            create_dirs()
            html = row['answer_stackoverflow']
            soup = BeautifulSoup(html, "html.parser")
            code_blocks = soup.find_all("code")
            create_java(name=f'RespostaStackOverflow{i}',
                        dir='files',
                        code_blocks=code_blocks)
            run_tools()

            loc, comments, cc, npath, cogntive, var_names = get_metrics()
            mi = calcular_mi(loc, cc, var_names)
            df.loc[i, 'loc_stackoverflow'] = loc
            df.loc[i, 'comments_stackoverflow'] = comments
            df.loc[i, 'comments_density_stackoverflow'] = comments / loc
            df.loc[i, 'cc_stackoverflow'] = cc
            df.loc[i, 'npath_stackoverflow'] = npath
            df.loc[i, 'cogntive_stackoverflow'] = cogntive
            df.loc[i, 'var_names_stackoverflow'] = var_names
            df.loc[i, 'mi_stackoverflow'] = mi
        except Exception as e:
            print('erro', e)
        delete_dirs()

    df = df.drop(labels=['answer_stackoverflow', 'answer_chatgpt'], axis=1)
    df = df.dropna(how='any')
    df.to_csv('responses_final.csv')
