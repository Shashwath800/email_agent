# 📧 AI-Powered Gmail Email Agent  

An **intelligent email assistant** that:  
- Reads your intent (e.g., "Send an extension request to my professor")  
- Generates a **polite, professional email** using **Mistral (via Ollama)**  
- Fetches contact details automatically from `contacts.json`  
- Sends the email securely through the **Gmail API**  

Perfect for students, professionals, and anyone who wants to automate **formal email drafting + sending**.  

---

## 🚀 Features  
- 🤖 AI-generated professional emails  
- 📇 Contact lookup from `contacts.json`  
- 🧑 Personalization using `user_profile.json` (Name, Enrollment ID, Professor info, etc.)  
- 📧 Gmail OAuth 2.0 authentication (`credentials.json` & `token.json`)  
- 🖥️ Works locally with **Mistral** running via [Ollama](https://ollama.ai)  

---

## 📂 Project Structure  
📁 email_agent
│── main.py # Main script (agent flow)
│── contacts.json # Store recipient names & emails
│── user_profile.json # User details (name, enrollment, professor data)
│── credentials.json # Google API credentials (download from Google Cloud)
│── token.json # Generated automatically after first Gmail login
│── README.md # Documentation

yaml
Copy code

---

## ⚙️ Setup & Installation  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/your-username/email_agent.git
cd email_agent
2️⃣ Install Dependencies
bash
Copy code
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests
3️⃣ Configure Gmail API
Go to Google Cloud Console

Enable Gmail API

Create OAuth 2.0 credentials → Download as credentials.json

Place it in the project root.

4️⃣ Setup Ollama (for Mistral)
Install Ollama

Run the Mistral model locally:

bash
Copy code
ollama run mistral
Ensure API runs at http://localhost:11434/api/generate

5️⃣ Add Contacts & Profile
contacts.json

json
Copy code
{
  "professor": "professor.email@university.edu",
  "manager": "manager.email@company.com"
}
user_profile.json

json
Copy code
{
  "name": "Shashwath M",
  "enrollment": "123456",
  "professors": {
    "professor": { "last_name": "Smith" }
  }
}
▶️ Usage
Run the agent:

bash
Copy code
python main.py
Example:

vbnet
Copy code
💬 What would you like to send? ➤ Request professor to extend submission deadline
Agent Flow:

Detect recipient from contacts.json

Generate polite email using Mistral

Send via Gmail API

✅ Output:

yaml
Copy code
📨 Email sent! Message ID: 1782a8fbc1234...
✨ Example Generated Email
Subject: Update regarding Professor

pgsql
Copy code
Dear Professor Smith,

I hope this message finds you well. I am writing to request an extension 
for my assignment submission. Due to unforeseen circumstances, I would 
like to submit it on 14 June 2025 instead of 10 June 2025. 

I sincerely apologize for any inconvenience caused and appreciate your 
understanding.

Thank you for your time and support.

Best regards,  
Shashwath M  
Enrollment: 123456
📌 Future Improvements
📎 Add support for attachments

🌍 Multi-language email drafting

⏰ Schedule emails automatically

📅 Integration with calendar reminders

