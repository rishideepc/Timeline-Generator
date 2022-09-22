import sqlite3

connect_=sqlite3.connect('timeline-data.db')
keyword='India'
cursor_=connect_.cursor()

cursor_.execute(f'''

SELECT * FROM Disaster WHERE location LIKE '{keyword}'

''')

# print(cursor_.fetchall())
items = cursor_.fetchall()
for item in items:
    print(f'''
    Title: {item[0]}
    DateTime: {item[1]}
    Type: {item[2]}
    Location: {item[3]}
    CronJobDate: {item[4]}
    ''')

connect_.commit()
connect_.close()