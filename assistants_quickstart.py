
from openai import OpenAI
import shelve
from dotenv import load_dotenv
import os
import time
import logging

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
def get_openai_assistant_id():
    return os.getenv("OPENAI_ASSISTANT_ID")
OPENAI_ASSISTANT_ID = get_openai_assistant_id()
OPENAI_ASSISTANT_NAME = os.getenv("OPENAI_ASSISTANT_NAME")
client = OpenAI(api_key=OPENAI_API_KEY)

# --------------------------------------------------------------
# Upload file
# --------------------------------------------------------------

# # Create a vector store
# vector_store = client.beta.vector_stores.create(name="Hotel FAQs")
 
# # Ready the files for upload to OpenAI
# file_paths = ["data/airbnb-faq.pdf", "data/Brief_FAQ_for_first-time_Airbnb_users.pdf", "data/How_to_Ask_for_a_Budget_Property_on_Airbnb.pdf", "data/How_to_Ask_for_the_Best_Budget_Value_Property_on_Airbnb.pdf"]
# file_paths = ["data/airbnb-faq_2.pdf"]
# file_streams = [open(path, "rb") for path in file_paths]
# # Use the upload and poll SDK helper to upload the files, add them to the vector store,
# # and poll the status of the file batch for completion.
# file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
#   vector_store_id=vector_store.id, files=file_streams
# )
 
# # You can print the status and the file counts of the batch to see the result of this operation.
# print(file_batch.status)
# print(file_batch.file_counts)

# --------------------------------------------------------------
# Create assistant
# --------------------------------------------------------------

# def create_assistant():
#     assistant = client.beta.assistants.create(
#         name="WhatsApp AirBnb Assistant",
#         instructions="You're a helpful WhatsApp assistant that can assist guests that are staying in our Paris AirBnb. Use your knowledge base to best respond to customer queries. Use direct answers whenever possible. If you don't know the answer, say simply that you cannot help with question and advice to contact the host directly. Be friendly. Keep answers short and concise.",
#         model="gpt-4o",
#         tools=[{"type": "file_search"}],
#     )
#     return assistant

# # Create the assistant
# assistant = create_assistant()

# assistant = client.beta.assistants.update(
# #   assistant_id=assistant.id,
#   assistant_id = OPENAI_ASSISTANT_ID,
#   tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
# )

# --------------------------------------------------------------
# Thread management
# --------------------------------------------------------------
def check_if_thread_exists(wa_id):
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(wa_id, None)


def store_thread(wa_id, thread_id):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[wa_id] = thread_id


# --------------------------------------------------------------
# Generate response
# --------------------------------------------------------------
def generate_response(message_body, wa_id, name):
    # Check if there is already a thread_id for the wa_id
    thread_id = check_if_thread_exists(wa_id)

    # If a thread doesn't exist, create one and store it
    if thread_id is None:
        print(f"Creating new thread for {name} with wa_id {wa_id}")
        thread = client.beta.threads.create()
        store_thread(wa_id, thread.id)
        thread_id = thread.id

    # Otherwise, retrieve the existing thread
    else:
        print(f"Retrieving existing thread for {name} with wa_id {wa_id}")
        thread = client.beta.threads.retrieve(thread_id)
    
    print(f"Operating Assistant - {OPENAI_ASSISTANT_NAME}")

    # Add message to thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_body,
    )

    # Run the assistant and get the new message
    new_message = run_assistant(thread)
    # print(f"To {name}:", new_message)
    return new_message


# --------------------------------------------------------------
# Run assistant
# --------------------------------------------------------------
def run_assistant(thread):
    # Retrieve the Assistant
    assistant = client.beta.assistants.retrieve(OPENAI_ASSISTANT_ID)

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=OPENAI_ASSISTANT_ID,
    )

    # Wait for completion
    while run.status != "completed":
        time.sleep(1.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Retrieve the Messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value
    return new_message


# --------------------------------------------------------------
# Test assistant
# --------------------------------------------------------------

# new_message = generate_response("What's the check in time?", "123", "John")
