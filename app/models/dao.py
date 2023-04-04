import sqlite3


class DAOOperations:
    def __init__(self):
        self.connect_ = sqlite3.connect('timeline-data.db')
        self.cursor_ = self.connect_.cursor()

    def __del__(self):
        self.connect_.close()

    def query_all(self, text_keyword, text_location):
        self.cursor_.execute(f'''

                SELECT * FROM Landslide WHERE (Type LIKE '{text_keyword}' AND Location LIKE '{text_location}') OR (Type LIKE '{text_keyword}')

            ''')

        items = self.cursor_.fetchall()
        return items
