import os
from flask import Flask, request, jsonify, send_from_directory, render_template
import sqlite3
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

app = Flask(__name__)
anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


# init sqllite database
def init_db():
    conn = sqlite3.connect('searches.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS searches
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  input TEXT,
                  output TEXT,
                  type TEXT)''')
    conn.commit()
    conn.close()


init_db()


@app.route('/')
def serve_index():
    return render_template('index.html')


@app.route('/convert/<conversion_type>', methods=['POST'])
def convert_text(conversion_type):
    data = request.json
    text = data['text']

    if conversion_type == 'emojify':
        message = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"You are given a text input. Your task is to modify this text by adding an appropriate emoji after each word. The emoji should match the context of the word and the overall sentiment of the text as closely as possible.\n\nHere is the input text:\n<text>\n{text}\n</text>\n\nFollow these guidelines to complete the task:\n\n1. Read and understand the context and sentiment of the entire text.\n2. For each word in the text, select an emoji that best represents its meaning or context.\n3. Place the chosen emoji immediately after the word, with a space between the word and the emoji.\n4. If you cannot find a perfectly matching emoji for a word, choose the closest possible option or skip adding an emoji for that particular word.\n5. Maintain the original punctuation and capitalization of the text.\n6. Common words like articles (a, an, the) and prepositions (in, on, at, etc.) may not need emojis unless they significantly contribute to the meaning.\n\nHere are some examples to guide you:\n\nInput: \"I love sunny days at the beach\"\nOutput: I 😊 love ❤️ sunny ☀️ days 📅 at the beach 🏖️\n\nInput: \"The cat chased the mouse through the house\"\nOutput: The cat 🐱 chased 🏃 the mouse 🐭 through the house 🏠\n\nNow, modify the given text by adding appropriate emojis after each word. Provide your answer as a string without tags"
                }
            ]
        }

    elif conversion_type == 'linkedin':
        message = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"You are tasked with creating a LinkedIn post based on a given text. Your goal is to transform the provided content into an engaging, professional post suitable for the LinkedIn platform.\n\nHere is the text you will be working with:\n\n<input_text>\n{text}\n</input_text>\n\nTo create an effective LinkedIn post, follow these guidelines:\n\n1. Keep the post concise and to the point (ideally 1-3 paragraphs).\n2. Use a professional tone while maintaining an engaging voice.\n3. Include relevant hashtags (2-3) to increase visibility.\n4. If appropriate, pose a question or call-to-action to encourage engagement.\n5. Ensure the content is valuable and relevant to your professional network.\n\nFirst, analyze the input text to identify the main points, key ideas, or valuable insights. Then, craft a LinkedIn post that captures the essence of the text while adhering to the guidelines above.\n\nPresent your LinkedIn post within as string.\n\nRemember to maintain a professional tone throughout the post and focus on delivering value to your LinkedIn network."
                }
            ]
        }
    elif conversion_type == 'prompt':
        message = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"You are tasked with generating the best possible prompt based on a given context and text. Your goal is to create a prompt that will elicit the most relevant and useful response for the given situation.\n\nFirst, carefully read and analyze the following context:\n<context>\n{{CONTEXT}}\n</context>\n\nNow, consider the text that will be used as the basis for generating the prompt:\n<text>\n{text}\n</text>\n\nAnalyze both the context and the text, paying attention to:\n1. The main themes or topics present\n2. Any specific requirements or constraints mentioned in the context\n3. The tone and style of the text\n4. Key words or phrases that could be important for the prompt\n\nBased on your analysis, craft a prompt that:\n1. Addresses the main points from the context\n2. Incorporates relevant elements from the text\n3. Is clear, concise, and specific\n4. Encourages a detailed and relevant response\n\nConsider using techniques such as:\n- Open-ended questions\n- Specific instructions or guidelines\n- Requests for examples or explanations\n- Hypothetical scenarios related to the context and text\n\nBefore finalizing your prompt, review it to ensure it aligns with the context and effectively utilizes the given text.\n\nPresent your generated prompt as a string."
                }
            ]
        }
    else:
        return jsonify({'error': 'Invalid conversion type'}), 400

    response = anthropic.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0,
        messages=[
            message
        ]
    )

    result = response.content[0].text

    conn = sqlite3.connect('searches.db')
    c = conn.cursor()
    c.execute("INSERT INTO searches (input, output, type) VALUES (?, ?, ?)", (text, result, conversion_type))
    conn.commit()
    conn.close()

    return jsonify({'result': result})


@app.route('/previous_searches/<conversion_type>')
def get_previous_searches(conversion_type):
    conn = sqlite3.connect('searches.db')
    c = conn.cursor()
    c.execute("SELECT input, output FROM searches WHERE type = ? ORDER BY id DESC LIMIT 10", (conversion_type,))
    searches = [{'input': row[0], 'output': row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify({'searches': searches})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)