import tkinter as tk
from openai import OpenAI

client = OpenAI()

def sendChat():
    # Retrieve the user's input from the bottom prompt text widget
    user_input = bottomPromptText.get("1.0", tk.END).strip()

    if not user_input:
        return  # Do nothing if the input is empty

    # Create chat completion
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    # Get the response content
    prompt_response = completion.choices[0].message.content

    # Enable the text widget to update content
    mainText.config(state=tk.NORMAL)
    
    # Insert the user prompt and assistant response with colour tags
    mainText.insert(tk.END, f"User: {user_input}\n", "user")
    mainText.insert(tk.END, f"Assistant: {prompt_response}\n\n", "assistant")

    # Scroll to the end to show the latest content
    mainText.yview(tk.END)

    # Disable the text widget to prevent editing
    mainText.config(state=tk.DISABLED)

    # Clear the bottom prompt text widget
    bottomPromptText.delete("1.0", tk.END)

def on_focus_in(event):
    current_text = bottomPromptText.get("1.0", tk.END).strip()
    if current_text == "Enter your text here...":
        bottomPromptText.delete("1.0", tk.END)
        bottomPromptText.config(fg="#ffffff")  # Set text color to white

def on_focus_out(event):
    current_text = bottomPromptText.get("1.0", tk.END).strip()
    if not current_text:
        bottomPromptText.insert("1.0", "Enter your text here...")
        bottomPromptText.config(fg="#aaaaaa")  # Set text color to grey

def on_enter_key(event):
    sendChat()
    return "break"  # Prevents the default behavior of adding a newline

window = tk.Tk()
window.title("ChatGPT Wrapper Interface")

# Fullscreen
window.state("zoomed")

# Icon
window.iconbitmap("./favicon.ico")

# Size
window.geometry("600x400")
window.minsize(600, 400)
window.resizable(True, True)

# Background color
window.config(bg="#2f2f2f")

# Frame for conversation history
conversationFrame = tk.Frame(window, bg="#2f2f2f")
conversationFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10, padx=10)

# Label for conversation history
conversationLabel = tk.Label(conversationFrame, text="Conversation History", bg="#2f2f2f", fg="#ffffff", font=("Arial", 12))
conversationLabel.pack(anchor=tk.W)

# Main text widget for conversation history (set to read-only)
mainText = tk.Text(conversationFrame, bg="#2f2f2f", fg="#ffffff", font=("Arial", 12), state=tk.DISABLED)
mainText.pack(fill=tk.BOTH, expand=True)

# Define tags for user and assistant messages
mainText.tag_configure("user", foreground="#00ff00")  # User text colour
mainText.tag_configure("assistant", foreground="#ff0000")  # Assistant text colour

# Frame for bottom prompt and send button
bottomPromptFrame = tk.Frame(window, bg="#2f2f2f")
bottomPromptFrame.pack(side=tk.BOTTOM, fill=tk.X, pady=5, padx=10)

# Label explaining the prompt
promptLabel = tk.Label(bottomPromptFrame, text="Enter your text below:", bg="#2f2f2f", fg="#ffffff", font=("Arial", 12))
promptLabel.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))

# Bottom prompt text widget
bottomPromptText = tk.Text(bottomPromptFrame, width=90, height=3, bg="#2f2f2f", fg="#aaaaaa", font=("Arial", 12))
bottomPromptText.grid(row=1, column=0, sticky=tk.W+tk.E, padx=(0, 5))
bottomPromptText.bind("<FocusIn>", on_focus_in)
bottomPromptText.bind("<FocusOut>", on_focus_out)
bottomPromptText.bind("<Return>", on_enter_key)  # Bind Enter key to sendChat

# Send Chat button
sendChatButton = tk.Button(bottomPromptFrame, text="Send Chat", command=sendChat, bg="#2f2f2f", fg="#ffffff", font=("Arial", 12))
sendChatButton.grid(row=1, column=1, sticky=tk.E)

# Run main loop
bottomPromptText.focus()
window.mainloop()
