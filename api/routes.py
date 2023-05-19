from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import requests


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = self.path
        print(f"url is: {url}")
        url_components = parse.urlsplit(url)
        print(f"url_list is: {url_components}")
        query_string_list = parse.parse_qsl(url_components.query)
        print(f"query string list is: {query_string_list}")
        dictionary = dict(query_string_list)
        
        country = dictionary.get('country')
        country_url = f"https://restcountries.com/v3.1/name/{country}"

        capital = dictionary.get('capital')
        capital_url = f"https://restcountries.com/v3.1/capital/{capital}"

        if country:
            req = requests.get(country_url)
            data = req.json()
            cap_name = data[0]['capital'][0]
            message = f"The capital of {country} is {cap_name}"
        elif capital:
            req = requests.get(capital_url)
            data = req.json()
            coun_name = data[0]['name']['common']
            message = f"{capital} is the capital of {coun_name}"
        else:
            message = 'Sorry, the country or capital you have entered is not valid'

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode())


if __name__ == '__main__':
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, handler)
    print(f'Starting httpd server on {server_address[0]}:{server_address[1]}')
    httpd.serve_forever()

