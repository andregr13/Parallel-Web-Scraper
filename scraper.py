import requests
from bs4 import BeautifulSoup

def scrape_wikipedia_references(url):
    try:
        response = requests.get(url) 

        if response.status_code == 200: #200 = successful 
            
            soup = BeautifulSoup(response.text, 'html.parser')
            references_section = soup.find('ol', class_='references') # Find the ordered references section 

            if references_section:
                references = []

                # Extract all the references
                for reference in references_section.find_all('li'):
                    ref_text = reference.get_text()
                    references.append(ref_text.strip())  
                return references
            
            else:
                return "References not found."
            
        else:
            return f"Failed to retrieve content, status code: {response.status_code}"
        
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Testing
url = 'https://en.wikipedia.org/wiki/Web_scraping'
references = scrape_wikipedia_references(url)
for i, ref in enumerate(references, start=1):
    print(f"Reference {i}: {ref}")
