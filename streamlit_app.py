import streamlit as st
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
                formatted_text = ' '.join(raw_text.split())
                text += formatted_text + "\n\n"
    return text

def query_gemini(prompt):
    """Queries Google Gemini API with a prompt."""
    try:
        response = genai.generate_text(prompt=prompt)
        if hasattr(response, 'candidates') and len(response.candidates) > 0:
            result = response.candidates[0]['output'].strip()
            return result if result else "No relevant information found."
        else:
            return "No valid response from API."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def format_text(text):
    """Formats the text into readable sentences."""
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
    st.title("Service Query Bot")

    # Load and format PDF text
    pdf_path = "D:\\bot\\SC data (1).pdf"
    pdf_text = extract_text_from_pdf(pdf_path)
    formatted_text = format_text(pdf_text)

    # Create database
    create_db()

    # User input for queries
    user_query = st.text_input("You:", "")
    
    if user_query:
        # Construct prompt and query the API
        full_prompt = f"{formatted_text}\n\nUser Query: {user_query}"
        response = query_gemini(full_prompt)
        st.write(f"Bot: {response}")

        # Ask if the user needs further assistance
        needs_help = st.radio("Do you need further assistance?", ("yes", "no"))

        if needs_help == "yes":
            # Provide dummy contractor numbers
            st.write("Here are some dummy contractor numbers for further assistance:")
            st.write("Contractor 1: (123) 456-7890")
            st.write("Contractor 2: (987) 654-3210")
            st.write("Contractor 3: (555) 555-5555")
            st.write("Contractor 4: (444) 444-4444")

            # Ask for user details
            user_name = st.text_input("Please provide your name:", "")
            user_email = st.text_input("Please provide your email:", "")
            user_phone = st.text_input("Please provide your phone number:", "")

            if user_name and user_email and user_phone:
                # Save user details
                save_user_details(user_name, user_email, user_phone, "Service needed not specified")
                st.write("Thank you for providing your details. Our team will contact you shortly.")
                st.stop()  # Stops further execution

        elif needs_help == "no":
            st.write("Okay, if you need anything else, feel free to ask. Have a great day!")
            st.stop()  # Stops further execution

if __name__ == "__main__":
    main()
