import requests
import json
import os
import argparse
import logging
from parse_label_config import get_project_category

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

timeoutInt = 100

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
        response = requests.get(f'{api_url}/api/projects', headers=headers, params=params, timeout=timeoutInt)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        projects = data.get('results', [])
        all_projects.extend(projects)
        
        if not data.get('next'):
            break
        page += 1

    return all_projects


# Function to check if import storage exists for a project
def import_storage_exists(api_url, api_token, project_id, bucket, prefix):
    headers = {
        'Authorization': f'Token {api_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f'{api_url}/api/storages/gcs?project={project_id}', headers=headers, timeout=10)
    response.raise_for_status()  # Raise an exception for HTTP errors
    storages = response.json()
    for storage in storages:
        if storage['bucket'] == bucket and storage['prefix'] == prefix:
            return True
    return False

# Function to check if export storage exists for a project
def export_storage_exists(api_url, api_token, project_id, bucket, prefix):
    headers = {
        'Authorization': f'Token {api_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f'{api_url}/api/storages/export/gcs?project={project_id}', headers=headers, timeout=10)
    response.raise_for_status()  # Raise an exception for HTTP errors
    storages = response.json()
    for storage in storages:
        if storage['bucket'] == bucket and storage['prefix'] == prefix:
            return True
    return False

# Function to set up input storage for a project
def setup_import_storage(api_url, api_token, project_id, bucket, prefix):
    if import_storage_exists(api_url, api_token, project_id, bucket, prefix):
        logging.info(f"Import storage already exists for project {project_id} with prefix {prefix}")
        return

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
    response = requests.post(f'{api_url}/api/storages/gcs', headers=headers, json=payload, timeout=10)
    response.raise_for_status()  # Raise an exception for HTTP errors
    logging.info(f"Created import storage for project {project_id} with prefix {prefix}")
    return response.json()

# Function to set up output storage for a project
def setup_export_storage(api_url, api_token, project_id, bucket, prefix):
    if export_storage_exists(api_url, api_token, project_id, bucket, prefix):
        logging.info(f"Export storage already exists for project {project_id} with prefix {prefix}")
        return

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
    response = requests.post(f'{api_url}/api/storages/export/gcs', headers=headers, json=payload, timeout=10)
    response.raise_for_status()  # Raise an exception for HTTP errors
    logging.info(f"Created export storage for project {project_id} with prefix {prefix}")
    return response.json()


# Function to list and sync input storages
def list_and_sync_input_storages(api_url, api_token, project_id):
    headers = {
        'Authorization': f'Token {api_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f'{api_url}/api/storages/gcs?project={project_id}', headers=headers, timeout=timeoutInt)
    response.raise_for_status()  # Raise an exception for HTTP errors
    storages = response.json()
    for storage in storages:
        storage_id = storage['id']
        sync_response = requests.post(f'{api_url}/api/storages/gcs/{storage_id}/sync', headers=headers, timeout=timeoutInt)
        sync_response.raise_for_status()  # Raise an exception for HTTP errors
        logging.info(f"Synced input storage with ID {storage_id}")

# Function to list and sync output storages
def list_and_sync_output_storages(api_url, api_token, project_id):
    headers = {
        'Authorization': f'Token {api_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f'{api_url}/api/storages/export/gcs?project={project_id}', headers=headers, timeout=timeoutInt)
    response.raise_for_status()  # Raise an exception for HTTP errors
    storages = response.json()
    for storage in storages:
        storage_id = storage['id']
        sync_response = requests.post(f'{api_url}/api/storages/export/gcs/{storage_id}/sync', headers=headers, timeout=timeoutInt)
        sync_response.raise_for_status()  # Raise an exception for HTTP errors
        logging.info(f"Synced output storage with ID {storage_id}")

# Function to check the existence of projects for each language
def check_projects_existence(api_url, api_token, json_file_path):
    languages = load_languages(json_file_path)
    projects = get_all_projects(api_url, api_token, 10000)
    required_categories = {'Response Feedback', 'Image Feedback', 'Text Feedback', 'Web Feedback', 'Response Generation'}
    logging.debug(f"Loaded languages: {languages.keys()}")
    logging.debug(f"Loaded projects: {[project['id'] for project in projects]}")

    for language in languages.keys():
        logging.debug(f"Processing language: {language}")
        language_projects = [project for project in projects if language.lower() in project['title'].lower()]
        logging.debug(f"Projects count for language {language}: {len(language_projects)}")

        for category in required_categories:
            category_projects = [project for project in language_projects if get_project_category(project) == category]
            if not category_projects:
                logging.warning(f"Missing project for category '{category}' in language '{language}'")
            else:
                logging.debug(f"Found projects for category '{category}' in language '{language}'")

# Function to check if projects have storage configured
def check_storage_configuration(api_url, api_token, json_file_path):
    languages = load_languages(json_file_path)
    projects = get_all_projects(api_url, api_token, 10000)
    logging.debug(f"Loaded languages: {languages.keys()}")
    logging.debug(f"Loaded projects: {[project['id'] for project in projects]}")

    for language in languages.keys():
        logging.debug(f"Processing language: {language}")
        language_projects = [project for project in projects if language.lower() in project['title'].lower()]
        logging.debug(f"Projects count for language {language}: {len(language_projects)}")

        for project in language_projects:
            project_id = project['id']
            logging.debug(f"Processing project ID: {project_id}")
            list_and_sync_input_storages(api_url, api_token, project_id)
            list_and_sync_output_storages(api_url, api_token, project_id)

# Function to add storage configurations
def add_storage_configuration(api_url, api_token, json_file_path):
    languages = load_languages(json_file_path)
    projects = get_all_projects(api_url, api_token, 10000)
    input_bucket = 'label-studio-input-open-paws'
    output_bucket = 'label-studio-output'
    prefixes = {
        'Response Generation': 'response-generation',
        'Response Feedback': 'response-feedback',
        'Image Feedback': 'image-feedback',
        'Text Feedback': 'text-feedback',
        'Web Feedback': 'web-page-feedback'
    }

    for language in languages.keys():
        language_projects = [project for project in projects if language.lower() in project['title'].lower()]

        for project in language_projects:
            project_id = project['id']
            category = get_project_category(project)
            if category in prefixes:
                prefix = f"{prefixes[category]}-{language}"
                setup_import_storage(api_url, api_token, project_id, input_bucket, prefix)
                setup_export_storage(api_url, api_token, project_id, output_bucket, prefix)
                logging.info(f"Configured storage for project {project_id} with prefix {prefix}")

# Function to sync all storages
def sync_all_storages(api_url, api_token, json_file_path):
    languages = load_languages(json_file_path)
    projects = get_all_projects(api_url, api_token, 10000)

    for language in languages.keys():
        language_projects = [project for project in projects if language.lower() in project['title'].lower()]

        for project in language_projects:
            project_id = project['id']
            list_and_sync_input_storages(api_url, api_token, project_id)
            list_and_sync_output_storages(api_url, api_token, project_id)

def main():
    parser = argparse.ArgumentParser(description="Manage Label Studio projects and storages.")
    parser.add_argument('command', choices=['check-projects', 'check-storage', 'add-storage', 'sync-storage'], help="Command to execute")
    args = parser.parse_args()

    json_file_path = '../../languages/languages.json'
    api_url = os.getenv('LABEL_STUDIO_URL')
    api_token = os.getenv('LABEL_STUDIO_API_TOKEN')

    if not api_url:
        raise ValueError("API URL not found. Please set the LABEL_STUDIO_URL environment variable.")
    
    if not api_token:
        raise ValueError("API token not found. Please set the LABEL_STUDIO_API_TOKEN environment variable.")

    if args.command == 'check-projects':
        check_projects_existence(api_url, api_token, json_file_path)
    elif args.command == 'check-storage':
        check_storage_configuration(api_url, api_token, json_file_path)
    elif args.command == 'add-storage':
        add_storage_configuration(api_url, api_token, json_file_path)
    elif args.command == 'sync-storage':
        sync_all_storages(api_url, api_token, json_file_path)

if __name__ == "__main__":
    main()