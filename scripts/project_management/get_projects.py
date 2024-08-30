import requests
import json
import os

project_type_keys = {
    "Response Feedback": '<TextArea name=\"explanation\" toName=\"chat\"',
    "Response Generation": '<TextArea name=\"explanation\" toName=\"chat\"',
    "Text Feedback": '<TextArea name=\"explanation\" toName=\"text\"',
    "Image Feedback": '<TextArea name=\"explanation\" toName=\"image\"',
    "HTML Feedback": '<TextArea name=\"explanation\" toName=\"html_content\"'
}
    # Add other project types and their unique keys here


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

# Compare projects with languages and save English and Spanish projects to a file\
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
                language_projects[language].append(project['title'])  # Use original project title
                if language.lower() == 'english':
                    english_projects.append(project)
    
    for language, projects in language_projects.items():
        if len(projects) != 5:
            print(f"Language '{language}' has {len(projects)} projects. Expected 5.")
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
    projects = get_all_projects(api_url, api_token, 10000)
    compare_projects_with_languages(projects, languages)

if __name__ == "__main__":
    main()