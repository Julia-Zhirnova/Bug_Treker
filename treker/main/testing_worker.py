import traceback
from pylint import epylint as lint
import os
from datetime import datetime
import pandas as pd
import shutil
import subprocess
from .models import Progs, Syntax, Runtime


class Tester(object):
    def __init__(self, filename, version, prg_id):
        super(Tester, self).__init__()
        self.file = filename
        self.file_path = os.path.join(os.getcwd(), 'main', 'user_files', self.file.replace('.py', ''), self.file)
        self.date = datetime.now()
        self.report_file = os.path.join(os.getcwd(), 'main', 'user_files', self.file.replace('.py', '')
                                        , 'Report_' + self.file.replace('.py', '.xlsx'))
        self.sample_path = os.path.join(os.getcwd(), 'main', 'user_files', 'sample_report.xlsx')

        try:
            open(os.path.join(os.getcwd(), 'main', 'user_files', self.file.replace('.py', ''),
                              'Report_' + self.file.replace('.py', '.xlsx')))
        except:
            shutil.copy2(self.sample_path,
                         os.path.join(os.getcwd(), 'main', 'user_files', self.file.replace('.py', '')))
            os.rename(
                os.path.join(os.getcwd(), 'main', 'user_files', self.file.replace('.py', ''), 'sample_report.xlsx'),
                os.path.join(os.getcwd(), 'main', 'user_files', self.file.replace('.py', ''),
                             'Report_' + self.file.replace('.py', '.xlsx')))

        self.report_items = {}
        self.version = version
        self.pd_frame = self.excel_reader()
        self.prog_id = prg_id

    def excel_reader(self):
        report_pd = pd.read_excel(self.report_file)
        data = {}
        for label, content in report_pd.items():
            self.report_items[label] = ''
        return report_pd

    def excel_writer(self):
        self.report_items['version'] = self.version
        new_pd = self.pd_frame.append(pd.DataFrame(self.report_items), ignore_index=True)
        new_pd.to_excel(self.report_file, index=False)

    def syntax_test(self):
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
        test_s = Syntax(time=self.report_items['time'],
                        version=self.version,
                        prog_id=self.prog_id,
                        err_text=self.report_items['syntax_errors'],
                        count=self.report_items['syntax_count'],
                        score=self.report_items['code_score'],
                        )
        test_s.save()

    def runtime_test(self):
        result = subprocess.run(
            ['python', self.file_path],
            capture_output=True, text=True)
        if result.stderr:
            trace = result.stderr
            up_tarace = []
            for tr in trace.split('\n'):
                if tr != '':
                    up_tarace.append(tr.replace('  ', ''))
            up_tarace[3] = up_tarace[3].replace('""', self.file)
            self.report_items['runtime_errors'] = '\n'.join(up_tarace[3:])
            self.report_items['run_result'] = ''
        else:
            trace = result.stdout
            self.report_items['run_result'] = trace

        test_r = Runtime(time=self.report_items['time'],
                         version=self.version,
                         prog_id=self.prog_id,
                         err_text=self.report_items['runtime_errors'],
                         no_err_text=self.report_items['run_result'],
                         )
        test_r.save()

    def __del__(self):
        for index, value in self.report_items.items():
            self.report_items[index] = [value]
        self.excel_writer()


def main():
    t = Tester('erors_file.py')
    t.syntax_test()
    t.runtime_test()
    print(t.report_items)
    del t


if __name__ == '__main__':
    main()
