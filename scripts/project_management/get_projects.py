import requests
import json
import os
from parse_label_config import get_project_category

# Load the languages from the JSON file
def load_languages(json_file_path):
    with open(json_file_path, 'r') as file:
        return json.load(file)

# Get all projects from Label Studio API
def get_all_projects(api_url, api_token, page_size=1000):
    headers = {
        'Authorization': f'Token {api_token}'
    }
    all_projects = []
    page = 1

    while True:
        params = {
            'page_size': page_size,
            'page': page
        }
        response = requests.get(f'{api_url}/api/projects', headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        projects = data.get('results', [])
        all_projects.extend(projects)
        
        if not data.get('next'):
            break
        page += 1

    return all_projects

# Compare projects with languages and save English and Spanish projects to a file
def compare_projects_with_languages(projects, languages):
    if isinstance(projects, dict):
        projects = projects.get('results', [])  # Adjust based on actual API response structure

    language_projects = {language: [] for language in languages.keys()}
    english_projects = []
    spanish_projects = []
    
    for project in projects:
        project_name = project['title'].lower()  # Convert project name to lowercase
        for language, non_english_name in languages.items():
            if language.lower() in project_name or non_english_name.lower() in project_name:  # Check both English and non-English names
                language_projects[language].append(project)  # Use original project title
                if language.lower() == 'english':
                    english_projects.append(project)
                elif language.lower() == 'spanish':
                    spanish_projects.append(project)
    
    for language, projects in language_projects.items():
        if len(projects) != 5:
            print(f"Language '{language}' has {len(projects)} projects. Expected 5.")
        # else:
        #     print(f"Language '{language}' has the correct number of projects.")
    
    # Save English and Spanish projects to a temporary file
    with open('english_spanish_projects.json', 'w') as file:
        json.dump({'English': english_projects, 'Spanish': spanish_projects}, file, indent=4)


    # Report missing project types for each language
    required_categories = {'Response Feedback', 'Image Feedback', 'Text Feedback', 'Web Feedback', 'Response Generation'}
    for language, projects in language_projects.items():
        categories = {get_project_category(project) for project in projects}
        missing_categories = required_categories - categories
        if missing_categories:
            print(f"Language '{language}' is missing the following project types: {', '.join(missing_categories)}")
        # else:
        #     print(f"Language '{language}' has all required project types.")

# Function to set up input storage for a project
def setup_import_storage(api_url, api_token, project_id, bucket, prefix):
    headers = {
        'Authorization': f'Token {api_token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "regex_filter": "",
        "use_blob_urls": False,
        "presign": False,
        "presign_ttl": 1,
        "title": "",
        "description": "",
        "project": project_id,
        "bucket": bucket,
        "prefix": prefix,
        "google_application_credentials": "",
        "google_project_id": ""
    }
    response = requests.post(f'{api_url}/api/storages/gcs', headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# function to set up target or output storage for a project
def setup_export_storage(api_url, api_token, project_id, bucket, prefix):
    headers = {
        'Authorization': f'Token {api_token}', 'Content-Type': 'application/json'}
    payload = {
        "regex_filter": "",
        "use_blob_urls": False,
        "presign": False,
        "presign_ttl": 1,
        "title": "",
        "description": "",
        "project": project_id,
        "bucket": bucket,
        "prefix": prefix,
        "google_application_credentials": "",
        "google_project_id": ""
    }
    response = requests.post(f'{api_url}/api/storages/export/gcs', headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

def list_and_sync_input_storages(api_url, api_token, language_projects):
    headers = {
        'Authorization': f'Token {api_token}', 'Content-Type': 'application/json'}
    # List input storages
    # loop over projects
    for project in language_projects:
        project_id = project['id']
        response = requests.get(f'{api_url}/api/storages/gcs?project={project_id}', headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        storages = response.json()
        # Sync input storages
        for storage in storages:
            storage_id = storage['id']
            sync_response = requests.post(f'{api_url}/api/storages/gcs/{storage_id}/sync', headers=headers)
            sync_response.raise_for_status()  # Raise an exception for HTTP errors
            print(f"Synced input storage with ID {storage_id}")
    
    
# Function to list and sync output storages
def list_and_sync_output_storages(api_url, api_token, language_projects):
    headers = {
        'Authorization': f'Token {api_token}',
        'Content-Type': 'application/json'
    }
    # List output storages
    # loop over projects
    for project in language_projects:
        project_id = project['id']
        response = requests.get(f'{api_url}/api/storages/export/gcs?project={project_id}', headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        storages = response.json()
        # Sync input storages
        for storage in storages:
            storage_id = storage['id']
            sync_response = requests.post(f'{api_url}/api/storages/export/gcs/{storage_id}/sync', headers=headers)
            sync_response.raise_for_status()  # Raise an exception for HTTP errors
            print(f"Synced input storage with ID {storage_id}")
    

# Function to update Label Studio configuration for English projects
def update_projects(api_url, api_token, projects, language):
    input_bucket = 'label-studio-input-open-paws'
    output_bucket = 'label-studio-output'
    # change the end of the prefixes to the language
    prefixes = {
        'Response Generation': f'response-generation-{language}',
        'Response Feedback': f'response-feedback-{language}',
        'Image Feedback': f'image-feedback-{language}',
        'Text Feedback': f'text-feedback-{language}',
    }

    for project in projects:
        project_id = project['id']
        category = get_project_category(project)
        if category in prefixes:
            prefix = prefixes[category]
            # Set up input storage
            setup_import_storage(api_url, api_token, project_id, input_bucket, prefix)
            # Set up output storage
            setup_export_storage(api_url, api_token, project_id, output_bucket, prefix)
            
            print(f"Configured storage for project {project_id} with prefix {prefix}")

def main():
    json_file_path = '../../languages/languages.json'
    api_url = os.getenv('LABEL_STUDIO_URL')  # Read API URL from environment variable
    api_token = os.getenv('LABEL_STUDIO_API_TOKEN')  # Read API token from environment variable

    if not api_url:
        raise ValueError("API URL not found. Please set the LABEL_STUDIO_URL environment variable.")
    
    if not api_token:
        raise ValueError("API token not found. Please set the LABEL_STUDIO_API_TOKEN environment variable.")

    languages = load_languages(json_file_path)
    projects = get_all_projects(api_url, api_token, 10000)
    # compare_projects_with_languages(projects, languages)

     # Update projects for every language
    for language in languages.keys():
        # find the projects for the language
        language_projects = [project for project in projects if language.lower() in project['title'].lower()]
        
        
        # Filter projects by ID range
        filtered_projects = [project for project in language_projects if 3061 <= project['id'] <= 3117]
        
        # Update and sync the filtered projects
        if filtered_projects:
            update_projects(api_url, api_token, filtered_projects, language)
            list_and_sync_input_storages(api_url, api_token, language_projects=filtered_projects)
            list_and_sync_output_storages(api_url, api_token, language_projects=filtered_projects)

if __name__ == "__main__":
    main()