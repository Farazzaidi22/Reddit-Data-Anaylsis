from pathlib import Path

# Assuming the analysis functions are defined elsewhere and modified to return the path of the generated chart images
from comments_anaylsis import analyze_all_comment_files
from overview_analysis import general_post_anaylsis
from post_analysis import emotional_pattern_analysis

def generate_html_report(file_path, directory_path, report_path):
    
    # Generate analysis charts and insights
    general_post_chart, general_post_analysis_summary = general_post_anaylsis(file_path, showChart=False)
    
    emotional_pattern_chart, emotional_post_analysis_summary = emotional_pattern_analysis(file_path, showChart=False)
    comment_analysis_chart, comments_analysis_summary = analyze_all_comment_files(directory_path, showChart=False)

    # HTML structure
    html_content = f"""
    <html>
    <head>
        <title>Analysis Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1, h2 {{ color: #333; }}
            img {{ width: 100%; max-width: 600px; height: auto; }}
            .section {{ margin-bottom: 40px; }}
        </style>
    </head>
    <body>
        <h1>Analysis Report</h1>
        
        <div class="section">
            <h2>General Post Analysis</h2>
            <img src="{general_post_chart}" alt="General Post Analysis Chart">
            <p>{general_post_analysis_summary}</p>
        </div>
        
        <hr />

        <div class="section">
            <h2>Emotional Pattern Analysis</h2>
            <img src="{emotional_pattern_chart}" alt="Emotional Pattern Analysis Chart">
            <p>{emotional_post_analysis_summary}</p>
        </div>
        
        <hr />

        <div class="section">
            <h2>Comment Analysis</h2>
            <img src={comment_analysis_chart} alt="Comment Analysis Chart">
             <p>{comments_analysis_summary}</p>
        </div>
    </body>
    </html>
    """

    # Write the HTML content to a file
    with open(report_path, 'w') as html_file:
        html_file.write(html_content)

    print("HTML report generated successfully.")

# Adjust paths accordingly
# file_path = '../Input_Output/autism_parenting_data_last_year.xlsx'
# directory_path = Path('../Input_Output/Autism_Parenting_Post_comments')
# report_path = 'analysis_report.html'  # Path where the HTML report will be saved

# generate_html_report(file_path, directory_path, report_path)
