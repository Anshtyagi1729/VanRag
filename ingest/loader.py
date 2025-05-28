import requests
from bs4 import BeautifulSoup
import PyPDF2
class documentLoader:
    @staticmethod
    def load_webpage(url, output_file):
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch page: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.find('body')
        if not body:
            print("Could not find body tag")
            return
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for tag in body.find_all(['h1', 'h2', 'h3', 'p', 'li', 'pre', 'code']):
                text = tag.get_text(separator=' ', strip=True)
                if text:
                    f.write(text + '\n\n')  
        
        print(f"Successfully saved to {output_file}")

