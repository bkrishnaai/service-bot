# Quick Setup Instructions

## 1. Run `service_bot.py` for Faster Responses

- **Download Files:**
  - Download the `service_bot.py` file and the PDF file from the provided link.
  - Save them to your computer.

- **Update PDF Path:**
  - Open `service_bot.py` in a text editor.
  - Go to line 68 and update the PDF path to where you saved the PDF file.
  - Example: `pdf_path = "/path/to/your/file.pdf"`

- **Install Required Libraries:**
  - Open your terminal or command prompt.
  - Run the following command to install the necessary libraries:
    ```sh
    pip install PyPDF2 google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
    ```

- **Run the Script:**
  - In your terminal or command prompt, navigate to the directory where `service_bot.py` is saved.
  - Run the script with:
    ```sh
    python service_bot.py
    ```

## 2. Using Streamlit for a Web Interface

- **Download PDF File:**
  - Download the PDF file from the provided link and save it to your computer.

- **Update PDF Path in Streamlit:**
  - Open `streamlit_app.py` in a text editor.
  - On line 66, update the PDF path to where you saved the file.
  - Example: `pdf_path = "/path/to/your/file.pdf"`

- **Install Required Libraries:**
  - Open your terminal or command prompt.
  - Run the following command to install the necessary libraries:
    ```sh
    pip install streamlit PyPDF2 google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
    ```

- **Run the Streamlit App:**
  - In your terminal or command prompt, navigate to the directory where `streamlit_app.py` is saved.
  - Run the app with:
    ```sh
    streamlit run streamlit_app.py
    ```
