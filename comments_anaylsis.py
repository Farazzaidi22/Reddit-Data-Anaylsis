# Import statements and NLTK corpus downloads
import nltk
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from nltk.corpus import wordnet as wn

# Download necessary NLTK resources
nltk.download('wordnet')
nltk.download('omw-1.4')

# Data Definitions
original_keywords = {
    'Supportive': ['support', 'well done', 'good job', 'keep it up', 'That’s huge'],
    'Empathetic': ['understand', 'feel', 'heart', 'empathy'],
    'Advice': ['suggest', 'recommend', 'you should', 'you could', "helping"],
    'Negative Behavior': ['stupid', 'idiot', 'dumb', 'useless', 'harass', 'annoy', 'bother', 'disturb'],
    'Experience': ['when I', 'I have', 'my experience', 'I felt', 'remember', 'exactly the same'],
    'Curiosity': ['wonder', 'question', 'inquire', 'curious'],
    'Gratitude': ['thankful', 'grateful', 'appreciate', 'thanks'],
    'Encouragement': ['motivate', 'encourage', 'inspire', 'uplift'],
    'Confusion': ['confused', 'puzzled', 'uncertain', 'bewildered'],
    'Joy': ['happy', 'joy', 'pleasure', 'delight', 'Congratulations', 'Congrats', 'great feeling'],
}

color_mapping = {
    'Neutral': 'grey',
    'Empathetic': '#C2577C',
    'Supportive': 'green',
    'Advice': 'blue',
    'Negative Behavior': 'red',
    'Experience': 'purple',
    'Curiosity': 'gold',
    'Gratitude': 'lightblue',
    'Encouragement': 'orange',
    'Confusion': 'yellow',
    'Joy': 'lightgreen',
}

# Utility Functions
def get_synonyms(word):
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
            if len(synonyms) >= 500:
                break
    return list(synonyms)



# Analysis Functions
def classify_comment_advanced(comment, expanded_keywords):
    comment_lower = comment.lower()
    for category, key_list in expanded_keywords.items():
        if any(keyword in comment_lower for keyword in key_list):
            return category
    return 'Neutral'

def process_comments_general(df, expanded_keywords):
    sentiment_categories = list(expanded_keywords.keys()) + ['Neutral']
    sentiment_counts = {category: 0 for category in sentiment_categories}
    comments = df['Comment Text'].dropna()
    for comment in comments:
        sentiment = classify_comment_advanced(comment, expanded_keywords)
        sentiment_counts[sentiment] += 1
    return sentiment_counts

def visualize_sentiment_counts(sentiment_counts, title, showChart = True):
    
    # Create a bar plot with improved styling
    categories = list(sentiment_counts.keys())
    counts = list(sentiment_counts.values())
    
    colors = [color_mapping.get(category, 'blue') for category in sentiment_counts.keys()]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, counts, color=colors)
    
    # Add data labels
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, round(yval, 2), va='bottom')
        
    plt.xlabel('Sentiment Category')
    plt.ylabel('Count')
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Save the plot as an image file
    plt.savefig('emotional_comment_analysis_chart.png')
    if showChart:
        plt.show()



# Main Functions
def process_all_comment_files_advanced(directory_path, expanded_keywords, showChart = True):
    
    # Initialize sentiment_counts with all categories, including 'Neutral', set to 0
    sentiment_categories = list(expanded_keywords.keys()) + ['Neutral']
    total_sentiment_counts = {category: 0 for category in sentiment_categories}
    
    for file_path in directory_path.glob('*.xlsx'):
        df = pd.read_excel(file_path, skiprows=4)
        sentiment_counts =  process_comments_general(df, expanded_keywords)
        print(total_sentiment_counts, "before")
        # Add the counts from this file to the total counts
        for category, count in sentiment_counts.items():
            total_sentiment_counts[category] += count
        print(total_sentiment_counts, "after")
        
            
    visualize_sentiment_counts(total_sentiment_counts, 'Overall Comments Emotional Analysis', showChart = True)

def process_one_comment_file_advanced(file_path, expanded_keywords):
    df = pd.read_excel(file_path, skiprows=4)
    sentiment_counts = process_comments_general(df, expanded_keywords)
    visualize_sentiment_counts(sentiment_counts, 'Single File Comments Emotional Analysis', showChart = True)



# Expanded Keywords Preparation
expanded_keywords = {category: [] for category in original_keywords}
for category, words in original_keywords.items():
    for word in words:
        expanded_keywords[category].extend(get_synonyms(word))


def analyze_all_comment_files(directory_path, showChart = True):
    # directory_path = Path('../Input_Output/Autism_Parenting_Post_comments')
    process_all_comment_files_advanced(directory_path, expanded_keywords, showChart = True)
    return "emotional_comment_analysis_chart.png"
    

def analyze_one_comment_file(file_path):
    # file_path = Path('../Input_Output/Autism_Parenting_Post_comments/11lh28j.xlsx')
    process_one_comment_file_advanced(file_path, expanded_keywords)



