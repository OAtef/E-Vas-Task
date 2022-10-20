from Server import app
from flask import (request, jsonify)

from Server.Service.OLX_Service import (get_all_posts)
from Server.Service.Scraper_service import scrape_data


@app.route('/scrape_olx', methods=['POST'])
def scrape_olx():
    data = request.get_json()
    return jsonify(scrape_data(data.get('key_word'), data.get('email'), data.get('items_in_mail')))



@app.route('/', methods=['GET'])
def query_records():
    return jsonify(get_all_posts())


if __name__ == "__main__":
    app.run(debug=True)
