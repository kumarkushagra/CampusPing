from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load the pre-trained DialoGPT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Initialize chat history
chat_history = torch.tensor([]).long()  # Ensure it's a tensor of long integers

def chat_with_model(user_input):
    """
    Generates a response to the user's input using DialoGPT.
    
    Args:
        user_input (str): The user's input.
        
    Returns:
        str: The model's response.  
    """
    global chat_history  # Declare chat_history as global to modify it

    # Encode the user's input and append it to the chat history
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    if chat_history.numel() == 0:
        bot_input_ids = new_user_input_ids
    else:
        bot_input_ids = torch.cat([chat_history, new_user_input_ids], dim=-1)

    # Generate a response from the model
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # Extract and decode the model's response
    chat_history_ids = chat_history_ids[:, bot_input_ids.shape[-1]:]
    bot_response = tokenizer.decode(chat_history_ids[0], skip_special_tokens=True)

    # Update chat history
    chat_history = chat_history_ids

    return bot_response

# Example conversation
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Bot: Goodbye!")
        break
    response = chat_with_model(user_input)
    print(f"Bot: {response}")
