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
    plt.xticks(rotation=45)  # Rotate the date labels for readability
    plt.grid(True)
    plt.tight_layout()

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

    plt.title('Weighted Average Study Time Percentage by Topic')
    plt.xlabel('Topic')
    plt.ylabel('Weighted Average Study Time (%)')
    plt.xticks(rotation=90)  # Rotate the topic labels for readability
    plt.grid(axis='y')
    plt.ylim([0.8, sorted_weighted_avg_study_percent.max() + 0.1])  # Setting the y-axis to start at 0.8
    plt.tight_layout()

    plt.show()

