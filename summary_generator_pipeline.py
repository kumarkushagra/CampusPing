import pandas as pd
import os
import warnings
import sys
from transformers import pipeline
from huggingface_hub import login
import fitz  # PyMuPDF
import time

# User defined functions
from LLM_api.LLM_contact import *
from LLM_api.summary_to_csv import *
from LLM_api.pdf_to_text import *

from Fetch_new_notices.create_csv import *
from Fetch_new_notices.create_csv_and_append_row import *
from Fetch_new_notices.is_target_tr import *

from Download_pdf.download_new_pdf import *
from Download_pdf.ocr_pdf import *


def process_notices():
    input_file = r"database\notice.csv"
    output_file = "output.csv"

    # Read the input CSV file using pandas
    df_orignal = pd.read_csv(input_file)
    df = df_orignal[df_orignal['Processed_status'] == 0]

    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        start_time = time.time() # REMOVE THIS AFTER TESTING IS COMPLETE
        
        # Fetch the serial number from the input CSV
        s_no = row['S.No']
        pdf_link = row['pdf_link']
        pdf_path = "temp/temp_pdf.pdf"
        
        
        # Step 1: Download the PDF
        download_pdf(pdf_link, pdf_path)
        
        # Step 2: Perform OCR on the downloaded PDF
        ocr_pdf(pdf_path)
        
        # Step 3: Extract text from the PDF
        extracted_text =extract_text_from_pdf(pdf_path)
        
        # Step 4: Get Tags and Summary from the LLM
        tags, llm_summary = process_notice(extracted_text)
        
        # Step 5: Prepare data for output
        output_data = {
            's_no': s_no,
            'extracted_text': extracted_text,
            'llm_summary': llm_summary,
            'link_to_notice': pdf_link,
            'tags': tags
        }
        
        # Append the output data to the output CSV
        append_to_csv(output_data, output_file)

        elapsed_time = time.time() - start_time
        print(f"Processed {pdf_link} in {elapsed_time:.2f} seconds")
        
        # Add delay to prevent overwhelming the system (optional)
        time.sleep(1)
        
        # Update the 'Download status' column for the current row
        df_orignal.at[index, 'Processed_status'] = 1

        # Save the updated DataFrame back to the CSV file
        df_orignal.to_csv(input_file, index=False)
        
        # Delete the temporary file
        os.remove(pdf_path)
        # counter +=1
        # if counter == 2:
        #     break


if __name__ == "__main__":
    # counter = 0
    # main(counter)
    try:
        process_notices()   
    # Your main code here
    except Exception as e:
        print(f"An error occurred: {e}")