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












