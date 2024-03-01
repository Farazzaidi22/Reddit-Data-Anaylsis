from pathlib import Path
from extract_data_reddit import save_reddit_posts
from comments_anaylsis import analyze_all_comment_files, analyze_one_comment_file
from overview_analysis import general_post_anaylsis
from post_analysis import emotional_pattern_analysis
from post_engament_analysis import analyze_post_engament


# Save subreddits posts and comments
# save_reddit_posts(subreddit_name="Autism_Parenting")


# Path for the main file
file_path = '../Input_Output/autism_parenting_data_last_year.xlsx'  # Update this path

# Path for the folders where comments files are stored
directory_path = Path('../Input_Output/Autism_Parenting_Post_comments')

# Path for the a single comment file
comment_file_path = Path('../Input_Output/Autism_Parenting_Post_comments/11lh28j.xlsx')


# general topic analysis for Autism_Parenting posts (not comments)
general_post_anaylsis(file_path)

# emotional analysis for Autism_Parenting posts (not comments)
emotional_pattern_analysis(file_path)

# anaylze overall tone and emotions of comments for all posts comments
analyze_all_comment_files(directory_path)

# anaylze overall tone and emotions of comments for all just one post and its comments
analyze_one_comment_file(comment_file_path)

# anaylze engagement on each post
analyze_post_engament(comment_file_path)


