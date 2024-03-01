import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from openpyxl import load_workbook

def load_excel_data(file_path):
    """
    Load data from an Excel file and return the DataFrame.
    """
    workbook = load_workbook(file_path)
    sheet = workbook.active
    post_title = sheet['B1'].value
    post_text = sheet['B2'].value
    df = pd.read_excel(file_path, header=4)
    return df, post_title, post_text

def preprocess_data(df):
    """
    Preprocess the DataFrame by converting 'Comment Timestamp' to datetime format without time,
    removing the first 4 rows, and resetting the index.
    """
    df['Comment Timestamp'] = pd.to_datetime(df['Comment Timestamp']).dt.date
    df = df.iloc[3:].reset_index(drop=True)
    return df

def analyze_data(df):
    """
    Analyze the data and return the appropriate x and y values for plotting.
    """
    if df['Comment Timestamp'].nunique() > 10:
        df.set_index('Comment Timestamp', inplace=True)
        comments_per_week = df.resample('W').size()
        comments_per_week_df = comments_per_week.reset_index(name='Comments Count')
        comments_per_week_df['Week Start'] = comments_per_week_df['Comment Timestamp'].dt.to_period('W').apply(lambda r: r.start_time)
        comments_per_week_df['Week End'] = comments_per_week_df['Comment Timestamp'].dt.to_period('W').apply(lambda r: r.end_time)
        comments_per_week_df['Week Range'] = comments_per_week_df.apply(lambda row: f"{row['Week Start'].strftime('%d/%b/%Y')} - {row['Week End'].strftime('%d/%b/%Y')}", axis=1)
        x = comments_per_week_df['Week Range']
        y = comments_per_week_df['Comments Count']
    else:
        comments_per_day = df.groupby(df['Comment Timestamp']).size()
        comments_per_day_df = comments_per_day.reset_index(name='Comments Count')
        comments_per_day_df['Comment Timestamp'] = pd.to_datetime(comments_per_day_df['Comment Timestamp'])
        x = comments_per_day_df['Comment Timestamp']
        y = comments_per_day_df['Comments Count']
    return x, y

def plot_data(x, y, post_title, post_text):
    """
    Plot the data with appropriate labels and titles.
    """
    plt.figure(figsize=(12, 7))
    plt.plot(x, y, marker='o', linestyle='-', color='teal')
    plt.title('Post Engagement', fontsize=14, fontweight='bold', pad=15)
    plt.figtext(0.5, 0.85, f'Post Title: {post_title}\n Post Text:{post_text}', fontsize=8, ha='center', fontweight='bold')
    plt.xlabel('Date Range', fontsize=10, fontweight='bold')
    plt.ylabel('Number of Comments', fontsize=10, fontweight='bold')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.subplots_adjust(top=0.75)
    plt.xticks(rotation=45, fontsize=8)
    plt.yticks(fontsize=8)
    plt.show()

def analyze_post_engament(file_path):
    """
    Analyze and plot data from an Excel file.
    """
    df, post_title, post_text = load_excel_data(file_path)
    df = preprocess_data(df)
    x, y = analyze_data(df)
    plot_data(x, y, post_title, post_text)

# Example usage:
# file_path = '../Input_Output/Autism_Parenting_Post_comments/11dmdku.xlsx'
# analyze_post_engament(file_path)
