import requests
import json
import os

# Load the languages from the JSON file
def load_languages(json_file_path):
    with open(json_file_path, 'r') as file:
        return json.load(file)

# Get all projects from Label Studio API
def get_all_projects(api_url, api_token):
    headers = {
        'Authorization': f'Token {api_token}'
    }
    response = requests.get(f'{api_url}/api/projects', headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# Compare projects with languages and save English and Spanish projects to a file
def compare_projects_with_languages(projects, languages):
    if isinstance(projects, dict):
        projects = projects.get('results', [])  # Adjust based on actual API response structure

    language_projects = {language: [] for language in languages.keys()}
    english_projects = []
    spanish_projects = []
    
    for project in projects:
        project_name = project['title']
        for language in languages.keys():
            if language in project_name:
                language_projects[language].append(project_name)
                if language == 'English':
                    english_projects.append(project)
                elif language == 'Spanish':
                    spanish_projects.append(project)
    
    for language, projects in language_projects.items():
        if len(projects) != 4:
            print(f"Language '{language}' has {len(projects)} projects. Expected 4.")
        else:
            print(f"Language '{language}' has the correct number of projects.")
    
    # Save English and Spanish projects to a temporary file
    with open('english_spanish_projects.json', 'w') as file:
        json.dump({'English': english_projects, 'Spanish': spanish_projects}, file, indent=4)

def main():
    json_file_path = '../../languages/languages.json'
    api_url = os.getenv('LABEL_STUDIO_URL')  # Read API URL from environment variable
    api_token = os.getenv('LABEL_STUDIO_API_TOKEN')  # Read API token from environment variable

    if not api_url:
        raise ValueError("API URL not found. Please set the LABEL_STUDIO_URL environment variable.")
    
    if not api_token:
        raise ValueError("API token not found. Please set the LABEL_STUDIO_API_TOKEN environment variable.")

    languages = load_languages(json_file_path)
    projects = get_all_projects(api_url, api_token)
    compare_projects_with_languages(projects, languages)

if __name__ == "__main__":
    main()