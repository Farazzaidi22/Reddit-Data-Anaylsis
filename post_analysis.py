import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import category_keyword
from textblob import TextBlob  # Example sentiment analysis library


def generate_category_narrative(category, count, total_posts, average_sentiment_score):
    # Determine sentiment trend
    sentiment_trend = (
        "predominantly positive" if average_sentiment_score > 0 else "mostly negative"
    )
    percentage_of_total = (count / total_posts) * 100

    # Category-specific narratives
    narratives = {
        "Seeking Advice": f"Seeking advice, with {count} posts ({percentage_of_total:.2f}% of total), demonstrates the community's proactive approach to problem-solving and knowledge-sharing. The {sentiment_trend} sentiment suggests that these discussions are often hopeful, focusing on solutions and support.",
        "Expressing Frustration": f"Expressing frustration, represented by {count} posts ({percentage_of_total:.2f}% of total), captures the difficulties and challenges within the autism parenting journey. The {sentiment_trend} sentiment indicates the emotional strain but also the community's resilience in facing these challenges.",
        "Seeking Support": f"Seeking support, with {count} posts, emphasizes the community's need for emotional backing and understanding. This category's {sentiment_trend} sentiment reflects the warmth and solidarity found within these interactions.",
        "Expressing Joy/Happiness": f"With {count} posts, expressing joy and happiness shines a light on the celebratory and positive moments in autism parenting. The {sentiment_trend} sentiment here is a beautiful reminder of the love and joy that permeates this community.",
        "Sharing Success Stories/Accomplishments": f"Sharing success stories and accomplishments, through {count} posts, highlights the achievements and milestones celebrated by the community. The {sentiment_trend} sentiment in these discussions fosters motivation and inspiration among members.",
        "Expressing Gratitude/Thankfulness": f"Expressing gratitude and thankfulness, in {count} posts, underscores the appreciation and recognition of support and kindness within the community. This category's {sentiment_trend} sentiment reinforces the positive impact of gratitude on community morale.",
        "Seeking Empathy/Understanding": f"Seeking empathy and understanding, with {count} posts, reveals the community's desire for deeper connection and mutual understanding. The {sentiment_trend} sentiment highlights the compassionate and empathetic nature of these discussions.",
        "Sharing Inspirational/Motivational Content": f"Sharing inspirational and motivational content, seen in {count} posts, serves as a beacon of hope and encouragement. The {sentiment_trend} sentiment in this category energizes the community, pushing forward with optimism.",
        "Sharing Personal Experiences/Stories": f"Sharing personal experiences and stories, with {count} posts, forms the backbone of the community, offering insights into the lived experiences of autism parenting. The {sentiment_trend} sentiment here deepens the collective understanding and bonds.",
        "Raising Awareness/Education": f"Raising awareness and education, through {count} posts, highlights the community's commitment to spreading knowledge and understanding about autism. This category's {sentiment_trend} sentiment underscores the importance of advocacy and education.",
        "Expressing Concerns/Worries": f"Expressing concerns and worries, with {count} posts, articulates the anxieties and fears prevalent within the community. The {sentiment_trend} sentiment emphasizes the need for support and reassurance in addressing these concerns.",
    }

    return narratives.get(
        category,
        "This category represents a unique aspect of the autism parenting experience, showcasing diverse emotions and perspectives.",
    )


def generate_predictive_insights(category_counts, average_sentiment_scores):
    # Identify categories with significant positive sentiment and high post counts
    positive_focus = sorted(
        [
            (category, count)
            for category, count in category_counts.items()
            if average_sentiment_scores.get(category, 0) > 0
        ],
        key=lambda x: x[1],
        reverse=True,
    )
    # Predict future trends based on current data
    if positive_focus:
        top_positive_category, top_count = positive_focus[0]
        predictive_text = f"With a notable focus on {top_positive_category} ({top_count} posts), showing a constructive and positive approach, the community is likely to deepen discussions in areas that promote positivity and support. This shift towards uplifting content could foster an even more supportive environment."
    else:
        predictive_text = "The community continues to balance a range of emotions, from challenges to triumphs. Moving forward, maintaining this balance will be key to providing comprehensive support."

    return predictive_text


def generate_overall_summary(category_counts, sentiment_scores):
    total_positive_posts = sum(
        1 for scores in sentiment_scores.values() for score in scores if score > 0
    )
    total_negative_posts = sum(
        1 for scores in sentiment_scores.values() for score in scores if score < 0
    )
    total_posts = sum(category_counts.values())
    summary_text = (
        "The emotional pattern analysis uncovers the rich spectrum of sentiments within the autism parenting community. "
        f"Across {total_posts} analyzed posts, there's a dynamic interplay of joy, frustration, support, and advice-seeking, "
        "reflecting the multifaceted nature of the autism parenting journey. "
        f"The community's leaning towards {total_positive_posts} positive expressions underscores a foundational optimism, "
        f"while {total_positive_posts} instances of shared challenges highlight the importance of solidarity and mutual support. "
        f"This emotional diversity not only strengthens the community fabric but also ensures a broad spectrum of experiences and perspectives are valued and explored."
    )
    return summary_text


def summarize_emotional_insights_html(category_counts, combined_text, sentiment_scores):
    total_posts = sum(category_counts.values())

    detailed_emotion_html = "<ul><h4>Emotional Pattern Insights</h4>"
    for category, count in category_counts.items():
        percentage = (count / total_posts) * 100
        # Calculate the average sentiment score for the category
        average_sentiment_score = (
            sum(sentiment_scores[category]) / len(sentiment_scores[category])
            if sentiment_scores[category]
            else 0
        )
        # Generate detailed narrative for the category
        category_narrative = generate_category_narrative(
            category, count, total_posts, average_sentiment_score
        )

        detailed_emotion_html += (
            f"<li><h4>Category: {category}</h4>"
            f"<p>{category_narrative} This makes up {percentage:.2f}% of total posts, indicating its significance within the community dialogue.</p></li>"
        )

    detailed_emotion_html += "</ul>"

    # Calculate average sentiment scores for each category
    average_sentiment_scores = {
        category: sum(scores) / len(scores) if scores else 0
        for category, scores in sentiment_scores.items()
    }

    # Generate predictive insights and overall summary
    predictive_insights = generate_predictive_insights(
        category_counts, average_sentiment_scores
    )
    overall_summary = generate_overall_summary(category_counts, sentiment_scores)

    # Compile the complete HTML content
    full_analysis_html = (
        f"{detailed_emotion_html}"
        f"<h4>Predictive Insights</h4><p>{predictive_insights}</p>"
        f"<h4>Overall Summary</h4><p>{overall_summary}</p>"
    )

    return full_analysis_html


def emotional_pattern_analysis(file_path, showChart=True):
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
        "Seeking Advice": category_keyword.advice_keywords,
        "Expressing Frustration": category_keyword.frustration_keywords,
        "Seeking Support": category_keyword.support_keywords,
        "Expressing Joy/Happiness": category_keyword.joy_keywords,
        "Sharing Success Stories/Accomplishments": category_keyword.success_keywords,
        "Expressing Gratitude/Thankfulness": category_keyword.gratitude_keywords,
        "Seeking Empathy/Understanding": category_keyword.empathy_keywords,
        "Sharing Inspirational/Motivational Content": category_keyword.information_keywords,
        "Sharing Personal Experiences/Stories": category_keyword.personal_keywords,
        "Raising Awareness/Education": category_keyword.awareness_keywords,
        "Expressing Concerns/Worries": category_keyword.concern_keywords,
    }

    # Initialize counts for each emotional category
    category_counts = {category: 0 for category in additional_categories}
    category_counts["Neutral"] = 0  # Initialize count for neutral titles

    combined_text = (
        df[["Post Title", "Post Text"]]
        .fillna("")
        .apply(lambda x: x["Post Title"] + " " + x["Post Text"], axis=1)
    )

    # Perform sentiment analysis and count occurrences of specific sentiment-related keywords
    for title in combined_text:
        sentiment_score = sia.polarity_scores(str(title))["compound"]
        if sentiment_score == 0:  # If sentiment score is exactly 0, consider it neutral
            category_counts["Neutral"] += 1
        else:
            categorized = False
            for category, keywords in additional_categories.items():
                if check_sentiment_keywords(title, keywords):
                    category_counts[category] += 1
                    categorized = True
                    break
            if not categorized:
                category_counts[
                    "Neutral"
                ] += 1  # If not categorized, consider it neutral

    # Create a bar plot with improved styling
    categories = list(category_counts.keys())
    counts = list(category_counts.values())

    plt.figure(figsize=(10, 8))

    # Color Mapping
    color_mapping = {
        "Neutral": "grey",
        "Expressing Frustration": "red",
        "Seeking Advice": "blue",
        "Seeking Support": "green",
        "Expressing Joy/Happiness": "yellow",
        "Sharing Success Stories/Accomplishments": "gold",
        "Expressing Gratitude/Thankfulness": "lightblue",
        "Seeking Empathy/Understanding": "lightgreen",
        "Sharing Inspirational/Motivational Content": "orange",
        "Sharing Personal Experiences/Stories": "purple",
        "Raising Awareness/Education": "darkblue",
        "Expressing Concerns/Worries": "darkgrey",
    }

    # Assign colors based on categories
    colors = [
        color_mapping.get(category, "blue") for category in categories
    ]  # Default to 'blue' if category color not defined

    bars = plt.bar(categories, counts, color=colors)

    # Add data labels
    for bar in bars:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2, yval + 0.1, round(yval, 2), va="bottom"
        )

    plt.xlabel("Sentiment Categories")
    plt.ylabel("Number of Post Titles")
    plt.title("Emotional Pattern Analysis of Post Titles")
    plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to prevent overlapping
    # Save the plot as an image file
    plt.savefig("./graphs/emotional_pattern_analysis_chart.png")
    if showChart:
        plt.show()

    # Initialize sentiment scores dictionary
    sentiment_scores = {
        topic: [] for topic in category_counts
    }  # Store sentiment scores for each topic

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
            sentiment_scores["Neutral"].append(post_sentiment)

    # Convert list of sentiment scores to an average score per topic for simplicity
    average_sentiment_scores = {
        topic: sum(scores) / len(scores) if scores else 0
        for topic, scores in sentiment_scores.items()
    }

    print(sentiment_scores, "sentiment_scores")
    print(average_sentiment_scores, "average_sentiment_scores")

    # Generate insights summary with the updated call
    insights_summary = summarize_emotional_insights_html(
        category_counts, combined_text, sentiment_scores
    )

    return "emotional_pattern_analysis_chart.png", insights_summary


# Call the function with the file path as an argument
# emotional_pattern_analysis("../Input_Output/autism_parenting_data_last_year.xlsx")
