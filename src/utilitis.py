# generate dates from previous year
def make_previous_date(current_date):
    import datetime

    previous_date = datetime.datetime.strptime(current_date, "%Y-%m-%d")- datetime.timedelta(days=365)
    previous_date = previous_date.strftime("%Y-%m-%d")

    return previous_date

def make_yesterday_date():
    from datetime import date, timedelta
    yesterday = date.today() - timedelta(1)
    yesterday = yesterday.strftime("%Y-%m-%d")

    return yesterday

def make_date_3_month_early(current_date):
    import datetime

    pres_3_m_early_date = datetime.datetime.strptime(current_date, "%Y-%m-%d")- datetime.timedelta(days=90)
    pres_3_m_early_date = pres_3_m_early_date.strftime("%Y-%m-%d")

    return pres_3_m_early_date












# generate each  of metrics separatly

def get_data_dau():
    import pandas as pd


    query = '''


        select `date` as dzien,'poprzedni' as rok , metric_id as metric_id, tags['project_clone'] as project_clone, 
        concat('poprzedni',' ', tags['project_clone']) as tag, value as value
        from metrics.metrics_table
        where tags['gg_id'] = '0' and (tags['project_clone'] = 'project_portal' or tags['project_clone'] = 'project_clones') 
        and `date` >= '{}' and `date` < '{}' and `range` = 1
        and metric_id = 'dau'

         union 
        select `date` as dzien,'obecny' as rok ,  metric_id as metric_id, tags['project_clone'] as project_clone, 
        concat('obecny',' ', tags['project_clone']) as tag,value as value
        from metrics.metrics_table
        where tags['gg_id'] = '0' and (tags['project_clone'] = 'project_portal' or tags['project_clone'] = 'project_clones') 
        and `date` >= '{}' and `date` < '{}' and `range` = 1
        and metric_id in = 'dau'

             '''.format(start_date_1, end_date_1, start_date_2, end_date_2)

    gauss = get_hive_connection()

    df = pd.read_sql(query, gauss)
    # zrobic post _process _ data ....
    df = df.rename(columns={"_u2.dzien": "dzien", "_u2.rok": "rok",
                            "_u2.metric_id": "metric_id", "_u2.project_clone": "project_clone", "_u2.tag": "legenda",
                            "_u2.value": "value"})

    return df
