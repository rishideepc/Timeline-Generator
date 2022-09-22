import sqlite3

connect_=sqlite3.connect('timeline-data.db')

cursor_=connect_.cursor()

cursor_.execute("""


    CREATE TABLE Disaster (
        Title text, 
        DateTime text, 
        Type text, 
        Location text, 
        CronJobDate text

    )

""")


# cursor_.execute("""

#     SELECT * FROM disaster

# """)

# print(cursor_.fetchall())


connect_.commit()
connect_.close()