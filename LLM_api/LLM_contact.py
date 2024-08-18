from transformers import pipeline

from huggingface_hub import login
# Login using your token
login("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")
# Load the summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
# Define a function to summarize the document
def generate_summary(input_text, max_len=30, min_len=10):
    summary = summarizer(input_text, max_length=max_len, min_length=min_len, do_sample=False)[0]['summary_text']
    return summary



# Modify the tags here
def extract_tags(input_text):
    tags = []
    keywords = {
        "Scholorship":["scheme", "scholorship"],
        "Fee Payment": ["fee", "payment"],
        "Warnings": ["bunk", "dead line","warning"],
        "Time Table": ["time table", "schedule"],
        "Results": ["exam result", "final result", "result"],
        "Exam Schedule": ["exam schedule", "schedule"],
        "B.Tech": ["B.Tech", "bachelor of technology"],
        "ECE": ["ECE", "electronics and communication engineering"],
        "Backlog": ["backlog", "improvement", "registration"],
    }
    
    # Check for keywords in the text and add them to tags if found
    for tag, keywords_list in keywords.items():
        if any(keyword.lower() in input_text.lower() for keyword in keywords_list):
            tags.append(tag)
    
    return tags

# Define the main function to get both tags and summary
def process_notice(input_text):
    tags = extract_tags(input_text)
    summary = generate_summary(input_text)
    tags_csv = ", ".join(tags)

    file_path = 'latest_notifications.txt'

    # Append the data to the file
    with open(file_path, 'a') as file:
        file.write(f"Tags: {tags_csv}\n")
        file.write(f"Summary: {summary}\n")
        file.write(f"Link: \n")
        file.write('\n')  # Add a new line between entries
    
    return tags_csv, summary

if __name__=="__main__":
    # Example usage
    input_text = """NOTIFICATION

Subject: Mandatory Attendance and Disciplinary Action for Mass Bunking

It is directed to inform you that mass bunking of classes is considered a

serious act of indiscipline. Students found involved in mass bunking will face

strict disciplinary action. Additionally, students involved in such activities will not be granted any relaxation in the attendance criteria in the future, regardless of the circumstances.

Please note that strict action will be taken against first-year students who participate in mass bunking or miss their classes on 21st August 2004 and 27th August 2024. Attendance on these dates is mandatory for all first-year students.

Purthermore, all course instructors teaching first-year students are requested to ensure that attendance for the dates mentioned above is marked in the CUMS system on the same day. This will help identify students who did not attend their classes, and it will be assumed that such students were involved in the mass bunk.

We urge you to comply with these directives and maintain the discipline expected at University.
          """

    # Get the result
    tags , summary = process_notice(input_text)
    print(f"tags: {tags}")
    print(f"summary: {summary}")