import json
from google.cloud import storage

def process_new_conversation_output_files_in_bucket(data, context):
	"""Background Cloud Function to be triggered by Cloud Storage.
	   This function processes files added to language-specific paths in the bucket.
	Args:
		data (dict): The Cloud Functions event payload.
		context (google.cloud.functions.Context): Metadata for the event.
	"""
	print(f"Received event: {data}")
	print(f"Event context: {context}")

	bucket_name = data['bucket']
	file_path = data['name']
	
	# Extract the language from the input path
	# Assuming input paths are in the format 'response-generation-<language>/'
	if 'response-generation-' in file_path:
		language = file_path.split('/')[0].replace('response-generation-', '')
	else:
		print(f"File {file_path} does not match expected input path format. Skipping.")
		return
	
	# Process the file based on the language
	process_file(bucket_name, file_path, language)

def process_file(bucket_name, file_name, language):
	"""Process the file based on the language."""
	storage_client = storage.Client()
	
	# Debug: Print bucket name and file name
	print(f"Accessing bucket: {bucket_name}")
	print(f"Accessing file: {file_name}")
	
	bucket = storage_client.bucket(bucket_name)
	
	# Check if bucket exists
	if not bucket.exists():
		print(f"Bucket {bucket_name} does not exist.")
		return
	
	blob = bucket.blob(file_name)
	
	# Check if blob exists
	if not blob.exists():
		print(f"File {file_name} does not exist in bucket {bucket_name}.")
		return
	
	try:
		# Read the file content
		file_content = blob.download_as_bytes()
		data = json.loads(file_content)
	except Exception as e:
		print(f"Error downloading or parsing file {file_name}: {e}")
		return
	
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
	
	# Define the output and feedback paths
	output_path = f'response-generation-{language}/'
	feedback_path = f'response-feedback-{language}/'
	
	file_suffix = file_name.split('/')[-1]
	output_bucket = storage_client.bucket('label-studio-input-open-paws')
	
	# Check if output bucket exists
	if not output_bucket.exists():
		print(f"Output bucket 'label-studio-input-open-paws' does not exist.")
		return

	try:
		# Upload the processed file to the output and feedback paths
		output_blob = output_bucket.blob(f'{output_path}{file_suffix}')
		feedback_blob = output_bucket.blob(f'{feedback_path}{file_suffix}')
		
		output_blob.upload_from_string(new_file_content, content_type='application/json')
		feedback_blob.upload_from_string(new_file_content, content_type='application/json')
		
		print(f"Processed and uploaded file {file_name} for language {language} into {output_path}{file_suffix} and {feedback_path}{file_suffix}")
	except Exception as e:
		print(f"Error uploading file {file_name}: {e}")