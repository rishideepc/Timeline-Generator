import time
from ui_ux.views import my_form_post
from websites.generic.ndtv import *
from websites.sports.cricketaddic import *
from ui_ux import create_app
# from ui_ux.views import *
from flask import request

app=create_app()
# app.app_context().push()



# if request.method == 'POST':
#     word=request.form['keyword']


# keyword="cricket"
# site='https://www.hindustantimes.com/'f'{keyword}'''

# keyword=['cricket', 'football', 'basketball']
# websites = ['https://cricketaddictor.com/', 'https://www.ndtv.com/search?searchtext='f'{keyword}''' ]


##################################################################################################

# def find_event(keyword):
#     html_text=requests.get('https://www.ndtv.com/search?searchtext='f'{keyword}''')
#     soup=BeautifulSoup(html_text.content, 'lxml')
#     pieces= soup.find_all('div', class_="src_lst-rhs")
#     # i=0
#     for index, piece in enumerate(pieces):
#         text_what= piece.find('div', class_="src_itm-txt").text
#         who_when_= piece.find('span', class_="src_itm-stx").text
#         # if piece[index].text_what!=piece[index+1].text_what:
#         print(f'{index+1}.', text_what.strip())
#         print(f'Date: {who_when_.strip()}', "\n")
#             # i=i+1


##################################################################################################


    # i=0
    # for index, text_what in enumerate(text_whats):
    #     text_what=text_what.text
    #     if text_what[index]!=text_what[index+1]:
    #         print(f'{i+1}.', text_what.strip(), "\n")
    #         i=i+1
    # for page in pages:
    #     title= page.find('a').text
    #     tagline=page.h3
    #     if tagline!=None:
    #         text_y=tagline.a.text
    #         print(text_y, "\n")

        # else:
        #     exit()

if __name__=="__main__":

    app.run(debug=True)
    
    
    # wrd=word
    #                             # keyword=input("Enter the keyword: ")
    # if word=='cricket-sport':
    #     find_event_cric()
    #                             # # while True:
    # else:
    #     find_event(keyword=word)    
                                # time_wait=10
                                # time.sleep(time_wait)