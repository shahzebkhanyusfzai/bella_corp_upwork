import requests
from lxml import html
import csv

def get_category_links(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)
    # Xpath to extract category links
    category_links = tree.xpath('//a[@class="dynamic-collection-list--item-link"]/@href')
    return category_links

def get_product_details(category_url):
    response = requests.get(category_url)
    tree = html.fromstring(response.content)
    # Xpath to extract product names and links
    product_names = tree.xpath('//h2[@class="productitem--title"]/a/text()')
    product_links = tree.xpath('//h2[@class="productitem--title"]/a/@href')
    return list(zip(product_names, product_links))

def main():
    url = "https://bellacorp.com.au/"
    category_links = get_category_links(url)
    all_products = []
    
    for category_link in category_links:
        # Check if the link is complete or not
        if not category_link.startswith("http"):
            category_link = url + category_link
        products = get_product_details(category_link)
        all_products.extend(products)
    
    # Saving to CSV
    with open('products.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Link'])  # Writing headers
        for product in all_products:
            writer.writerow([product[0], product[1]])

    print("Data has been written to products.csv")

if __name__ == "__main__":
    main()
