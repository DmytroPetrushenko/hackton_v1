from entities.launchers.launcher_phishing_graph import launcher_phishing_graph
from entities.states import PhishingState

# model = creat_bedrock_llm(model_name=MODEL.LLAMA_31_405B_INSTRUCT)
# response = model.invoke('Hello') # invoke the model
# print(response.content)  # print the response


# def main():
#     creds = validate_and_generate(token_file='token.pickle', credentials_file='credentials.json')
#     if creds.valid:
#         print("Token is valid and ready to use.")
#     else:
#         print("Failed to generate a valid token.")
#
#
# if __name__ == "__main__":
#     main()

initial_state: PhishingState = {
    "messages_id": set(),  # IDs of all messages (processed and unprocessed)
    "senders": [],      # Sources of incoming data
    "error": [],        # List of errors during processing
    "phishing_ids": set()
}
print(launcher_phishing_graph(initial_state))


