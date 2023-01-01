import re
import sqlite3

def casualty_count(text_keyword, text_location):

    connect_=sqlite3.connect('timeline-data.db')

    cursor_=connect_.cursor()

    cursor_.execute(f"""

            SELECT * FROM Disaster WHERE Type LIKE '{text_keyword}' AND Location LIKE '{text_location}'

    """
    )

    items = cursor_.fetchall()

    # for number, item in enumerate(items):
    #     print("News Item ", number+1)
    #     print(item[0])
    #     print("\n")

    for index, item in enumerate(items):
        # print("News Item Number: ", index+1)
        temp=re.compile(r'dead|Death|death|Dead|killed|Killed|buries|Buries').search(item[0])
        if not temp:
            # print("Casualty not found")
            temp_2=re.compile(r'injured|Injured|hit|Hit|hits|Hits|trapped|Trapped|feared|Feared|threat|Threat').search(item[0])
            if not temp_2:
                return "Casualty not found"
            else:
                # print(temp_2)
                temp_3=re.compile(r'/d').search(item[0])
                if not temp_3:
                    return "Casualty found - Couldn't detect count of injured."

                else:
                    # print(temp_3)
                    return f"Injuries: {temp_3.group()}" 
                    # to recheck and improvise
            # print("\n\n")


        else:
            # print(temp.group())
            # print(temp)
            temp_1=re.compile(r'\d').search(item[0])
            if not temp_1:
                return "Casualty Found - Couldn't detect count of casualities."

            else:
                # print(temp_1)
                return f"Casualties: {temp_1.group()}"
            # print("\n\n")

        

    connect_.commit()
    connect_.close()

if __name__=="__main__":
    print(casualty_count("landslide", "India"))
