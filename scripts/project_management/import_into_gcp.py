import os
import subprocess
from google.cloud import storage

# Dictionary of language abbreviations and their full names
languages = {
    "en": "English",
    "es": "Spanish",
    "ru": "Russian",
    "zh": "Chinese",
    "de": "German",
    "fr": "French",
    "pt": "Portuguese",
    "th": "Thai",
    "ca": "Catalan",
    "it": "Italian",
    "uk": "Ukrainian",
    "ja": "Japanese",
    "pl": "Polish",
    "eo": "Esperanto",
    "eu": "Basque",
    "vi": "Vietnamese",
    "fi": "Finnish",
    "hu": "Hungarian",
    "ar": "Arabic",
    "nl": "Dutch",
    "da": "Danish",
    "tr": "Turkish",
    "ko": "Korean",
    "he": "Hebrew",
    "id": "Indonesian",
    "cs": "Czech",
    "bn": "Bengali",
    "sv": "Swedish"
}

# Parent directory
parent_dir = "response_generation"

# Iterate through the sub-folders
for lang_abbr, lang_name in languages.items():
    sub_folder = os.path.join(parent_dir, lang_abbr)
    if os.path.exists(sub_folder):
        # GCP bucket name
        bucket_name = f"label-studio-input-open-paws/response-generation-{lang_name.capitalize()}" 
        # Transfer files using gsutil
        command = f"gsutil -m cp -r {sub_folder}/* gs://{bucket_name}/"
        subprocess.run(command, shell=True)
        print(f"Transferred files from {sub_folder} to gs://{bucket_name}/")
    else:
        print(f"Sub-folder {sub_folder} does not exist.")
