import matplotlib.pyplot as plt
import wget
import pandas as pd
import os
import numpy as np

filelist = [ f for f in os.listdir(os.getcwd()) if f.endswith(".csv") ]
for f in filelist:
    os.remove(os.path.join(os.getcwd(), f))

URL = 'https://docs.google.com/spreadsheets/d/1nCNc1TwCi3XKPzmFTA1oVVBx1zR5Q8YHYAvTmTt65cQ/export?format=csv&gid=0'
filename = wget.download(URL)
df = pd.read_csv(filename)
Date = df.columns[0]
TotalTime = df.columns[1]
TimeStudied = df.columns[2]
PercentageTime = df.columns[3]
Topic = df.columns[4]

def preprocess_time_string(time_str):
    parts = time_str.split(':')
    # Pad the hour component with a leading zero if it has less than two digits
    if len(parts[0]) < 2:
        parts[0] = '0' + parts[0]
    return ':'.join(parts)

df[Date] = pd.to_datetime(df[Date])
df[TotalTime] = pd.to_timedelta(df[TotalTime].apply(lambda td: pd.Timedelta(preprocess_time_string(str(td)))))
df[TimeStudied] = pd.to_timedelta(df[TimeStudied].apply(lambda td: pd.Timedelta(preprocess_time_string(str(td)))))
df = df[df[Date] > pd.to_datetime('2024-01-13')]
def plot_daily_study_time():
    daily_study_time = df.groupby(Date)[TimeStudied].sum()

    # Convert 'TimeStudied' from Timedelta to total minutes for plotting
    daily_study_time_hours = daily_study_time.dt.total_seconds() / 3600  # Converts to minutes

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(daily_study_time_hours.index,daily_study_time_hours)

    plt.title('Total Time Studied Each Day')
    plt.xlabel('Date')
    plt.ylabel('Total Time Studied (Hours)')
    plt.axhline(y = 4.0, linestyle='-', label = 'target', color='red')
    plt.ylim(0, 6.0)
    plt.xticks(rotation=90)  # Rotate the date labels for readability
    plt.tight_layout()
    plt.legend()
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.show()


def plot_average_focus_time():
    weighted_sum = df.groupby(Topic).apply(lambda x: (x[PercentageTime] * x[TotalTime].dt.total_seconds()).sum())
    total_time_per_topic = df.groupby(Topic)[TotalTime].sum().dt.total_seconds()
    weighted_avg_study_percent = weighted_sum / total_time_per_topic

    # Sorting the weighted average study percentages in decreasing order
    sorted_weighted_avg_study_percent = weighted_avg_study_percent.sort_values(ascending=False)

    # Plotting the bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(sorted_weighted_avg_study_percent.index, sorted_weighted_avg_study_percent, color='skyblue')

    plt.title('Weighted Average Study Time Percentage by Topic (Since college started)')
    plt.xlabel('Topic')
    plt.ylabel('Weighted Average Study Time (%)')
    plt.xticks(rotation=90)  # Rotate the topic labels for readability
    plt.grid(axis='y')
    plt.ylim([0.8, sorted_weighted_avg_study_percent.max() + 0.1])  # Setting the y-axis to start at 0.8
    plt.tight_layout()

    plt.show()

def plot_daily_study_time_by_topic():
    # Grouping the data by Date and Topic and summing up TimeStudied
    grouped_data = df.groupby([Date, Topic])[TimeStudied].sum().reset_index()

    # Convert 'TimeStudied' from Timedelta to total hours
    grouped_data[TimeStudied] = grouped_data[TimeStudied].dt.total_seconds() / 3600

    # Pivoting the data for plotting
    pivot_data = grouped_data.pivot(index=Date, columns=Topic, values=TimeStudied).fillna(0)

    # Create a complete date range for the dataset
    date_range = pd.date_range(start=pivot_data.index.min(), end=pivot_data.index.max())

    # Reindex the pivot table to include the full date range, filling missing values with 0
    pivot_data = pivot_data.reindex(date_range, fill_value=0)

    # Format the dates to exclude the time component
    pivot_data.index = pivot_data.index.date

    # Plotting the stacked bar graph
    plt.figure(figsize=(10, 6))
    pivot_data.plot(kind='bar', stacked=True, ax=plt.gca(), legend=False)
    plt.axhline(y=4.0, linestyle='-', label='target', color='red')
    plt.title('Daily Study Time by Topic')
    plt.xlabel('Date')
    plt.ylabel('Total Time Studied (Hours)')
    plt.xticks(rotation=90)  # Rotate the date labels for readability
    plt.legend(title='Topic', loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.show()

plot_daily_study_time_by_topic()

