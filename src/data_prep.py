def get_data():
    import pandas as pd


    query = '''


        select `date` as dzien,'poprzedni' as rok , metric_id as metric_id, tags['project_clone'] as project_clone, 
        concat('poprzedni',' ', tags['project_clone']) as tag, value as value
        from metrics.metrics_table
        where tags['gg_id'] = '0' and (tags['project_clone'] = 'project_portal' or tags['project_clone'] = 'project_clones') 
        and `date` >= '{}' and `date` < '{}' and `range` = 1
        and metric_id in (  'dau', 'mau', 'monthly_paying_users',
         'gross_revenue_brutto','daily_paying_users', 'arppu')

         union 
        select `date` as dzien,'obecny' as rok ,  metric_id as metric_id, tags['project_clone'] as project_clone, 
        concat('obecny',' ', tags['project_clone']) as tag,value as value
        from metrics.metrics_table
        where tags['gg_id'] = '0' and (tags['project_clone'] = 'project_portal' or tags['project_clone'] = 'project_clones') 
        and `date` >= '{}' and `date` < '{}' and `range` = 1
        and metric_id in ( 'new_users', 'dau', 'mau', 'monthly_paying_users',
         'gross_revenue_brutto','daily_paying_users', 'arppu')
         union
         select `date` as dzien,'poprzedni' as rok ,  metric_id as metric_id, tags['project_clone'] as project_clone, 
        concat('poprzedni',' ', tags['project_clone']) as tag, value/60 as value
        from metrics.metrics_table
        where tags['gg_id'] = '0' and (tags['project_clone'] = 'project_portal' or tags['project_clone'] = 'project_clones') 
        and `date` >= '{}' and `date` < '{}' and `range` = 1
        and metric_id in ( 'average_session_time')

         union 
        select `date` as dzien,'obecny' as rok ,    metric_id as metric_id, tags['project_clone'] as project_clone, 
        concat('obecny',' ', tags['project_clone']) as tag,value/60 as value
        from metrics.metrics_table
        where tags['gg_id'] = '0' and (tags['project_clone'] = 'project_portal' or tags['project_clone'] = 'project_clones') 
        and `date` >= '{}' and `date` < '{}' and `range` = 1
        and metric_id in ( 'average_session_time')

        union
         select `date` as dzien,'poprzedni' as rok ,  'gross_revenue_brutto_rolling' as metric_id, tags['project_clone'] as project_clone, 
        concat('poprzedni',' ', tags['project_clone']) as tag, value as value
        from metrics.metrics_table
        where tags['gg_id'] = '0' and (tags['project_clone'] = 'project_portal' or tags['project_clone'] = 'project_clones') 
        and `date` >= '{}' and `date` < '{}' and `range` = 30
        and metric_id in ( 'gross_revenue_brutto')

        union
        select `date` as dzien ,'obecny' as rok ,  'gross_revenue_brutto_rolling' as metric_id, tags['project_clone'] as project_clone, 
        concat('obecny',' ', tags['project_clone']) as tag, value as value
        from metrics.metrics_table
        where tags['gg_id'] = '0' and (tags['project_clone'] = 'project_portal' or tags['project_clone'] = 'project_clones') 
        and `date` >= '{}' and `date` < '{}' and `range` = 30
        and metric_id in ( 'gross_revenue_brutto')

        union
        select a.dzien as dzien,'poprzedni' as rok , a.metric_id as metric_id, 'project_clones' as project_clone, 
        concat('poprzedni',' ', 'project_clones') as tag, (b.value-a.value) as value
        from ((select `date` as dzien,'poprzedni' as rok ,  metric_id as metric_id, tags['project_clone'] as project_clone, 
        concat('poprzedni',' ', tags['project_clone']) as tag, value as value
        from metrics.metrics_table
        where tags['gg_id'] = '0' and tags['project_clone'] = 'project_portal' 
        and `date` >= '{}' and `date` < '{}' and `range` = 1
        and metric_id in ('new_users')) as a
        join (
        select  `date` as dzien , value as value
        from metrics.metrics_table
        where tags['gg_id'] = '0' and tags['project_clone'] = 'project_with_clones' and  metric_id in ('new_users') 
        and `date` >= '{}' and `date` < '{}' and `range` = 1) as b on a.dzien=b.dzien
        ) 
        union
        select `date` as dzien ,'poprzedni' as rok ,  metric_id as metric_id, tags['project_clone'] as project_clone, 
        concat('poprzedni',' ', tags['project_clone']) as tag, value as value
        from metrics.metrics_table
        where tags['gg_id'] = '0' and tags['project_clone'] = 'project_portal' 
       and `date` >= '{}' and `date` < '{}' and `range` = 1
        and metric_id in ('new_users') 



             '''.format(start_date_prev_year, end_date_prev_year, start_date_present, end_date_present,
                        start_date_prev_year, end_date_prev_year, start_date_present,
                        end_date_present, start_date_prev_year, end_date_prev_year,start_date_present,
                        end_date_present, start_date_prev_year, end_date_prev_year, start_date_prev_year,
                        end_date_prev_year, start_date_prev_year,
                        end_date_prev_year)

    gauss = get_hive_connection()

    df = pd.read_sql(query, gauss)
    # zrobic post _process _ data ....
    df = df.rename(columns={"_u8.dzien": "dzien", "_u8.rok": "rok",
                            "_u8.metric_id": "metric_id", "_u8.project_clone": "project_clone", "_u8.tag": "legenda",
                            "_u8.value": "value"})

    return df

