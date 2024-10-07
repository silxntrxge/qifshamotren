from flask import Flask, request, jsonify
from scraper import scrape_emails

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    names = data.get('names', '')
    domain = data.get('domain', 'gmail.com')
    niche = data.get('niche', '')
    webhook_url = data.get('webhook')
    
    emails = scrape_emails(names, domain, niche, webhook_url)
    
    return jsonify({'emails': emails})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)