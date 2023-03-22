import sqlite3

connect_=sqlite3.connect('timeline-data.db')

cursor_=connect_.cursor()

# cursor_.execute("""


#     CREATE TABLE Landslide (
#         Title text, 
#         Paragraph text, 
#         Type text, 
#         Location text, 
#         Casualty_Injury text, 
#         Severity_Label text,
#         Summary text,
#         CronJobDate text
#     )


# """)

# cursor_.execute("""

#     DROP TABLE Landslide;

# """)


cursor_.execute("""

    SELECT * FROM Landslide

""")

print(cursor_.fetchall())


connect_.commit()
connect_.close()


    