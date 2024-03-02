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

def generate_emotional_category_narrative(category, count, total_posts, average_sentiment_score):
    sentiment_trend = "predominantly positive" if average_sentiment_score > 0 else "mostly negative"
    percentage_of_total = (count / total_posts) * 100

    narratives = {
        'Supportive': f"Under 'Supportive', {count} posts ({percentage_of_total:.2f}%) reflect the community's backbone, offering encouragement and solidarity. Its {sentiment_trend} sentiment underscores a strong culture of upliftment and mutual support.",
        'Empathetic': f"'Empathetic' category, with {count} posts ({percentage_of_total:.2f}%), highlights the community's ability to understand and share the feelings of others. This {sentiment_trend} sentiment demonstrates deep connections and shared experiences.",
        'Advice': f"The 'Advice' category, including {count} posts ({percentage_of_total:.2f}%), showcases the community's collective wisdom and guidance. The {sentiment_trend} sentiment here indicates a proactive approach towards problem-solving and support.",
        'Negative Behavior': f"With {count} posts ({percentage_of_total:.2f}%), 'Negative Behavior' candidly represents the community's challenges and conflicts. The {sentiment_trend} sentiment reveals the need for empathy and conflict resolution skills within dialogues.",
        'Experience': f"'Experience', with {count} posts ({percentage_of_total:.2f}%), serves as a repository of personal stories and lessons learned, offering invaluable insights. The {sentiment_trend} sentiment enriches the community's knowledge base and empathy.",
        'Curiosity': f"'Curiosity', encompassing {count} posts ({percentage_of_total:.2f}%), reflects the community's desire for learning and understanding. This {sentiment_trend} sentiment fosters a culture of inquiry and growth.",
        'Gratitude': f"The 'Gratitude' category, with {count} posts ({percentage_of_total:.2f}%), celebrates the appreciation and thankfulness within the community. Its {sentiment_trend} sentiment strengthens communal bonds and positive interactions.",
        'Encouragement': f"'Encouragement', including {count} posts ({percentage_of_total:.2f}%), highlights motivational messages and uplifting content. The {sentiment_trend} sentiment in this category inspires hope and resilience.",
        'Confusion': f"With {count} posts ({percentage_of_total:.2f}%), 'Confusion' addresses the uncertainties and questions shared by community members. The {sentiment_trend} sentiment indicates the community's role in clarifying doubts and fostering understanding.",
        'Joy': f"The 'Joy' category, featuring {count} posts ({percentage_of_total:.2f}%), encapsulates moments of happiness and celebration. This {sentiment_trend} sentiment showcases the community's capacity for joy and positive celebrations."
    }

    return narratives.get(category, f"This category, with {count} posts ({percentage_of_total:.2f}%), showcases a unique aspect of the community's emotional landscape, characterized by a {sentiment_trend} sentiment.")

def calculate_average_sentiment_for_category(category, sentiment_scores):
    """
    Calculate the average sentiment score for a given category.

    :param category: The category for which to calculate the average sentiment score.
    :param sentiment_scores: A dictionary with categories as keys and lists of sentiment scores as values.
    :return: The average sentiment score for the category.
    """
    scores = sentiment_scores.get(category, [])
    if not scores:
        return 0  # Return 0 if there are no scores to avoid division by zero
    average_score = sum(scores) / len(scores)
    return average_score


def summarize_comments_insights(sentiment_counts, combined_text):
    total_posts = sum(sentiment_counts.values())

    # Prepare the detailed emotion HTML content
    detailed_emotion_html = "<ul><h4>Comments Emotional Insights</h4>"
    for category, count in sentiment_counts.items():
        # Assume function to calculate average sentiment score for the category
        average_sentiment_score = calculate_average_sentiment_for_category(category, combined_text)
        narrative = generate_emotional_category_narrative(category, count, total_posts, average_sentiment_score)
        detailed_emotion_html += f"<li><h4>{category}:</h4><p>{narrative}</p></li>"
    
    detailed_emotion_html += "</ul>"
    return detailed_emotion_html


def generate_comments_predictive_insights(sentiment_counts):
    # Example predictive insights based on sentiment counts
    most_common_category = max(sentiment_counts, key=sentiment_counts.get)
    predictive_text = f"Given the prominence of '{most_common_category}' in discussions, we foresee a continued focus on this theme. It reflects a critical area of collective interest and support within the community."
    return predictive_text

def generate_comments_summary(sentiment_counts):
    total_posts = sum(sentiment_counts.values())
    summary_text = f"Across {total_posts} comments, the community has showcased a rich diversity of emotional expressions. This analysis highlights the critical role of empathy, support, and shared experiences in fostering a vibrant and caring community."
    return summary_text


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
    
    combined_text= ""
    
    for file_path in directory_path.glob('*.xlsx'):
        df = pd.read_excel(file_path, skiprows=4)
        sentiment_counts =  process_comments_general(df, expanded_keywords)
        
        combined_text = combined_text + '\n' + df[['Comment Text']].fillna('').apply(lambda x: x['Comment Text'], axis=1)
        
        print(total_sentiment_counts, "before")
        # Add the counts from this file to the total counts
        for category, count in sentiment_counts.items():
            total_sentiment_counts[category] += count
        print(total_sentiment_counts, "after")
    
    

    visualize_sentiment_counts(total_sentiment_counts, 'Overall Comments Emotional Analysis', showChart)
    
    # Generate insights summary with the updated call
    insights_summary = summarize_comments_insights(total_sentiment_counts, combined_text)
    return insights_summary

def process_one_comment_file_advanced(file_path, expanded_keywords, showChart = True):
    df = pd.read_excel(file_path, skiprows=4)
    sentiment_counts = process_comments_general(df, expanded_keywords)
    visualize_sentiment_counts(sentiment_counts, 'Single File Comments Emotional Analysis', showChart)



# Expanded Keywords Preparation
expanded_keywords = {category: [] for category in original_keywords}
for category, words in original_keywords.items():
    for word in words:
        expanded_keywords[category].extend(get_synonyms(word))


def analyze_all_comment_files(directory_path, showChart = True):
    # directory_path = Path('../Input_Output/Autism_Parenting_Post_comments')
    insights_summary = process_all_comment_files_advanced(directory_path, expanded_keywords, showChart)
    return "emotional_comment_analysis_chart.png", insights_summary
    

def analyze_one_comment_file(file_path, showChart = True):
    # file_path = Path('../Input_Output/Autism_Parenting_Post_comments/11lh28j.xlsx')
    process_one_comment_file_advanced(file_path, expanded_keywords, showChart)



