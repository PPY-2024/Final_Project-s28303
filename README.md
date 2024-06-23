# Text Converter Web Application

## Description

This web application provides a user-friendly interface for converting text in various ways:

1. Emojify: Add emojis to your text
2. Text to LinkedIn: Convert text into a professional LinkedIn post
3. Text to Prompt: Generate an AI prompt from your text

The application uses the Anthropic API for text processing and stores conversion history in a SQLite database.

## Features

- Responsive design using Bootstrap
- Dynamic title and label changes for each conversion type
- Conversion history for each type
- Docker containerization for easy deployment

## Technologies Used

- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- API: Anthropic
- Database: SQLite
- Containerization: Docker, Docker Compose

## Setup and Running

1. Clone the repository
2. Replace `your_api_key_here` in `docker-compose.yml` with your Anthropic API key
3. Run `docker-compose up --build`
4. Access the application at `http://localhost:5000`

## Usage

1. Select the desired conversion type from the navigation menu
2. Enter your text in the input field
3. Click "Convert" to see the result
4. View previous conversions in the history section
