from bs4 import BeautifulSoup
import requests

def find_event_cric():
    html_text=requests.get('https://www.cricketaddictor.com')
    soup=BeautifulSoup(html_text.content, 'lxml')

    pages= soup.find_all('div', class_="entry-wrapper")
    for index, page in enumerate(pages):
        title= page.find('a').text
        tagline=page.h3
        if tagline!=None:
            text_y=tagline.a.text.strip()
            with open(f'cricket_information/new_cric_info_{index+1}.txt', 'w') as f:
                f.write(f'{index}. {title.strip()}\n')
                # f.write(text_y, "\n")
                f.write(f'Info: {text_y}\n')

                f.write(f'\n\nFile Saved: New Cricket Info')
    