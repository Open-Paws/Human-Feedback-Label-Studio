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

# Compare projects with languages
def compare_projects_with_languages(projects, languages):
    if isinstance(projects, dict):
        projects = projects.get('results', [])  # Adjust based on actual API response structure

    language_projects = {language: [] for language in languages.keys()}
    
    for project in projects:
        project_name = project['title'].lower()  # Convert project name to lowercase
        for language, non_english_name in languages.items():
            if language.lower() in project_name or non_english_name.lower() in project_name:  # Check both English and non-English names
                language_projects[language].append(project)  # Use original project title
    
    for language, projects in language_projects.items():
        if len(projects) != 5:
            print(f"Language '{language}' has {len(projects)} projects. Expected 5.")
        else:
            print(f"Language '{language}' has the correct number of projects.")
    
    # Report missing project types for each language
    required_categories = {'Response Feedback', 'Image Feedback', 'Text Feedback', 'Web Feedback', 'Response Generation'}
    for language, projects in language_projects.items():
        categories = {get_project_category(project) for project in projects}
        missing_categories = required_categories - categories
        if missing_categories:
            print(f"Language '{language}' is missing the following project types: {', '.join(missing_categories)}")
        else:
            print(f"Language '{language}' has all required project types.")

def main():
    json_file_path = '../../languages/languages.json'
    api_url = os.getenv('LABEL_STUDIO_URL')
    api_token = os.getenv('LABEL_STUDIO_API_TOKEN')

    if not api_url:
        raise ValueError("API URL not found. Please set the LABEL_STUDIO_URL environment variable.")
    
    if not api_token:
        raise ValueError("API token not found. Please set the LABEL_STUDIO_API_TOKEN environment variable.")

    languages = load_languages(json_file_path)
    projects = get_all_projects(api_url, api_token)
    compare_projects_with_languages(projects, languages)
    

if __name__ == "__main__":
    main()