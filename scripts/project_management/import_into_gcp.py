PapaVegan
taterfighter
Online

Sam Tucker - Open Paws — 09/05/2024 8:33 AM
Yay! 😀 I think that might be just about everything we needed ready to launch?
PapaVegan — 09/05/2024 8:37 AM
I think so!
Pranav Banuru — 09/05/2024 11:18 AM
Some things I noticed as well -
Loading time for the home project page is ~17-20 seconds
https://feedback.openpaws.ai/projects/ 
If we have the site remember language selection when refreshing/going to the projects page it would be good
https://feedback.openpaws.ai/projects/ 
Pranav Banuru — 09/05/2024 12:31 PM
https://feedback.openpaws.ai/projects/2479/settings/storage
Web Page Feedback's bucket for English and Danish didn't appear
but it did appear for Spanish - 

So seems some connected and some did not
Image
Image
Projects without input storage buckets:
Project ID: 3096, Title: Feedback Resp [Português - EU] (Portuguese - EU)
Project ID: 3095, Title: Geração Resps [Português - EU] (Portuguese - EU)
Project ID: 3085, Title: Resposta Eco [Português - BR] (Portuguese - BR)
Project ID: 3073, Title: Gerar Resposta [Português - BR] (Portuguese - BR)
Project ID: 3071, Title: Feedback Texto [Português - EU] (Portuguese - EU)
Expand
message.txt
12 KB
Pranav Banuru — 09/05/2024 2:43 PM
@Sam Tucker - Open Paws For the Semantic Scholar Dataset, 

### 1. `semantic_scholar_processing.ipynb`
This Google Colab notebook contains code for processing and analyzing data from the Semantic Scholar corpus. The notebook is designed to:
- **Load**: Load the raw data including TLDR summaries, Abstracts and S2ORC metadata.
- **Preprocess**: Clean and preprocess the data, focusing on key fields such as paper titles, abstracts, and author information.
- **Transform**: Merge TLDR summaries and Abstracts with S2ORC metadata to create a comprehensive dataset, whilst reducing token usage by scoring and filtering based on TLDRs and Abstracts.
- **Score**: Calculate custom CRITERIA scores for each paper.
- **Filter**: Return only the papers with a high Relevance score.
- **Export**: Save the processed data into a JSONL file.

### 2. `final_combined_tldr_and_s2orc.jsonl`
This JSONL (JSON Lines) file contains the processed data, which is a combination of TLDR summaries and S2ORC (Semantic Scholar Open Research Corpus) data. Each line in the file represents a JSON object with fields capturing various aspects of research papers from the Semantic Scholar corpus. 

Please note that this file is a sample, not the entirety of the filtered dataset. We will release the full dataset filtered and ranked by relevance to veganism in the near future.

Because this file is too large to upload directly to GitHub, please [download it here via Google Drive.](https://drive.google.com/file/d/1nLhRrVn0FeB1gcPPAXfHNlF8naoW_fo_/view?usp=sharing)


Should I run the ipynb? I've requested an API key, but it might take some time. Or should I use the final_combined_tldr_and_s2orc.jsonl --  or do you have a full version on google drive (or on cloud storage) which I could download? 
Sam Tucker - Open Paws — 09/05/2024 3:09 PM
Use the final filtered version with the link on Google Drive, running the script has literally taken weeks and it's still not fully done haha it's a huge dataset
Pranav Banuru — 09/05/2024 3:30 PM
Haha ok sounds good
Pranav Banuru — 09/05/2024 7:00 PM
Scroll is not working on webpage feedback for the website
Adding overflow auto to these two places will fix it
Image
Pranav Banuru — 09/05/2024 7:18 PM
on the left side (this picture is local but it applies to the live site too)
Image
Aditi — 09/05/2024 9:11 PM
@Sam Tucker - Open Paws How are we thinking about classifying images into the different language folders? Some images are just photos (with no written content) so can be put into all folders. Some images have written content so they would need to be put into into their respective language folders. Is that the correct way of thinking about it? If so, I'd somehow need get my script to detect text within an image...
Sam Tucker - Open Paws — 09/05/2024 9:43 PM
Yes I think any image without text can go in all language folders and images with text should go in their corresponding language folder. The easiest way to deal with this will be using the tesseract OCR library, you can have it extract and return the text (which can then be filtered by language) or mark it as a text-free image if the response is empty. 

Here's a sample of what that might look like in code:

import pytesseract
from PIL import Image

image = Image.open("image.jpg")
text = pytesseract.image_to_string(image)

if len(text.strip()) > 0:
    print("Image contains text")
    print("Detected text:", text)
else:
    print("No text detected")
This library is free and open source, so no auth key is needed
Sam Tucker - Open Paws — 09/05/2024 10:04 PM
Thank you! Has this been pushed to live yet? On my end the scroll isn't working when I tested it on the spanish web feedback project
Pranav Banuru — 09/05/2024 10:20 PM
I haven't made any changes is there a list of project ids for all the Web Page Feedback projects? (or project titles)
If I get that I'll try the sdk working on it
https://labelstud.io/sdk/project.html#label_studio_sdk.project.Project.set_params
or api
https://labelstud.io/api#tag/Projects/operation/api_projects_partial_update
to update 
Label Studio SDK
Label Studio - Data labeling, annotation and exploration tool
PapaVegan — 09/05/2024 10:34 PM
Sorry I've been afk for a bit. I'll try to get all of the projects finished with the storage configuration tomorrow, in about 10 hrs.
Pranav Banuru — 09/05/2024 10:43 PM
All good!! nw
PapaVegan — 09/06/2024 9:06 AM
I think I've recreated those missing storages now. Could you please rerun your script to double-check, @Pranav Banuru ?
PapaVegan — 09/06/2024 9:15 AM
FWIW, I uploaded the scripts I've been using to /scripts/project-management. Haven't written a readme yet.
Pranav Banuru — 09/06/2024 9:55 AM
Checking projects: 100%|██████████████████████████████████████████████████████| 765/765 [03:05<00:00,  4.11project/s]
Projects without input storage buckets:
Project ID: 3096, Title: Feedback Resp [Português - EU] (Portuguese - EU)
Project ID: 3095, Title: Geração Resps [Português - EU] (Portuguese - EU)
Project ID: 3085, Title: Resposta Eco [Português - BR] (Portuguese - BR)
Project ID: 3073, Title: Gerar Resposta [Português - BR] (Portuguese - BR)
Project ID: 3071, Title: Feedback Texto [Português - EU] (Portuguese - EU)
Project ID: 3070, Title: Feedback texto [Português - BR] (Portuguese - BR)
Project ID: 3069, Title: Feedback imagem [Português - BR] (Portuguese - BR)
Project ID: 3068, Title: Feedback Web [Português - EU] (Portuguese - EU)
Project ID: 3067, Title: Feedback Imagem [Português - EU] (Portuguese - EU)
Project ID: 3065, Title: Comentários Web [Português - BR] (Portuguese - BR)

When I select the language selector for either portuguese, no projects show up despite them having ids
project_ids = [3096, 3095, 3085, 3073, 3071, 3070, 3069, 3068, 3067, 3065] 
Pranav Banuru — 09/06/2024 11:35 AM
Thanks! checking the label config for specific tags helped me, got the list of the projects in each category now.
Pranav Banuru — 09/06/2024 3:11 PM
Ok scrolling on web is 👍 now
Sam Tucker - Open Paws — 09/06/2024 10:36 PM
Everything is looking great, thank you all so much for all your hard work on this! One minor thing I noticed is that it seems like the pages might be group together, for example on web page feedback it returns African Animal Media pages only and I think you'd have to go through every single AAM page to get to any other pages. Is there a simple way that we can shuffle the order of the tasks so that it mixes it up more for users? Otherwise we may end up with many rankings for websites at the beginning of the list and none for those at the end?
Sam Tucker - Open Paws — 09/06/2024 11:29 PM
This also seems to be the case with other projects like feedback generation where you have to go through all the climate disclosure questions from the anthropic dataset to get to any other questions
Sam Tucker - Open Paws — 09/06/2024 11:37 PM
I'm also getting this error pop up a lot on image feedback, which seems to all come from this link: https://corsproxy.io/?https%3A//africaanimalmedia.com/wp-content/themes/assets/../assets/img/jeg-empty.png

It might be worth deduplicating the URLs within image feedback as it seems to all be the same image causing this
Image
Pranav Banuru — 09/06/2024 11:46 PM
There is a random sampling setting in project settings that might work and could be enabled (though I think Colin wrote some code to randomize? )

It'll be tough for me to take a look for a few days.
Pranav Banuru — 09/06/2024 11:47 PM
Here
Sam Tucker - Open Paws — 09/06/2024 11:49 PM
I believe that code is just to pull a random project if "no more tasks left" is showing, we'd probably be better off using the random sampling settings in project settings, I'll have a look into how to do this through the API
It doesn't look like there's an option to change this through the API but it can be done manually through the UI, I'll go through and do it, so in the meantime is anyone able to have a look at deduplicating the image buckets so there are no repeated URLs?
Sam Tucker - Open Paws — 09/07/2024 12:11 AM
Since I've been adding random sampling in the UI I've also been resyncing with the buckets and I've noticed a lot of them did have unsynced tasks, so just a remind that any scripts that add data to the buckets should also end with an API call to sync the bucket with label studio: https://labelstud.io/api#tag/Storage:-GCS/operation/api_storages_gcs_sync_create

Don't worry about this for any data already uploaded as I'll sync everything now, but just something to note for going forward that label studio doesn't automatically sync with either import or export buckets
Sam Tucker - Open Paws — 09/07/2024 12:20 AM
Text and image feedback buckets in English failed to sync through the UI just now, will test if this is the case for other languages soon
Image
Sam Tucker - Open Paws — 09/07/2024 12:47 AM
It also happened for text feedback in Portugues BR, but not for image feedback
Image
Sam Tucker - Open Paws — 09/07/2024 3:25 AM
This project sync failed too
Image
This is happening with all projects in Malay, only for the input buckets though, the output buckets are syncing fine
Sam Tucker - Open Paws — 09/07/2024 6:18 AM
I've now set all projects to random sampling and resycned all projects, the only one that has failed is "Maklum Balas Maklum Balas [Bahasa Melayu] (Malay)" which has given this error message:

Error logs for gcs storage 694 in project 2716 and job null:

  File "/label-studio/label_studio/io_storages/gcs/utils.py", line 267, in read_file
    raise ValueError(
ValueError: Error on key response-feedback-Malayalam/: For GCS your JSON file must be a dictionary with one task.


meta = {"attempts":6,"duration":0.120786,"time_queued":"2024-09-07 12:17:57.104055+00:00","time_failure":"2024-09-07 12:17:57.238350+00:00","time_last_ping":"2024-09-07 12:17:57.117564+00:00","time_in_progress":"2024-09-07 12:17:57.117564+00:00"}
For the Malay language, it's also showing results for another language called Malayalam
Image
The "Ewe" language is also showing results from multiple other languages where the string "ewe" appears elsewhere in the project title
Image
Sam Tucker - Open Paws — 09/07/2024 6:27 AM
In order of importance, here are the most urgent next steps:

1) Finish uploading the synthetic_seed_data files so that there are at least some projects in all languages (currently many languages don't have any projects, it may take a while to get web data for all languages, but we should be able to fill in all response generation and feedback projects with synthetic_seed_data)

2) Add images without text to all image buckets (so that there are images to rank in image feedback for all languages)

3) Deduplicate the image data so there are no repeated URLs (there are currently many double ups of broken links to removed images)

4) Fix the language filtering for Ewe and Malay languages.

I'm going to be travelling all day tomorrow to get to Poland for the CARE conference, but I'll be back online after that. If anyone is able to start working on these tasks before then that would be hugely appreicated and I can assist with these tasks after I've finished travelling the day after tomorrow 🙂
PapaVegan — 09/07/2024 6:19 PM
I can work on the ewe and Malay issue.
PapaVegan — 09/09/2024 1:59 PM
I'm trying to carefully reinstate the api-based project filtering along with the language processing Ewe and Malay issue, so things load more quickly. 

I don't want to disrupt production, so it's time to make a staging/testing instance! Our end users will never see it. I think it could use the same database as the production instance (if we're testing ONLY frontend changes), or we can take a snapshot/clone of our database and run a test instance off of it. WDYT?
Sam Tucker - Open Paws — 09/10/2024 7:43 AM
I think that using the same DB if we're only testing front end changes
Also, the Global Animal Law Association just recently signed a data sharing agreement so now we have a new dataset with all of the animal welfare legislation that exists in the world! https://github.com/Open-Paws/Datasets/tree/main/animal_welfare_legislation
GitHub
Datasets/animal_welfare_legislation at main · Open-Paws/Datasets
Datasets relevant to veganism and/or animal rights, plus the scripts used to collect and process them. These datasets are intended for use in developing AI systems and tools that are aligned with e...
Datasets/animal_welfare_legislation at main · Open-Paws/Datasets
Sam Tucker - Open Paws — 09/10/2024 1:28 PM
We also have a new dataset with text chunks for 213 vegan-focus GitHub repos! All repos either have permissive licences that allow any use or modification, or in some cases project owners have signed data sharing agreements with us: https://github.com/Open-Paws/Datasets/tree/main/github_repos
GitHub
Datasets/github_repos at main · Open-Paws/Datasets
Datasets relevant to veganism and/or animal rights, plus the scripts used to collect and process them. These datasets are intended for use in developing AI systems and tools that are aligned with e...
Datasets/github_repos at main · Open-Paws/Datasets
PapaVegan — 09/10/2024 4:26 PM
Any user/usability reports you've recieved yet?
Sam Tucker - Open Paws — 09/11/2024 1:35 AM
Not yet, just waiting for the synthetic seed data to be uploaded before actually officially launching feedback collection so that there are at least some projects with data available in all languages
Aditi — 09/11/2024 2:27 AM
Sorry team, just been recovering from sickness the past week. I'm gonna work on uploading the synthetic seed data into GCP tonight and let you all know how it goes
Sam Tucker - Open Paws — 09/11/2024 2:29 AM
No stress it's completely understandable and nothing is more urgent than your health! Looking forward to hearing how things go with the upload and hope you're feeling better now 🙂
Aditi — 09/11/2024 3:03 AM
Thanks Sam, really appreciate your patience here 🙂
Aditi — 09/11/2024 3:55 AM
@PapaVegan do you remember what the fix was for this error which I believe we saw when we were first trying to upload tasks into GCP?
ERROR: (gcloud.alpha.storage.cp) Destination (gs://label-studio-input-open-paws/response-generation-Aymara/) must match exactly one URL.
PapaVegan — 09/11/2024 8:04 AM
I'm not certain, but the issue could be the trailing slash in the destination, or the lack of a filename? Could you share the call being made?
Thread
I'm not certain, but the issue could be
5 Messages ›
PapaVegan
22h ago
Aditi
 started a thread: 
I'm not certain, but the issue could be
. See all 
threads
.
 — 09/11/2024 4:17 PM
﻿
PapaVegan — 09/11/2024 8:04 AM
I'm not certain, but the issue could be the trailing slash in the destination, or the lack of a filename? Could you share the call being made?
Aditi — 09/11/2024 4:17 PM
@PapaVegan Yes, here's the script -- it's similar to what I used last time except that now I'm trying to import whole folders instead of individual files within those folders to maintain some form of organisation within the GCP buckets
import os
import subprocess
from google.cloud import storage

# Generate a list of folders in the sub folders
aligned_qna_path = "Aligned QnA/tasks"
Expand
import_into_gcp.py
3 KB
Aditi — Yesterday at 4:12 PM
Happy to get on a call today or tomorrow (during our weekly) to work this out
PapaVegan — Yesterday at 6:30 PM
Yes, let's meet tomorrow. We could have a working session earlier than the meeting, too.
Aditi — Yesterday at 6:34 PM
Sounds good! Should we start about 15 mins earlier than the usual meeting time?
PapaVegan — Yesterday at 6:34 PM
Sure, sounds like a plan.
﻿
import os
import subprocess
from google.cloud import storage

# Generate a list of folders in the sub folders
aligned_qna_path = "Aligned QnA/tasks"
controversial_path = "Controversial QnA/tasks"

aligned_folders = [name for name in os.listdir(aligned_qna_path) if os.path.isdir(os.path.join(aligned_qna_path, name))]
controversial_folders = [name for name in os.listdir(controversial_path) if os.path.isdir(os.path.join(controversial_path, name))]


# Iterate through the aligned folders
failed_uploads_aligned = []

for folder_name in aligned_folders:
    sub_folder = os.path.join(aligned_qna_path, folder_name)
    print(sub_folder)
    if os.path.exists(sub_folder):
        # GCP bucket name
        bucket_name = f"label-studio-input-open-paws/response-generation-{folder_name.split('_')[-1]}"
        # Transfer the entire folder using gsutil
        command = f"gcloud alpha storage cp -r {sub_folder} gs://{bucket_name}/"
        print(command)
        subprocess.run(command, env=os.environ, shell=True)
        print(f"Transferred folder {sub_folder} to gs://{bucket_name}/")
    else:
        print(f"Sub-folder {sub_folder} does not exist.")
        failed_uploads_aligned.append(sub_folder)


if failed_uploads_aligned:
    print("Failed uploads in Aligned folder:")
    for failed in failed_uploads_aligned:
        print(failed)
else:
    print("All folders uploaded successfully.")



# Iterate through the Controversial folders
failed_uploads_controversial = []

for folder_name in controversial_folders:
    sub_folder = os.path.join(controversial_path, folder_name)
    print(sub_folder)
    if os.path.exists(sub_folder):
        # GCP bucket name
        bucket_name = f"label-studio-input-open-paws/response-generation-{folder_name.split('_')[-1]}"
        # Transfer the entire folder using gsutil
        command = f"gcloud alpha storage cp -r {sub_folder} gs://{bucket_name}/"
        print(command)
        subprocess.run(command, env=os.environ, shell=True)
        print(f"Transferred folder {sub_folder} to gs://{bucket_name}/")
    else:
        print(f"Sub-folder {sub_folder} does not exist.")
        failed_uploads_aligned.append(sub_folder)


if failed_uploads_controversial:
    print("Failed uploads in Controversial folder:")
    for failed in failed_uploads_controversial:
        print(failed)
else:
    print("All folders uploaded successfully.")
import_into_gcp.py
3 KB