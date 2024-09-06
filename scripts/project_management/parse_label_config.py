import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the JSON data from the file
with open('english_spanish_projects.json', 'r') as file:
    data = json.load(file)


# Function to categorize projects based on parsed_label_config
def categorize_project(parsed_label_config):
    if is_response_feedback(parsed_label_config):
        return 'Response Feedback'
    elif is_text_feedback(parsed_label_config):
        return 'Text Feedback'
    elif is_image_feedback(parsed_label_config):
        return 'Image Feedback'
    elif is_web_feedback(parsed_label_config):
        return 'Web Feedback'
    elif is_response_generation(parsed_label_config):
        return 'Response Generation'
    else:
        return 'Other'

def is_response_feedback(config):
    return (
        'explanation' in config and
        'inputs' in config['explanation'] and
        'value' in config['explanation']['inputs'][0] and
        config['explanation']['inputs'][0]['value'] == 'dialogue' and
        'to_name' in config['explanation'] and
        config['explanation']['to_name'][0] == 'chat'
                    
    )

def is_text_feedback(config):
    return (
        'explanation' in config and
        'inputs' in config['explanation'] and
        'type' in config['explanation']['inputs'][0] and
        config['explanation']['inputs'][0]['type'] == 'Text' and
        'to_name' in config['explanation'] and
        config['explanation']['to_name'][0] == 'text'
                    
    )

def is_image_feedback(config):
     return (
        'explanation' in config and
        'inputs' in config['explanation'] and
        'value' in config['explanation']['inputs'][0] and
        config['explanation']['inputs'][0]['value'] == 'url' and
        'to_name' in config['explanation'] and
        config['explanation']['to_name'][0] == 'image'
    )

def is_web_feedback(config):
    return (
        'explanation' in config and
        'inputs' in config['explanation'] and
        'type' in config['explanation']['inputs'][0] and
        config['explanation']['inputs'][0]['type'] == 'HyperText'and
        'to_name' in config['explanation'] and
        config['explanation']['to_name'][0] == 'html_content'
    )

def is_response_generation(config):
    return 'response' in config


def get_project_category(project_json):
    
    logging.debug(f"Getting category for project: {project_json}")
    parsed_label_config = project_json.get('parsed_label_config', {})
    
    categorized_project = categorize_project(parsed_label_config)
    logging.debug(f"Category: {categorized_project}")
    return categorized_project

# # Extract projects and categorize them
# unique_configs = set()
# categorized_projects = {
#     'Response Feedback': [],
#     'Image Feedback': [],
#     'Text Feedback': [],
#     'Web Feedback': [],
#     'Response Generation': [],
#     'Other': []
# }

# for language in data:
#     for project in data[language]:
#         parsed_label_config = project.get('parsed_label_config', {})
#         config_str = json.dumps(parsed_label_config, sort_keys=True)
        
#         # Add to unique configurations
#         unique_configs.add(config_str)
        
#         # Categorize project
#         category = categorize_project(parsed_label_config)
#         categorized_projects[category].append(project)

# # Print unique configurations and categorized projects
# print(f"Unique Configurations: {len(unique_configs)}")
# for category, projects in categorized_projects.items():
#     print(f"{category}: {len(projects)} projects")

# # Optionally, save categorized projects to a file
# with open('categorized_projects.json', 'w') as file:
#     json.dump(categorized_projects, file, indent=4)