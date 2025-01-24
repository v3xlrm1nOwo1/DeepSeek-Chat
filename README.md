

## DeepSeek-Chat Scraper

### Overview
The DeepSeek Chat Scraper is a Python-based automation tool designed to interact programmatically with the [DeepSeek Chat](https://chat.deepseek.com/). By leveraging the power of the Selenium WebDriver, this tool enables seamless communication with the chatbot, including logging in, sending messages, starting new chats, and capturing responses.

Whether you're conducting research, building automated workflows, or collecting data for analysis, this scraper provides a robust foundation to integrate DeepSeek into your projects. It is optimized for performance with features like automated chunked message input for handling long texts, and graceful session management.

### Features 

- **Login Automation**: Automatically log in to the DeepSeek chatbot platform with email and password.  
- **Message Sending**: Send text messages in chunks to handle input size limitations.  
- **Session Management**: Includes logout and clean shutdown functionalities.  
- **New Chat Creation**: Start fresh conversation threads.  
- **DeepThink Mode (R1)**: Activate advanced processing for comprehensive, multi-step analysis of queries.  

### Install Required Dependencies
Use `pip` to install the required Python libraries:

```bash
pip install selenium
```

### Example Basic Usage Code 
Below is a step-by-step guide to get started with the DeepSeek Chatbot Scraper:

```python
from deepseek_chat import DeepSeek

# Initialize the DeepSeek class
deepseek = DeepSeek(email="your_email@example.com", password="your_password")

# Activate deep think mode
deepseek.deepthink()

# Send a message and capture the response
response = deepseek.send_text("uwu")
print("DeepSeek response:", response)

# Send a message and capture the response
response = deepseek.send_text("Hii, DeepSeek!")
print("DeepSeek response:", response)

# Start a new chat
deepseek.create_new_chat()

# Send a message and capture the response
response = deepseek.send_text("How are you!!!")
print("DeepSeek response:", response)

# Log out from account
deepseek.logout()

# quit the session
deepseek.quit()
```

### TODO List
- [x] **Login/Logout** Full authentication workflow.
- [x] **Text Messaging** Chunked input handling (500 characters per chunk).  
- [x] Create new chat threads.
- [x] Activate DeepThink analysis mode.  
- [x] Clean session termination.
- [ ] Image/file uploads **not supported**.
- [ ] The code uses fragile `XPath/CSS` selectors that may break with website updates.
