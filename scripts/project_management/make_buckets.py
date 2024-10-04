# Explanation
# This script creates subfolders in the input and output buckets for each language in the languages.json file.
# The script uses the google.cloud.storage library to interact with Google Cloud Storage.
# The load_language_mappings function reads the languages.json file and returns the language mappings as a dictionary.
# The create_language_subfolders function creates subfolders in the specified bucket with the given folder prefix and language mappings.
# The main function loads the language mappings, creates subfolders in the input and output buckets for response generation and feedback, and calls the create_language_subfolders function.
# It should not need to be rerun unless output folders are deleted, new languages are added, or we need more sets of buckets (like for websites, pdf or videos).

from google.cloud import storage
import json

def load_language_mappings(json_file_path):
    with open(json_file_path, 'r') as file:
        return json.load(file)

def create_language_subfolders(bucket_name, folder_prefix, language_mappings):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    for language in language_mappings:
        folder_name = f"{folder_prefix}{language}/"  # Construct folder name
        blob = bucket.blob(folder_name)
        if not blob.exists():  # Check if the folder (blob) already exists
            blob.upload_from_string('', content_type='application/x-www-form-urlencoded;charset=UTF-8')
            print(f"Created folder for {language}")
        else:
            print(f"{folder_prefix} folder for {language} already exists. Skipping.")

def main():
    json_file_path = '../../languages/languages.json'
    input_bucket_name = 'label-studio-output'
    output_bucket_name = 'label-studio-input-open-paws'
    response_folder_prefix = 'response-generation-'
    feedback_folder_prefix = 'response-feedback-'
    text_feedback_folder_prefix = 'text-feedback-'
    image_feedback_folder_prefix = 'image-feedback-'
    web_page_feedback_folder_prefix = 'web-page-feedback-'

    unfiltered_language_mappings = load_language_mappings(json_file_path)
    
    # filter out all languages except Portugese
    # including portugese anywhere in the key, both portugese - BR and portugese - EU
    language_mappings = {k: v for k, v in unfiltered_language_mappings.items() if 'portuguese' in k.lower()}
    
    print(language_mappings)
    create_language_subfolders(input_bucket_name, response_folder_prefix, language_mappings)
    create_language_subfolders(input_bucket_name, feedback_folder_prefix, language_mappings)
    create_language_subfolders(input_bucket_name, text_feedback_folder_prefix, language_mappings)
    create_language_subfolders(input_bucket_name, image_feedback_folder_prefix, language_mappings)
    create_language_subfolders(input_bucket_name, web_page_feedback_folder_prefix, language_mappings)

    create_language_subfolders(output_bucket_name, response_folder_prefix, language_mappings)
    create_language_subfolders(output_bucket_name, feedback_folder_prefix, language_mappings)
    create_language_subfolders(output_bucket_name, text_feedback_folder_prefix, language_mappings)
    create_language_subfolders(output_bucket_name, image_feedback_folder_prefix, language_mappings)
    create_language_subfolders(output_bucket_name, web_page_feedback_folder_prefix, language_mappings)

if __name__ == "__main__":
    main()