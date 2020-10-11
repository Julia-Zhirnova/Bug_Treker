# import requests
import subprocess
import traceback
from pylint import epylint as lint
import sys
import os
import datetime
import pandas as pd


class Tester(object):
    def __init__(self, filename):
        super(Tester, self).__init__()
        self.file = filename
        self.file_path = os.path.join(os.getcwd(), 'user_files', self.file.replace('.py', ''), self.file)
        self.date = datetime.datetime.now()
        self.report_file = os.path.join(os.getcwd(), 'user_files', self.file.replace('.py', '')
                                        , 'Report_' + self.file.replace('.py', '.xlsx'))
        self.report_items = {}
        self.pd_frame = self.excel_reader()
        print(self.report_items)

    def excel_reader(self):
        report_pd = pd.read_excel(self.report_file)
        data = {}
        for label, content in report_pd.items():
            print(label)
            self.report_items[label] = 1
        return report_pd

    def excel_writer(self):
        new_pd = self.pd_frame.append(pd.DataFrame(self.report_items), ignore_index=True)
        new_pd.to_excel(self.report_file)

    def syntax_test(self):
        # template = self.file_path+" --msg-template='{category};in-module_{module},line({line}):{msg}' "
        try:
            (pylint_stdout, pylint_stderr) = lint.py_run(command_options=self.file_path, return_std=True)
            syntax_err = []
            lints = pylint_stdout.getvalue().split('\n')[1:]
            for l in lints:
                if 'warning' in l:
                    syntax_err.append(l)
                else:
                    continue

            print(syntax_err)
        except:
            print('Syntax_error')

    def runtime_test(self):
        with open(self.file_path) as f:
            try:
                eval(compile(f.read(), '', 'exec'))
            except:
                trace = traceback.format_exc()
                print(trace)

    def __del__(self):
        print("cltkf")


def main():
    test = Tester('erors_file.py')
    test.syntax_test()
    del test
    # test.runtime_test()

    # os.startfile(r"C:\Users\yaroh\OneDrive\Рабочий стол\123.xlsx")
    # xl=pd.read_excel(r"C:\Users\yaroh\OneDrive\Рабочий стол\123.xlsx", index_col=0)
    # xl.to_excel('new_xl.xlsx')
    # pd.DataFrame()
    # print(xl)


if __name__ == '__main__':
    main()
