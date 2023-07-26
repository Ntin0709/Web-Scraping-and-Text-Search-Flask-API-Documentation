from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from langchain.document_loaders import WebBaseLoader
import nest_asyncio
nest_asyncio.apply()

app = Flask(__name__)
scraped_data = []  # Store the scraped data in a list

def load_site_map(base_url):
    response = requests.get(base_url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'lxml')

    urls = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None:
            if href.startswith('http'):
                urls.append(href)
            else:
                urls.append(base_url + href)

    return urls

def extracting_data(urls):
    loader = WebBaseLoader(urls)
    loader.requests_kwargs = {'verify': False}
    loader.requests_per_second = 1
    docs = loader.aload()
    return docs

@app.route('/load_and_extract_data', methods=['POST'])
def load_and_extract_data():
    try:
        data = request.get_json()
        base_url = data.get('base_url')

        urls = load_site_map(base_url)
        global scraped_data  # Use the global variable to store the scraped data
        scraped_data = extracting_data(urls)

        return jsonify({"message": "Data loaded and extracted successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search_text', methods=['POST'])
def search_text():
    try:
        data = request.get_json()
        search_text = data.get('search_text')

        found_pages = []
        for doc in scraped_data:
            if search_text.lower() in doc.page_content.lower():
                found_pages.append(doc.metadata.get('source'))

        return jsonify(found_pages), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)