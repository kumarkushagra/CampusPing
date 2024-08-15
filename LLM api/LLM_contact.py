# from huggingface_hub import login
# login(token="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")


# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch

# # Load the DialoGPT model and tokenizer
# tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
# model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# # Function to handle conversation
# def chat_with_bot(user_input, chat_history_ids=None):
#     new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

#     # Append the new user input to the chat history
#     bot_input_ids = new_user_input_ids if chat_history_ids is None else torch.cat([chat_history_ids, new_user_input_ids], dim=-1)

#     # Generate a response from the model (reduced max_length for less resource usage)
#     chat_history_ids = model.generate(bot_input_ids, max_length=100, pad_token_id=tokenizer.eos_token_id)

#     # Decode the generated response
#     chat_output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
#     return chat_output, chat_history_ids

# # Start a conversation
# chat_history_ids = None
# while True:
#     user_input = input("You: ")
#     if user_input.lower() in ['exit', 'quit']:
#         break
#     response, chat_history_ids = chat_with_bot(user_input, chat_history_ids)
#     print("Bot:", response)

