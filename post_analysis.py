import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import category_keyword
from textblob import TextBlob  # Example sentiment analysis library


def summarize_emotional_insights_html(category_counts, combined_text, sentiment_scores):
    total_posts = sum(category_counts.values())

    detailed_emotion_html = "<ul><h4>Emotional Pattern Insights</h4>"
    for category, count in category_counts.items():
        percentage = (count / total_posts) * 100
        detailed_emotion_html += (
            f"<li><h4>Category: {category}</h4>"
            f"<p>This category, with <strong>{count} posts</strong> ({percentage:.2f}% of total), "
            f"reflects a specific aspect of the autism parenting community's emotional landscape. "
            f"Understanding these emotional patterns helps in tailoring support and resources effectively.</p></li>"
        )
    
    detailed_emotion_html += "</ul>"
    
    return detailed_emotion_html


def emotional_pattern_analysis(file_path, showChart = True):
    # Load the Excel file into a DataFrame
    df = pd.read_excel(file_path)

    # Initialize SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()

    # Function to check if a post title contains specific keywords related to sentiment
    def check_sentiment_keywords(title, keywords):
        for keyword in keywords:
            if keyword.lower() in title.lower():
                return True
        return False

    # Define additional emotional categories and their keywords
    additional_categories = {
        'Seeking Advice': category_keyword.advice_keywords, 
        'Expressing Frustration': category_keyword.frustration_keywords, 
        'Seeking Support': category_keyword.support_keywords, 
        
        'Expressing Joy/Happiness': category_keyword.joy_keywords, 
        'Sharing Success Stories/Accomplishments': category_keyword.success_keywords,
        
        'Expressing Gratitude/Thankfulness': category_keyword.gratitude_keywords, 
        'Seeking Empathy/Understanding': category_keyword.empathy_keywords, 
        
        'Sharing Inspirational/Motivational Content': category_keyword.information_keywords,
        'Sharing Personal Experiences/Stories': category_keyword.personal_keywords,
        
        'Raising Awareness/Education': category_keyword.awareness_keywords,
        'Expressing Concerns/Worries': category_keyword.concern_keywords,
    }

    # Initialize counts for each emotional category
    category_counts = {category: 0 for category in additional_categories}
    category_counts['Neutral'] = 0  # Initialize count for neutral titles
    
    combined_text = df[['Post Title', 'Post Text']].fillna('').apply(lambda x: x['Post Title'] + ' ' + x['Post Text'], axis=1)

    # Perform sentiment analysis and count occurrences of specific sentiment-related keywords
    for title in combined_text:
        sentiment_score = sia.polarity_scores(str(title))['compound']
        if sentiment_score == 0:  # If sentiment score is exactly 0, consider it neutral
            category_counts['Neutral'] += 1
        else:
            categorized = False
            for category, keywords in additional_categories.items():
                if check_sentiment_keywords(title, keywords):
                    category_counts[category] += 1
                    categorized = True
                    break
            if not categorized:
                category_counts['Neutral'] += 1  # If not categorized, consider it neutral

    # Create a bar plot with improved styling
    categories = list(category_counts.keys())
    counts = list(category_counts.values())

    plt.figure(figsize=(10, 8))
    
    # Color Mapping
    color_mapping = {
        'Neutral': 'grey',
        'Expressing Frustration': 'red',
        
        'Seeking Advice': 'blue', 
        'Seeking Support': 'green', 
        
        'Expressing Joy/Happiness': 'yellow', 
        'Sharing Success Stories/Accomplishments': 'gold',
        
        'Expressing Gratitude/Thankfulness': 'lightblue', 
        'Seeking Empathy/Understanding': 'lightgreen', 
        
        'Sharing Inspirational/Motivational Content': 'orange',
        'Sharing Personal Experiences/Stories': 'purple',
        
        'Raising Awareness/Education': 'darkblue',
        'Expressing Concerns/Worries': 'darkgrey',
    }


    # Assign colors based on categories
    colors = [color_mapping.get(category, 'blue') for category in categories]  # Default to 'blue' if category color not defined
    
    bars = plt.bar(categories, counts, color=colors)

    # Add data labels
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, round(yval, 2), va='bottom')

    plt.xlabel('Sentiment Categories')
    plt.ylabel('Number of Post Titles')
    plt.title('Emotional Pattern Analysis of Post Titles')
    plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to prevent overlapping
    # Save the plot as an image file
    plt.savefig('emotional_pattern_analysis_chart.png')
    if showChart:
        plt.show()
        
    # Initialize sentiment scores dictionary
    sentiment_scores = {topic: [] for topic in category_counts}  # Store sentiment scores for each topic

   # Corrected loop
    for post in combined_text:
        post_sentiment = TextBlob(post).sentiment.polarity
        categorized = False
        for category, keywords in additional_categories.items():
            if check_sentiment_keywords(post, keywords):
                sentiment_scores[category].append(post_sentiment)
                categorized = True
                break
        if not categorized:
            sentiment_scores['Neutral'].append(post_sentiment)

    # Convert list of sentiment scores to an average score per topic for simplicity
    average_sentiment_scores = {topic: sum(scores)/len(scores) if scores else 0 for topic, scores in sentiment_scores.items()}
    
    print(sentiment_scores, "sentiment_scores")
    print(average_sentiment_scores, "average_sentiment_scores")
        
    # Generate insights summary with the updated call
    insights_summary = summarize_emotional_insights_html(category_counts, combined_text, sentiment_scores)

    return "emotional_pattern_analysis_chart.png", insights_summary

# Call the function with the file path as an argument
# emotional_pattern_analysis("../Input_Output/autism_parenting_data_last_year.xlsx")
