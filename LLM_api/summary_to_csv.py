import pandas as pd
import os

def append_to_csv(new_row, filename='notices.csv'):
    # Define the column headings
    column_headers = ['S. no.', 'extracted_text', 'LLM_summary', 'link_to_notice', 'tags']
    
    # Check if the file exists
    if not os.path.isfile(filename):
        # If the file doesn't exist, create it and write the header
        df = pd.DataFrame(columns=column_headers)
        df.to_csv(filename, index=False)
    
    # Append the new row to the CSV
    # new_row = {
    #     'S. no.': s_no,
    #     'extracted_text': extracted_text,
    #     'LLM_summary': llm_summary,
    #     'link_to_notice': link_to_notice,
    #     'tags': tags
    # }
    
    df = pd.DataFrame([new_row])
    df.to_csv(filename, mode='a', header=False, index=False)

    # Example usage
if __name__ == "__main__":
    append_to_csv(1, 'Sample text', 'Sample summary', 'http://example.com', 'Sample tags')
