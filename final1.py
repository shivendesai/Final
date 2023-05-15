#Written by Shiven Desai
import openai
import time

# Set the OpenAI API key
openai.api_key = "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"

# Define the ChatGPT class
class ChatGPT:
    def __init__(self):
        # Initialize the chat history list and timeout value
        self.chat_history = []
        self.timeout = 5

    def send_message(self, message):
        try:
            # Send the user's message to the OpenAI API and get the AI's response
            response = openai.Completion.create(
                engine="davinci",
                prompt=f"{self.chat_history}User: {message}\nAI:",
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.7,
            )

            # Add the user's message and the AI's response to the chat history as a tuple
            self.chat_history.append(('User', message))
            self.chat_history.append(('AI', response.choices[0].text))

            # Return the AI's response
            return response.choices[0].text

        except openai.error.RateLimitError:
            # If the API call hits the rate limit, wait and try again
            time.sleep(self.timeout)
            self.timeout *= 2
            return "Sorry, the service is temporarily unavailable. Please try again later."

        except Exception as e:
            # If any other error occurs, return the error message
            return f"An error occurred: {e}"

    def clear_history(self):
        # Clear the chat history list
        self.chat_history = []
        return "Chat history cleared."

    def show_history(self):
        # Create a dictionary to store the chat history
        history_dict = {}
        for i, (sender, message) in enumerate(self.chat_history):
            history_dict[f'{sender} {i+1}'] = message

        # Return the chat history dictionary
        return history_dict

# Create an instance of the ChatGPT class
chatbot = ChatGPT()

# Start the main repeat loop
for i in range(2):
    # Get user input
    user_input = input("User: ")

    if user_input.lower() == "clear":
        # If the user wants to clear the chat history, call the clear_history method
        print(chatbot.clear_history())

    elif user_input.lower() == "history":
        # If the user wants to see the chat history, call the show_history method
        print(chatbot.show_history())

    else:
        # Otherwise, send the user's message to the chatbot and print the response
        print(chatbot.send_message(user_input))
