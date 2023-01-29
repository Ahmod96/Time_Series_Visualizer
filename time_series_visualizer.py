import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col = 0, parse_dates = True)

# Clean data
df = df.loc[(df['value'] > df['value'].quantile(0.025)) & (df['value'] < df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize = (14,6))
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.plot(df.index, df['value'], c='r')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy().reset_index()
    df_bar['date'] = [str(i)[0:7] for i in  list(df_bar['date'])]
    df_bar = df_bar.groupby(['date']).mean()
    df_bar = df_bar['value'].values.tolist()
    df_bar = [0,0,0,0] + df_bar
    df_bar = pd.DataFrame({'2016':df_bar[0:12], 
'2017':df_bar[12:24], 
                           '2018':df_bar[24:36], '2019':df_bar[36:48]},
                            index = ['January', 'February', 'March', 'April', 'May', 'June', 
                            'July', 'August', 'September', 'October', 'November', 'December']).T
  
    # Draw bar plot
    fig, axes = plt.subplots()
    df_bar.plot(kind = 'bar', figsize = (14,6), xlabel = 'Years',  ylabel = 'Average Page Views', ax = axes)
    axes.legend(title = 'Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(figsize = (16, 6), nrows = 1, ncols  = 2)

    sns.boxplot(x = 'year', y = 'value', data = df_box, ax = ax1)
    ax1.set(title = 'Year-wise Box Plot (Trend)',xlabel = 'Year', ylabel = 'Page Views', yticks = range(0, 220000, 20000))

    order = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    xticklabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x = 'month', y = 'value', data = df_box, ax = ax2, order = order)
    ax2.set(title = 'Month-wise Box Plot (Seasonality)',xlabel = 'Month', ylabel = 'Page Views', xticklabels = xticklabels, yticks = range(0, 220000, 20000))

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
