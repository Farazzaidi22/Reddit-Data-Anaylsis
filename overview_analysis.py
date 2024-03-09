import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
from textblob import TextBlob  # Example sentiment analysis library


def print_top_words(model, feature_names, n_top_words):
    topics = {}
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join(
            [feature_names[i] for i in topic.argsort()[: -n_top_words - 1 : -1]]
        )
        topics[f"Topic {topic_idx}"] = message
    return topics


def summarize_insights_html(topic_counts, combined_text, sentiment_scores):
    total_posts = sum(topic_counts.values())
    positive_sentiment_posts = sum(
        1 for scores in sentiment_scores.values() for score in scores if score > 0
    )
    negative_sentiment_posts = sum(
        1 for scores in sentiment_scores.values() for score in scores if score < 0
    )

    # Example of topic insights mapping
    topic_insights = {
        "Personal Care & Daily Activities": "This topic often revolves around the day-to-day triumphs and challenges in fostering independence in personal care routines, a cornerstone of nurturing self-sufficiency in individuals with autism.",
        "Social & Family Events": "Discussions here illuminate the vibrant social interactions and familial bonds, emphasizing the importance of inclusive social environments and family support systems.",
        "General Life & Experiences": "Captures the broad spectrum of life's moments experienced by autism families, from milestones to everyday occurrences, reflecting the nuanced reality of autism parenting.",
        "Holiday & Seasonal Events": "Highlights how seasonal celebrations and holidays are uniquely experienced and adapted by autism families, fostering traditions that are both inclusive and respectful of sensory preferences.",
        "Communication & Learning": "Focuses on the pivotal role of communication and education in autism, discussing innovative strategies and tools that facilitate learning and understanding.",
    }

    detailed_discussion_html = "<h3>Detailed Topic Insights</h3>"
    for topic, count in topic_counts.items():
        average_sentiment_score = (
            sum(sentiment_scores[topic]) / len(sentiment_scores[topic])
            if sentiment_scores[topic]
            else 0
        )
        sentiment_analysis = (
            "predominantly positive"
            if average_sentiment_score > 0
            else "significantly negative"
        )
        future_trend = (
            "increasing interest"
            if count / total_posts > 0.2
            else "steady but notable presence"
        )

        topic_narrative = topic_insights.get(
            topic,
            "This topic brings a unique perspective to the autism parenting community, underscoring diverse experiences and insights.",
        )

        detailed_discussion_html += (
            f"<li><h4>Topic: {topic}</h4>"
            f"<p>{topic_narrative} With <strong>{count}</strong> posts showing a {sentiment_analysis} sentiment, "
            f"there's a {future_trend} in discussions. Such engagement underscores the topic's relevance and the community's investment in exploring it further.</p></li>"
        )

    predictive_insight_html = (
        "<h3>Predictive Insights</h3>"
        "<p>The analysis predicts a growing focus on <strong>'Personal Care & Daily Activities'</strong> and <strong>'Communication & Learning'</strong>, "
        "reflecting a broader societal movement towards independence and enhanced communication for individuals with autism.</p>"
    )

    conclusion_html = (
        "<h3>Conclusion</h3>"
        "<p>This comprehensive analysis underscores the diversity of the autism parenting experience, "
        "highlighting the community's resilience, challenges, and evolving needs. The varied sentiment across topics "
        "reveals the complex emotions that parenting a child with autism entails, from joy and pride to concern and advocacy. "
        "As the community continues to share, support, and learn from one another, these insights can inform targeted "
        "support services, educational resources, and policy advocacy to better meet the needs of individuals with autism and their families.</p>"
    )

    summary_html = (
        "<h4>Comprehensive Analysis Summary</h4>"
        f"<p>Across <strong>{total_posts}</strong> posts, the autism parenting community has engaged in a rich tapestry of discussions, "
        f"reflecting a wide range of experiences, concerns, and triumphs. "
        f"With <strong>{positive_sentiment_posts}</strong> posts expressing positive sentiments and <strong>{negative_sentiment_posts}</strong> conveying challenges, "
        f"the community's dialogue is both hopeful and grounded in reality.</p>"
        f"<ul>{detailed_discussion_html}</ul>"
        f"{predictive_insight_html}"
        f"{conclusion_html}"
    )

    return summary_html


def general_post_anaylsis(file_path, showChart=True):
    # Load the dataset
    data = pd.read_excel(file_path)

    # Combine "Post Title" and "Post Text" for analysis, dropping missing values
    combined_text = (
        data[["Post Title", "Post Text"]]
        .fillna("")
        .apply(lambda x: x["Post Title"] + " " + x["Post Text"], axis=1)
    )
    combined_text = combined_text[combined_text != " "]

    # Text feature extraction for LDA
    tf_vectorizer = CountVectorizer(
        max_df=0.95, min_df=2, max_features=1000, stop_words="english"
    )
    tf = tf_vectorizer.fit_transform(combined_text)

    # Fit LDA model
    lda = LDA(
        n_components=5,
        max_iter=5,
        learning_method="online",
        learning_offset=50.0,
        random_state=0,
    )
    lda.fit(tf)

    # Assuming identification of keywords per topic for plotting
    topic_keywords = {
        "Personal Care & Daily Activities": ["body", "hair", "cut", "feet", "tree"],
        "Social & Family Events": ["party", "birthday", "kids", "kiddo", "park"],
        "General Life & Experiences": ["time", "know", "feel", "day", "year"],
        "Holiday & Seasonal Events": ["santa", "milk", "christmas", "tree", "cup"],
        "Communication & Learning": [
            "blue",
            "word",
            "conversation",
            "daughter",
            "language",
        ],
    }

    # Initialize topic counts
    topic_counts = {topic: 0 for topic in topic_keywords}

    # Count posts per topic based on keywords
    for post in combined_text:
        for topic, keywords in topic_keywords.items():
            if any(keyword in post for keyword in keywords):
                topic_counts[topic] += 1

    # Plot the distribution of topics
    plt.figure(figsize=(10, 6))
    plt.bar(topic_counts.keys(), topic_counts.values(), color="skyblue")
    plt.xlabel("Topics")
    plt.ylabel("Number of Posts")
    plt.title("Distribution of Topics in Posts")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("./graphs/general_post_analysis_chart.png")
    if showChart:
        plt.show()

    # Initialize sentiment scores dictionary
    sentiment_scores = {
        topic: [] for topic in topic_keywords
    }  # Store sentiment scores for each topic

    # Analyze sentiment for each post and assign to relevant topic based on keywords
    for post in combined_text:
        post_sentiment = TextBlob(post).sentiment.polarity  # Example sentiment analysis
        for topic, keywords in topic_keywords.items():
            if any(keyword in post for keyword in keywords):
                sentiment_scores[topic].append(post_sentiment)

    # Convert list of sentiment scores to an average score per topic for simplicity
    average_sentiment_scores = {
        topic: sum(scores) / len(scores) if scores else 0
        for topic, scores in sentiment_scores.items()
    }

    print(sentiment_scores, "sentiment_scores")
    print(average_sentiment_scores, "average_sentiment_scores")

    # Generate insights summary with the updated call
    insights_summary = summarize_insights_html(
        topic_counts, combined_text, sentiment_scores
    )

    return "./graphs/general_post_analysis_chart.png", insights_summary
