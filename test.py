# import requests
import subprocess
import traceback
import pylint
from pylint import epylint as lint
import sys
import os
import pandas as pd


def main():
    # os.startfile(r"C:\Users\yaroh\OneDrive\Рабочий стол\123.xlsx")
    xl=pd.read_excel(r"C:\Users\yaroh\OneDrive\Рабочий стол\123.xlsx", index_col=0)
    xl.to_excel('new_xl.xlsx')
    pd.DataFrame()
    print(xl)
    # syntax_erors
    # (pylint_stdout, pylint_stderr) = lint.py_run('erors_file.py', return_std=True)
    # print(pylint_stdout.getvalue())
    # # print(pylint_stderr.getvalue())
    # # print('qwe')
    #
    # # runtime_erors
    #
    # file_from_interface = 'erors_file.py'
    # program = "python erors_file.py"
    # with open(file_from_interface) as f:
    #     try:
    #         eval(compile(f.read(), '', 'exec'))
    #     except Exception as e:
    #         # print(e)*
    #         # traceback.print_exc(file=sys.stdout)
    #         exept = traceback.format_exc()
    #         print(exept)
    #         # print(traceback.extract_stack())

    # eval(compile('',filename='erors_file.py',mode='exec'))


if __name__ == '__main__':
    main()
