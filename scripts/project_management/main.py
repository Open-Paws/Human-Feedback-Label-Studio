# Explanation
# This script processes the files in the input bucket, generates a response based on the input dialogue, and uploads the processed file to the output bucket.
# The process_and_upload_file function reads the file content, processes the data to generate a response, and uploads the processed file to the output bucket.
# It works for english language only, but can be extended to other languages by changing the paths.

from google.cloud import storage
import json

# Initialize the GCP storage client
storage_client = storage.Client()

input_bucket_name = 'label-studio-output'
output_bucket_name = 'label-studio-input-open-paws'
feedback_bucket_name = 'label-studio-input-open-paws'

# Path within the bucket where files are located/should be uploaded
input_path = 'response-generation-english/'
output_path = 'response-generation-english/'
feedback_path = 'response-feedback-english/'

def process_and_upload_file(blob, output_bucket, feedback_bucket):
    # Read the file content
    file_content = blob.download_as_bytes()
    data = json.loads(file_content)
    
    # Process the data
    existing_dialogue = data['task']['data']['dialogue']
    final_response = data['result'][0]['value']['text'][0]
   
    # Initialize the new dialogue list with the existing dialogue preserved
    new_dialogue = existing_dialogue[:]
    
    # Determine the author of the last dialogue entry to alternate correctly
    last_author = existing_dialogue[-1]['author'] if existing_dialogue else "bot"  # Default to "bot" if empty
    new_response_author = "human" if last_author == "bot" else "bot"
    
    # Add the final response to the new dialogue
    new_dialogue.append({"text": final_response, "author": new_response_author})
    
    # Create the new data structure
    new_data = {
     
            "dialogue": new_dialogue
    }
    # Convert the conversation array directly to JSON
    new_file_content = json.dumps(new_data).encode('utf-8')
    new_object_name = f"{output_path}{blob.name.split('/')[-1]}"

    # Check if the file already exists in the output bucket
    output_blob = output_bucket.blob(new_object_name)
    if not output_blob.exists():
        output_blob.upload_from_string(new_file_content)
        print(f"Uploaded processed file to {output_bucket_name}/{new_object_name}")
    else:
        print(f"File {new_object_name} already exists in {output_bucket_name}, skipping.")
    
    if new_response_author == "bot":
        new_feedback_object_name = f"{feedback_path}{blob.name.split('/')[-1]}"
        feedback_blob = feedback_bucket.blob(new_feedback_object_name)
        if not feedback_blob.exists():
            feedback_blob.upload_from_string(new_file_content)
            print(f"Uploaded feedback file to {feedback_bucket_name}/{new_feedback_object_name}")     
        else:
            print(f"File {new_feedback_object_name} already exists in {output_bucket_name}, skipping.")


def process_files_in_bucket(input_bucket_name, output_bucket_name, input_path):
    input_bucket = storage_client.bucket(input_bucket_name)
    output_bucket = storage_client.bucket(output_bucket_name)
    feedback_bucket = storage_client.bucket(feedback_bucket_name)
    blobs = input_bucket.list_blobs(prefix=input_path)
    for blob in blobs:
        # Skip the dummy blob for the folder
        if blob.name.endswith('/'):
            continue  # This skips the folder blob
        
        # Process and upload the file
        process_and_upload_file(blob, output_bucket, feedback_bucket)

process_files_in_bucket(input_bucket_name, output_bucket_name, input_path)