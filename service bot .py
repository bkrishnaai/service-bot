import google.generativeai as genai
import PyPDF2
import sqlite3

# Set up Google Gemini API
api_key = "AIzaSyAXdLysf8fUUKaJcAhoxrZt3ObwkKTpxIA"
genai.configure(api_key=api_key)

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file and formats it for readability."""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            raw_text = page.extract_text()
            if raw_text:
                # Replace newlines and excessive spaces with a single space
                formatted_text = ' '.join(raw_text.split())
                # Optional: Add custom formatting rules here
                text += formatted_text + "\n\n"
    return text

def query_gemini(prompt):
    """Queries Google Gemini API with a prompt."""
    try:
        response = genai.generate_text(prompt=prompt)
        if hasattr(response, 'candidates') and len(response.candidates) > 0:
            # Clean up response text
            result = response.candidates[0]['output'].strip()
            return result if result else "No relevant information found."
        else:
            return "No valid response from API."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def format_text(text):
    """Formats the text into readable sentences."""
    # Replace bullet points and colons with appropriate formatting
    formatted_text = text.replace('●', '\n- ').replace(':', ': ').replace('\n\n', '\n')
    return formatted_text.strip()

def create_db():
    """Creates a database for storing user details."""
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT,
                      email TEXT,
                      phone TEXT,
                      service TEXT,
                      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def save_user_details(name, email, phone, service):
    """Saves user details to the database."""
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users (name, email, phone, service) 
                      VALUES (?, ?, ?, ?)''', (name, email, phone, service))
    conn.commit()
    conn.close()

def main():
    print("Hi there! I'm here to help you with your queries about services. How can I assist you today?")

    pdf_path = "D:\\bot\\SC data (1).pdf"
    pdf_text = extract_text_from_pdf(pdf_path)
    formatted_text = format_text(pdf_text)

    create_db()

    while True:
        user_query = input("You: ").strip()

        # Basic responses handling
        if user_query.lower() in ['hi', 'hello']:
            print("Bot: Hello! What can I do for you today?")
        elif user_query.lower() in ['bye', 'goodbye']:
            print("Bot: Goodbye! Have a great day!")
            break
        elif user_query.lower() in ['thanks', 'thank you']:
            print("Bot: You're welcome! If you need more help, just ask.")
        elif user_query.lower() == '1':
            print("Bot: Stopping execution. Have a great day!")
            break
        else:
            # Construct prompt and query the API
            full_prompt = f"{formatted_text}\n\nUser Query: {user_query}"
            response = query_gemini(full_prompt)
            print("Bot:", response)

            # Ask if the user needs further assistance
            needs_help = input("Bot: Do you need further assistance? (yes/no): ").strip().lower()

            if needs_help == 'yes':
                # Provide dummy contractor numbers
                print("Bot: Here are some dummy contractor numbers for further assistance:")
                print("Contractor 1: (123) 456-7890")
                print("Contractor 2: (987) 654-3210")
                print("Contractor 3: (555) 555-5555")
                print("Contractor 4: (444) 444-4444")

                # Ask for user details
                user_name = input("Bot: Please provide your name: ").strip()
                user_email = input("Bot: Please provide your email: ").strip()
                user_phone = input("Bot: Please provide your phone number: ").strip()

                # Save user details
                save_user_details(user_name, user_email, user_phone, "Service needed not specified")
                
                # Confirm and exit
                print("Bot: Thank you for providing your details. Our team will contact you shortly.")
                break
            
            elif needs_help == 'no':
                # Exit if no further assistance is needed
                print("Bot: Okay, if you need anything else, feel free to ask. Have a great day!")
                break

if _name_ == "_main_":
    main()