import re
import sqlite3


connect_=sqlite3.connect('timeline-data.db')

cursor_=connect_.cursor()

cursor_.execute("""

        SELECT Title FROM DISASTER

"""
)

items = cursor_.fetchall()

# for number, item in enumerate(items):
#     print("News Item ", number+1)
#     print(item[0])
#     print("\n")

for index, item in enumerate(items):
    print("News Item Number: ", index+1)
    temp=re.compile(r'dead|Death|death|Dead|killed|Killed|buries|Buries').search(item[0])
    if not temp:
        # print("Casualty not found")
        temp_2=re.compile(r'injured|Injured|hit|Hit|hits|Hits|trapped|Trapped|feared|Feared|threat|Threat').search(item[0])
        if not temp_2:
            print("Casualty not found")
        else:
            print(temp_2)
            temp_3=re.compile(r'/d').search(item[0])
            if not temp_3:
                print("Couldn't detect count of injured.")

            else:
                print(temp_3)
                print("Injuries: ", temp_3.group())
                # to recheck and improvise
        print("\n\n")


    else:
        # print(temp.group())
        print(temp)
        temp_1=re.compile(r'\d').search(item[0])
        if not temp_1:
            print("Couldn't detect count of casualities.")

        else:
            print(temp_1)
            print("Casualties: ", temp_1.group())
        print("\n\n")

    

connect_.commit()
connect_.close()

