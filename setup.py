from setuptools import setup, find_packages
import glob
import os

data_files = []
path_list = glob.glob('data/*/*/*/*', recursive=True)

print(len(path_list))

for path in path_list:
    if os.path.isdir(path):
        print('skipped directory', path)
    elif os.path.isfile(path):
        data_files.append(path)

print(len(data_files))

setup(
    name='gotolong',
    version='0.0.1',
    url='https://github.com/gotolong/gotolong',
    description='An investor stock advisor',
    author='Surinder Kumar',
    author_email='surinder.kumar.xyz@gmail.com',
    install_requires=['Django', 'prettytable'],
    packages=find_packages(),
    scripts=['scripts/gotolong_all_report.sh',
             'scripts/gotolong_amfi_invoke',
             'scripts/gotolong_bhav_invoke',
             'scripts/gotolong_bstmt_invoke.sh',
             'scripts/gotolong_corpact_invoke',
             'scripts/gotolong_daily_report.sh',
             'scripts/gotolong_db_schema_gen.sh',
             'scripts/gotolong_db_schema_install.sh',
             'scripts/gotolong_db_stats.sh',
             'scripts/gotolong_demat_invoke',
             'scripts/gotolong_dividend_invoke.sh'
             'scripts/gotolong_download_move.sh',
             'scripts/gotolong_ftwhl_invoke',
             'scripts/gotolong_gcweight_invoke',
             'scripts/gotolong_isin_invoke',
             'scripts/gotolong_nach_invoke',
             'scripts/gotolong_peqia_invoke',
             'scripts/gotolong_screener_invoke',
             'scripts/gotolong_trendlyne_invoke'
             ],
)
# data_files=[('gotolong_data', data_files)],
