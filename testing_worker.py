# import requests
import subprocess
import traceback
from pylint import epylint as lint
import sys
import os
from datetime import datetime
import pandas as pd
import shutil


class Tester(object):
    def __init__(self, filename):
        super(Tester, self).__init__()
        self.file = filename
        self.file_path = os.path.join(os.getcwd(), 'user_files', self.file.replace('.py', ''), self.file)
        self.date = datetime.now()
        self.report_file = os.path.join(os.getcwd(), 'user_files', self.file.replace('.py', '')
                                        , 'Report_' + self.file.replace('.py', '.xlsx'))
        self.sample_path = os.path.join(os.getcwd(), 'user_files', 'sample_report.xlsx')

        try:
            open(os.path.join(os.getcwd(), 'user_files', self.file.replace('.py', ''),
                                   'Report_' + self.file.replace('.py', '.xlsx')))
        except:
            shutil.copy2(self.sample_path,
                         os.path.join(os.getcwd(), 'user_files', self.file.replace('.py', '')))
            os.rename(os.path.join(os.getcwd(), 'user_files', self.file.replace('.py', ''), 'sample_report.xlsx'),
                      os.path.join(os.getcwd(), 'user_files', self.file.replace('.py', ''),
                                   'Report_' + self.file.replace('.py', '.xlsx')))

        self.report_items = {}
        self.pd_frame = self.excel_reader()
        print(self.report_items)

    def excel_reader(self):
        report_pd = pd.read_excel(self.report_file)
        data = {}
        for label, content in report_pd.items():
            self.report_items[label] = ''
        return report_pd

    def excel_writer(self):
        new_pd = self.pd_frame.append(pd.DataFrame(self.report_items), ignore_index=True)
        new_pd.to_excel(self.report_file,index=False)

    def syntax_test(self):
        # template = self.file_path+" --msg-template='{category};in-module_{module},line({line}):{msg}' "
        try:
            (pylint_stdout, pylint_stderr) = lint.py_run(command_options=self.file_path, return_std=True)
            syntax_err = []
            lints = pylint_stdout.getvalue().split('\n')[1:]
            for l in lints:
                if 'warning' in l:
                    err = l.split(':')
                    syntax_err.append(f'line({err[2]}) : {err[3]} ')
                if 'rated' in l:
                    self.report_items['code_score'] = l.split('(')[0]
                else:
                    continue
            self.report_items['syntax_count'] = str(len(syntax_err))
            self.report_items['syntax_errors'] = '\n'.join(syntax_err)
            self.report_items['time'] = self.date.strftime("%d.%m.%Y-%H:%M:%S")
        except:
            print('Syntax_analyse_error')

    def runtime_test(self):
        with open(self.file_path) as f:
            try:
                eval(compile(f.read(), '', 'exec'))
            except:
                trace = traceback.format_exc()
                up_tarace = []
                for tr in trace.split('\n'):
                    if tr != '':
                        up_tarace.append(tr.replace('  ', ''))
                up_tarace[3] = up_tarace[3].replace('""', self.file)
                self.report_items['runtime_errors'] = '\n'.join(up_tarace[3:])

    def __del__(self):
        for index, value in self.report_items.items():
            self.report_items[index] = [value]
            # print(value)
        self.excel_writer()
        print(self.report_items)


def main():
    test = Tester('erors_file.py')
    test.syntax_test()
    test.runtime_test()
    del test
    # test.runtime_test()

    # os.startfile(r"C:\Users\yaroh\OneDrive\Рабочий стол\123.xlsx")
    # xl=pd.read_excel(r"C:\Users\yaroh\OneDrive\Рабочий стол\123.xlsx", index_col=0)
    # xl.to_excel('new_xl.xlsx')
    # pd.DataFrame()
    # print(xl)


if __name__ == '__main__':
    main()