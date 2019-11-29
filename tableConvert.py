# pipenv run python3 tableConvert.py
import os

from bs4 import BeautifulSoup 
# To install Beautiful Soup: pipenv install bs4
# To install lxml parser: pipenv install lxml

def convert(myfile):
    with open(myfile, mode='r', encoding='utf-8') as f:
        # soup = BeautifulSoup(f, "lxml")    
        soup = BeautifulSoup(f, "html.parser")   
        for table in soup.find_all(attrs={"class": "api-layout-table"}):
            div = soup.new_tag('div')
            for th in table.find_all('th'):
                if len(th.find_parents("table")) == 1:  #Ignore nested tables
                    h4 = soup.new_tag('h4')
                    for item in th.find_all(attrs={"class": "api-label"}):
                        for string in item.stripped_strings:
                            h4.append(string)
                            div.append(h4)
                            p = soup.new_tag('p')
                            for sibling in th.next_siblings:
                                if sibling.name == "td":
                                    p.contents = sibling.contents
                                    div.append(p)
            table.replace_with(div)
        # print(soup.prettify())
        # In text mode, the default when reading is to convert platform-specific line endings (\n on Unix, \r\n on Windows) to
        # just \n. When writing in text mode, the default is to convert occurrences of \n back to platform-specific line endings.
        with open('out.htm', mode='w', encoding='utf-8') as out:
            # out.write(soup.prettify())
            out.write(str(soup))

def main():
    convert('rest_api_ref.htm')

if __name__ == '__main__':
    main()