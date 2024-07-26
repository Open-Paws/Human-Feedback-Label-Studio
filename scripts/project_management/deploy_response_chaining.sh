#!/bin/bash

# Define variables
FUNCTION_NAME="process_new_conversation_output_files_in_bucket"
RUNTIME="python39"
TRIGGER_RESOURCE="label-studio-output"
TRIGGER_EVENT="google.storage.object.finalize"
SOURCE_PATH="./response_chaining_cloud_function"  # Update this to the path of your Python file
ENTRY_POINT="process_new_conversation_output_files_in_bucket"

# Deploy the Cloud Function
gcloud functions deploy $FUNCTION_NAME \
    --runtime $RUNTIME \
    --trigger-resource $TRIGGER_RESOURCE \
    --trigger-event $TRIGGER_EVENT \
    --entry-point $ENTRY_POINT \
    --source $SOURCE_PATH \