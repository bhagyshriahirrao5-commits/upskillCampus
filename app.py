from flask import Flask, request, redirect, render_template_string
import string
import random

app = Flask(__name__)

# In-memory database (dictionary)
url_db = {}

# Function to generate short code
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Home page
@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = None
    
    if request.method == 'POST':
        long_url = request.form['url']
        
        # Generate unique short code
        short_code = generate_short_code()
        while short_code in url_db:
            short_code = generate_short_code()
        
        url_db[short_code] = long_url
        short_url = request.host_url + short_code
    
    return render_template_string('''
        <h2>URL Shortener</h2>
        <form method="POST">
            <input type="text" name="url" placeholder="Enter URL" required>
            <button type="submit">Shorten</button>
        </form>
        {% if short_url %}
            <p>Short URL: <a href="{{ short_url }}">{{ short_url }}</a></p>
        {% endif %}
    ''', short_url=short_url)

# Redirect route
@app.route('/<short_code>')
def redirect_url(short_code):
    long_url = url_db.get(short_code)
    if long_url:
        return redirect(long_url)
    return "Invalid URL"

if __name__ == '__main__':
    app.run(debug=True)