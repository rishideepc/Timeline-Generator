from bs4 import BeautifulSoup
import requests
import webbrowser
import datetime


# keywords for disaster class
keywords_disaster=['landslide', 'flood', 'earthquake', 'tsunami', 'flash flood']

# keywords for generic superclass
keywords_generic=['politics', 'sports', 'economics', 'disaster']

################################################################################d##########
# cronjob script

def fetch_info_ndtv(keywords):
    len_=len(keywords)
    for i in len_:
        html_text=requests.get('https://www.ndtv.com/search?searchtext='f'{keywords}''')
        # webbrowser.open('https://www.ndtv.com/search?searchtext='f'{keyword}''')
        soup=BeautifulSoup(html_text.content, 'lxml')
        pieces= soup.find_all( 'div', class_="src_lst-rhs")
        # i=0
        for index, piece in enumerate(pieces):
            text_what= piece.find('div', class_="src_itm-txt").text
            who_when_= piece.find('span', class_="src_itm-stx").text
            link_text= piece.find('div', class_="src_itm-ttl")
            link_go= link_text.a['href']
            # if piece.text_what[index]!=piece.text_what[index+1]:
            html_text_2=requests.get(link_go)
            soup_2=BeautifulSoup(html_text_2.content, 'lxml')
            story_content=soup_2.find('div', class_="story__content")

            with open(f'information/new_info_{index+1}.txt', 'w') as f:
                f.write(f'{index+1}. {text_what.strip()}\n')
                f.write(f'Date: {who_when_.strip()}\n')
                if story_content!=None:
                    central_div=story_content.find('div')
                    paragraph= central_div.find('p').text
                    f.write(f'More Info: {paragraph}\n\n\n')

                    f.write(f'\n\nFile Saved: New Info')


        print("\n\nDone iteration.")
                
            # print(f'{index+1}.', text_what.strip())
            # print(f'Date: {who_when_.strip()}', "\n")
            # print(f'Link: {link_go.strip()}', "\n")
            
            # if story_content!=None:
            #     central_div=story_content.find('div')
            #     paragraph= central_div.find('p').text
                # print(f'More Info: {paragraph}', "\n\n\n")



##########################################################################################