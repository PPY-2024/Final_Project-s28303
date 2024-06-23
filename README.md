### Description
This web application provides a user-friendly interface for converting text in various ways:

Emojify: Add emojis to your text
Text to LinkedIn: Convert text into a professional LinkedIn post
Text to Prompt: Generate an AI prompt from your text

The application uses the Anthropic API for text processing and stores conversion history in a SQLite database.
Features

Responsive design using Bootstrap
Dynamic title and label changes for each conversion type
Conversion history for each type
Docker containerization for easy deployment

### Technologies Used

Frontend: HTML, CSS, JavaScript
Backend: Python, Flask
API: Anthropic
Database: SQLite
Containerization: Docker, Docker Compose

### Setup and Running

Clone the repository
Replace your_api_key_here in docker-compose.yml with your Anthropic API key
Run _docker-compose up --build_
Access the application at _http://localhost:5000_

**Usage**

Select the desired conversion type from the navigation menu
Enter your text in the input field
Click "Convert" to see the result
View previous conversions in the history section
