import base64
import json
import os
import requests
import sys
import time
from word2number import w2n

def get_api_key():
    """Gets the API key from an environment variable."""
    api_key = os.environ.get("AZURE_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set the AZURE_API_KEY environment variable.")
    return api_key

def encode_image_to_base64(image_path):
    """Encodes an image file to a base64 string."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found at: {image_path}")
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def process_document_with_ai(api_key, image_base64):
    """Sends the image data to the Mistral Document AI API for processing."""
    endpoint_url = "https://dines-mbf128eg-swedencentral.services.ai.azure.com/providers/mistral/azure/ocr"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    record_schema = {
        "properties": {
            "customer_reference_number": {"title": "Customer Reference Number", "type": "string"},
            "customer_name": {"title": "Customer Name", "type": "string"},
            "city_state": {"title": "City, State", "type": "string"},
            "purchase_value": {"title": "Purchase Value", "description": "Extract the purchase value as a string.", "type": "string"},
            "down_payment": {"title": "Down Payment", "description": "Extract the down payment as a string.", "type": "string"},
            "loan_period": {"title": "Loan Period", "description": "Extract the loan period as a string.", "type": "string"},
            "annual_interest": {"title": "Annual Interest", "description": "Extract the annual interest as a string.", "type": "string"},
            "guarantor_name": {"title": "Guarantor Name", "description": "The name of the guarantor, which is a person's name (e.g., Mr. John Doe), typically found at the end of the record after the percentage values for interest reduction.", "type": "string"},
            "guarantor_reference_number": {"title": "Guarantor Reference Number", "description": "The alphanumeric reference number of the guarantor, typically found at the very end of the record after the guarantor's name.", "type": "string"},
            "purchase_value_reduction": {"title": "Purchase Value Reduction", "description": "Extract the purchase value reduction as a string.", "type": "string"},
            "monthly_principal_reduction": {"title": "Monthly Principal Reduction", "description": "Extract the monthly principal reduction as a string.", "type": "string"},
            "total_interest_reduction": {"title": "Total Interest Reduction", "description": "Extract the total interest reduction as a string.", "type": "string"}
        },
        "title": "MortgageDocument",
        "type": "object",
        "additionalProperties": False
    }

    schema = {
        "properties": {
            "records": {
                "type": "array",
                "description": "A list of all records found in the document.",
                "items": record_schema
            }
        },
        "required": ["records"],
        "type": "object"
    }



    payload = {
        "model": "mistral-document-ai-2505",
        "document": {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_base64}"},
        "document_annotation_format": {"type": "json_schema", "json_schema": {"schema": schema, "name": "document_annotation"}}
    }



    print("Sending request to AI API...")
    response = requests.post(endpoint_url, headers=headers, data=json.dumps(payload), timeout=60)
    print("Received response from AI API.")
    response.raise_for_status()
    return response.json()

def parse_and_transform_data(api_response):
    """Applies formatting and calculation rules to the extracted data."""
    raw_annotation_str = api_response.get('document_annotation', '{}')
    annotation_data = json.loads(raw_annotation_str)
    
    records = []
    if 'properties' in annotation_data and 'records' in annotation_data['properties']:
        records = annotation_data['properties']['records']
    elif 'records' in annotation_data:
        records = annotation_data['records']
    elif isinstance(annotation_data, list):
        records = annotation_data
    
    if not records and 'properties' in annotation_data:
        if 'customer_reference_number' in annotation_data['properties']:
             records = [annotation_data['properties']]

    return records

def convert_string_with_numbers(text):
    """Converts number words within a string to numbers, leaving other words intact."""
    if not isinstance(text, str):
        return text
    
    text = str(text).upper()
    text = text.replace('%', '').strip()
    # Replace " AND " with " POINT " for cases like "FOURTEEN AND SEVENTY FOUR" -> 14.74
    text = text.replace(' AND ', ' POINT ')
    text = text.replace('.', ' POINT ')

    words = text.split()
    if not words:
        return ""
        
    converted_words = []
    i = 0
    while i < len(words):
        # Try to match longest possible number phrase
        j = len(words)
        found = False
        while j > i:
            phrase = " ".join(words[i:j])
            try:
                num = w2n.word_to_num(phrase)
                converted_words.append(str(num))
                i = j
                found = True
                break
            except ValueError:
                j -= 1
        
        if not found:
            converted_words.append(words[i])
            i += 1
            
    return " ".join(converted_words)

def convert_price_to_number(price_str):
    """Converts a price string with words to a number."""
    try:
        price_str = str(price_str)
        # Remove currency symbols and other non-numeric words
        price_str = price_str.replace('$', '').replace(',', '').replace(' AND', '')
        # Handle OCR inconsistencies
        price_str = price_str.replace(' H UNDRED', ' HUNDRED').replace('H UNDRED', 'HUNDRED')
        price_str = price_str.strip()
        return w2n.word_to_num(price_str)
    except ValueError:
        return price_str

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python3 process_image.py <folder_path> [output_folder_path]")
        sys.exit(1)

    folder_path = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) == 3 else "."

    if not os.path.isdir(folder_path):
        print(f"Error: Folder not found at: {folder_path}")
        sys.exit(1)

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    output_path = os.path.join(output_folder, "output.txt")
    
    try:
        api_key = get_api_key()
        filenames = sorted(os.listdir(folder_path))
        
        all_records = []
        partial_record = {}
        required_fields = ["customer_reference_number", "customer_name", "city_state", "purchase_value", "down_payment", "loan_period", "annual_interest", "guarantor_name", "guarantor_reference_number", "purchase_value_reduction", "monthly_principal_reduction", "total_interest_reduction"]

        for filename in filenames:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(folder_path, filename)
                print(f"Processing {image_path}...")
                try:
                    print("Step 1: Sending image to Mistral AI for data extraction...")
                    api_result = process_document_with_ai(api_key, encode_image_to_base64(image_path))
                    print("Step 2: Parsing and transforming AI response...")
                    records = parse_and_transform_data(api_result)
                    
                    # If there's a partial record from a previous page, prepend it to this page's records
                    if partial_record:
                        records.insert(0, partial_record)
                        partial_record = {}

                    processed_records = []
                    # Now, iterate through the combined list and merge adjacent partial records
                    i = 0
                    while i < len(records):
                        current_record = records[i]
                        if i + 1 < len(records):
                            next_record = records[i+1]
                            # Heuristic for continuation: next record is missing a primary key
                            if 'customer_reference_number' not in next_record or not next_record.get('customer_reference_number'):
                                # Merge next_record into current_record
                                for key, value in next_record.items():
                                    if not current_record.get(key) and value:
                                        current_record[key] = value
                                records.pop(i+1) # remove the merged record
                                # Stay at the same index 'i' to see if the now-merged record needs to be merged again
                                continue
                        
                        processed_records.append(current_record)
                        i += 1

                    # After processing a page, the last record might be partial for the *next* page
                    if processed_records:
                        last_record = processed_records[-1]
                        if any(field not in last_record or not last_record.get(field) for field in required_fields):
                            partial_record = processed_records.pop(-1)
                    
                    all_records.extend(processed_records)
                    time.sleep(2)
                except Exception as e:
                    print(f"An error occurred while processing {filename}: {e}")
        
        if partial_record:
            all_records.append(partial_record)
        
        header = [
            "Customer Reference Number", "Customer Name", "City, State", 
            "Purchase Value", "Down Payment", "Loan Period and Annual Interest", 
            "Purchase Value Reduction", "Monthly Principal Reduction", "Total Interest Reduction", 
            "Guarantor Name", "Guarantor Reference Number"
        ]
        
        with open(output_path, 'w') as f:
            f.write(', '.join(header) + '\n')
            for record in all_records:
                loan_period_str = record.get('loan_period', '')
                annual_interest_str = record.get('annual_interest', '')

                loan_period = convert_string_with_numbers(loan_period_str)
                annual_interest = convert_string_with_numbers(annual_interest_str)
                
                purchase_value = convert_price_to_number(record.get('purchase_value', ''))
                down_payment = convert_price_to_number(record.get('down_payment', ''))

                city_state = str(record.get('city_state', '')).replace(', ', '.').upper()

                row = [
                    str(record.get('customer_reference_number', '')).upper(),
                    str(record.get('customer_name', '')).upper(),
                    city_state,
                    f"{purchase_value:.2f}",
                    str(down_payment),
                    f"{loan_period} YEARS AND {annual_interest} %",
                    str(record.get('purchase_value_reduction', '')),
                    str(record.get('monthly_principal_reduction', '')),
                    str(record.get('total_interest_reduction', '')),
                    str(record.get('guarantor_name', '')).upper(),
                    str(record.get('guarantor_reference_number', '')).upper(),
                ]
                f.write(', '.join(row) + '\n')
        
        print(f"Step 3: All data saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
