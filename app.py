from flask import Flask, jsonify, request

from crawler import get_event_urls

app = Flask(__name__)

@app.route('/api/v1.0/crawl', methods=['GET','POST'])
def get_tasks():
    search_url = request.args.get('url', '') or request.form.get('url','')
    urls = get_event_urls(search_url)
    return jsonify({'urls': urls})

if __name__ == '__main__':
    app.run(debug=True)