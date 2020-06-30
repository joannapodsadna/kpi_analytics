# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from utilitis import make_previous_date, make_yesterday_date, make_date_3_month_early
from plot_tools import *
from data_prep import get_data

import os
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')




# give a current date
current_date = 'yyyy-mm-dd'
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))



def get_hive_connection():
    import pyodbc
    cnxnstr = 'Driver={/usr/lib/hive/lib/native/Linux-amd64-64/libhortonworkshiveodbc64XXX.so};HOST=masterXXX.hadoop.project;PORT=10000;uid=etl;pwd=etl'
    return pyodbc.connect(cnxnstr, autocommit=True)



if __name__ == "__main__":
    # give start dates
    start_date_present = make_date_3_month_early(current_date)
    end_date_present = current_date
    start_date_prev_year = make_previous_date(start_date_present)
    end_date_prev_year = make_previous_date(end_date_present)
    print('generowanie danych')
    df = get_data()
    print('tworzenie wykresow')
    make_image(df)
    print('tworzenie pdfa')
    make_pdf()
    print('done!')