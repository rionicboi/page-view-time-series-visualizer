import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import numpy as np
np.float = float


# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace = True)
# Clean data
upperBound = df['value'].quantile(0.975)
lowerBound = df['value'].quantile(0.025)
df = df[(df['value'] >= lowerBound) & (df['value'] <= upperBound)]

def draw_line_plot():
    # Draw line plot
    ax = df.plot(y = 'value', xlabel= "Date", ylabel= "Page Views", title= "Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    fig = ax.figure

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df1 = df.reset_index()
    df1['year'] = df1['date'].dt.year
    df1['month'] = df1['date'].dt.month_name()

    df_bar = df1.groupby(['year', 'month'])['value'].mean().reset_index()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December']
    df_bar['month'] = pd.Categorical(df_bar['month'], categories = month_order, ordered = True)

    plt.figure(figsize = (10, 10))
    ax = sns.barplot(data = df_bar, x = 'year', y = 'value', hue = 'month', palette = 'tab10')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    plt.legend(loc = 'upper left', title = 'Months')
    fig = ax.figure
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # Adjust figsize as needed

    # Year-wise Box Plot (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Month-wise Box Plot (Seasonality)
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])  # Specify month order
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Adjust layout to prevent overlapping
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
