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
        "fee_payment": ["fee", "payment"],
        "exam_schedule": ["exam schedule", "schedule"],
        "B.Tech": ["B.Tech", "bachelor of technology"],
        "ECE": ["ECE", "electronics and communication engineering"],
        "backlog": ["backlog"],
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
    
    return tags_csv, summary

if __name__=="__main__":
    # Example usage
    input_text = """
        All B.Tech students are hereby informed that the fee payment for the upcoming semester is due by the end of this month.
        The exam schedule for the final semester exams has been released. Students with backlogs are advised to check the updated
        schedule on the official website. This notice is applicable to all branches including CSE, ECE, and Mechanical Engineering.
    """

    # Get the result
    tags , summary = process_notice(input_text)
    print(f"tags: {tags}")
    print(f"summary: {summary}")