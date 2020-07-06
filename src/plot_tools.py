def create_helping_parametr(df):
    import pandas as pd

    return pd.date_range(start=df.dzien.min(), end=df.dzien.max(), freq='7D')


def create_positoning_vector(l):
    positioning_vector = []

    for i in xrange(len(l)):
        positioning_vector.append(i * 7)

    return positioning_vector


def make_plot_from_metrics(df, metric_id, tekst, title_name):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import matplotlib.dates as mdates
    import matplotlib.ticker as ticker


    sns.set(style="darkgrid")
    sns.set(rc={'figure.figsize': (15, 12)})

    ax = plt.gca()
    ax.xaxis_date()

    # plotting
    # style="project_clone", style_order=['project_portal', 'project_clones']
    df1 = df[(df.loc[:, 'rok'] == 'obecny') & (df.loc[:, 'metric_id'] == metric_id)]
    ax = sns.lineplot(x="dzien", y="value", hue="legenda", hue_order=['obecny project_clones',
                                                                      'obecny project_portal'],
                      data=df1, palette=['orangered', 'navy'], legend=False)
    plt.legend(loc='lower center', bbox_to_anchor=(.3, 0), ncol=6, fontsize=15,
               labels=['obecny project_portal', 'obecny project_clones'])
    sns.despine(left=True, bottom=True)

    plt.xticks(fontsize=12, rotation=90)
    plt.title(tekst, fontsize=20)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%d'))



    ax.set(xlabel="", ylabel="")
    # ax.set_ylim([0,None])

    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    # Put the legend out of the figure
    df2 = df[(df.loc[:, 'rok'] == 'poprzedni') & (df.loc[:, 'metric_id'] == metric_id)]

    ax2 = ax.twiny()

    ax2 = sns.lineplot(x="dzien", y="value", hue="legenda"
                       , hue_order=['poprzedni project_clones',
                                    'poprzedni project_portal'],
                       data=df2, palette=['orangered', 'navy'], dashes=[(2, 2, 2, 2), (2, 2, 2, 2)],
                       ax=ax2, legend=False)

    ax2.set_xticklabels(ax.get_xticklabels())
    ax2.set(xlabel="", ylabel="")
    ax2.set_ylim([0, None])
    # ax.set_visible(False)

    ax2.lines[0].set_linestyle("--")
    ax2.lines[1].set_linestyle("--")

    plt.legend(loc='lower center', bbox_to_anchor=(.7, 0), ncol=6, fontsize=15,
               labels=['poprzedni project_clones',
                       'poprzedni project_portal'])
    plt.tight_layout()
    plt.savefig(title_name + '.png')
    plt.close()


def make_image(df):
    dict = {'new_users': 'Nowe rejestracje dla Firma.com i klonów',
            'average_session_time': 'Średni czas sesji dla Firma.com i klonów',
            'dau':
                'Aktywni użytkownicy dla Firma.com i klonów', 'gross_revenue_brutto_rolling':
                'Przychód miesięczny brutto - rolling dla Firma.com i klonów', 'gross_revenue_brutto':
                'Przychód dzienny brutto dla Firma.com i klonow',
            'daily_paying_users': 'Dziennie płacący uzytkownicy dla Firma i klonów',
            'monthly_paying_users': 'Miesięcznie płacący użytkownicy dla Firma.com i klonów',
            'arppu': 'Średni przychód na płacącego użytkownika dla Firma.com i klonów '}

    for k, v in dict.items():
        make_plot_from_metrics(df, k, v, k)

def make_pdf():

    from fpdf import FPDF

    class PDF(FPDF):
        def header(self):
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Move to the right
            self.cell(80)
            # Title
            # Line break
            self.ln(20)

        # Page footer
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Page number
            self.cell(0, 10, 'Strona ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


    import datetime

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page(orientation='Lor')
    #pdf.image('05_Firma_LOGO_H_W.png', x=None, y=None, w=0, h=90, type='', link='')
    pdf.cell(0, 10, 'Firma Websites', 0, 1, 'C')
    pdf.cell(0, 10, 'KPI`s Review #' , 0, 1, 'C')
    pdf.cell(0, 10, 'Firma Sp. z o.o. ', 0, 1)
    pdf.cell(0, 10, 'Autor : Joanna Podsadna ', 0, 1)
    pdf.cell(0, 10, 'Krakow, ' + str(datetime.datetime.now().strftime("%Y-%m-%d")), 0, 1)

    images = ['new_users.png', 'average_session_time.png', 'dau.png', 'gross_revenue_brutto_rolling.png',
              'gross_revenue_brutto.png', 'daily_paying_users.png', 'monthly_paying_users.png', 'arppu.png']
    for image in images:
        pdf.image(image, x=None, y=None, w=280, h=160, type='', link='')
    pdf.output('out/kpi_report_' + str(datetime.datetime.now().strftime("%Y-%m-%d")) + '.pdf', 'F')