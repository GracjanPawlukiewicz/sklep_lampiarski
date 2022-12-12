import requests
from bs4 import BeautifulSoup
import json
import glob

def get_links(page_link) -> list:
    """
    Method used to get links of product in store
    
    Args:
        page_link (str): Url of category
        
    Returns:
        product_links (list): Urls of every product in shop
    """
    k = requests.get(page_link).text
    bs = BeautifulSoup(k, 'html.parser')
    num = bs.find("a", {"title":"ostatnia strona"}).get("data-pagination")
    
    product_links = []    
    for page in range(1, int(num) + 1):  
        url = f'{page_link}/lp/{page}'
        k = requests.get(url).text

        bs = BeautifulSoup(k,'html.parser')
        productlist = bs.find_all("div", {"class":"product-list-item"})
        
        for product in productlist:
            link = product.find("a", {"class":"product-content-container"}).get("href") 
            product_links.append(link)
            
    return product_links


def get_data(products_links: list, headers: dict) -> list:
    """
    Method used to get data of products in store

    Args:
        products_links (list): Urls of every product in shop
        headers (dict): user-agent data

    Returns:
       data (list): Data of store all products in dictionaries
       
    """
    data=[]
    for category in products_links:
        print(category)
        for link in products_links[category]:
            f = requests.get(link,headers=headers).text
            bs = BeautifulSoup(f,'html.parser')
            
            try:
                name = bs.find("h1", {"class":"product-title"}).text.replace('\n',"")
            except:
                name = None


            try:
                price = bs.find("strong", {"class":"produkt-cena"}).text.replace('\n',"").strip()
            except:
                price = None
                
                
            try:
                short_about = bs.find("div", {"class":"product-short-description"}).text.replace('\n',"")
            except:
                short_about=None
                
                
            try:
                selection = []
                selector_description = bs.find("label", {"class":"col-sm-4"}).text.replace('\n',"")
                
                selector = bs.find("select", {"class":"custom-select"}).find_all('option')
                for sel in selector:
                    selection.append(sel.text.strip())
            except:
                selector_description = None
                selection = None
                
                
            try:
                description = bs.find("div", {"class":"col-sm-9"}).text
            except:
                description = None
                
                
            try:  
                attributes_table = bs.find("table", {"class":"table"})
                attributes = {}
                for row in attributes_table.findAll('tr'):
                    key = row.find('th').text
                    value = row.find('td').text
                    attributes[key] = value        
            except:
                attributes=None
                
                
            try:
                img = bs.find("a", {"class":"fotka"}).get("href")
            except:
                img = None
                
            lamp = {"category": category,
                    "name": name,
                    "price": price,
                    "short_about": short_about,
                    "selector_description": selector_description,
                    "selection": selection,
                    "description": description,
                    "attributes": attributes,
                    "img": img
                    }
            
            data.append(lamp)
    return data

def retrieve_links() -> dict:
    """Method used to retrieve links of products

    Returns:
        _type_: _description_
    """
    for file in glob.glob("./products_data/*.json"):
        print(file)
        with open(file, 'r', encoding="UTF-8") as infile:
            data = json.load(infile)
    return data
 
def save_links():
    """
    Method used to save links of all shop categories
    Links are saved in JSON file with categories as keys
    """
    categories = ['https://www.skleplampy.pl/kategoria/tasmy-led-291',
                  'https://www.skleplampy.pl/kategoria/lampy-wiszace-i-zyrandole-273',
                  'https://www.skleplampy.pl/kategoria/kinkiety-274',
                  'https://www.skleplampy.pl/kategoria/lampy-sufitowe-i-plafony-275'
                  'https://www.skleplampy.pl/kategoria/lampy-stojace-276',
                  'https://www.skleplampy.pl/kategoria/oprawy-wpuszczane-277',
                  'https://www.skleplampy.pl/kategoria/listwy-reflektory-spoty-278'
                  'https://www.skleplampy.pl/kategoria/lampy-zewnetrzne-wiszace-279',
                  'https://www.skleplampy.pl/kategoria/plafony-zewnetrzne-280',
                  'https://www.skleplampy.pl/kategoria/lampy-ogrodowe-stojace-281',
                  'https://www.skleplampy.pl/kategoria/oprawy-najazdowe-285',
                  'https://www.skleplampy.pl/kategoria/zarowki-286',
                  'https://www.skleplampy.pl/kategoria/wentylatory-287',
                ]
    links = {}
    for link in categories:
        category_name = ''.join([i for i in link.split('/')[-1] if not i.isdigit()])
        links[category_name[:-1]] = get_links(page_link=link)
            
    with open("./products_data/links.json", 'w', encoding="UTF-8") as outfile:
        json.dump(links, outfile, ensure_ascii=False, indent=4)
        
if __name__ == '__main__':
    base_url = "https://www.skleplampy.pl/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    
    # save_links()
    products_links = retrieve_links()
    
    data = get_data(products_links=products_links, headers=headers)
    with open('./products_data/products.json', 'w', encoding="UTF-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
