import sys
sys.path.append('C:\\Users\\HP\\Desktop\\Python_AI\\Timeline_Generator')
import sqlite3


class DAOOperations:
    def __init__(self):
        try:
            self.connect_ = sqlite3.connect('C:\\Users\\HP\\Desktop\\Python_AI\\Timeline_Generator\\app\\resources\\timeline-data.db')
        except:
            self.connect_ = sqlite3.connect('C:\\Users\\HP\\Desktop\\Python_AI\\Timeline_Generator\\app\\resources\\timeline-data.db')
        self.cursor_ = self.connect_.cursor()

    def create_table(self):
        self.cursor_.execute("""


            CREATE TABLE Landslide (
                Title text, 
                Paragraph text, 
                Type text, 
                Location text, 
                Casualty_Injury text, 
                Severity_Label text,
                Summary text,
                CronJobDate text,
                PublicationDate text
            )
            """)
        self.connect_.commit()

    def clean_table(self):
        self.cursor_.execute("""
        DROP TABLE Landslide
        """)
        self.connect_.commit()

    def query_all(self, text_keyword, text_location=None):
        if text_location:
            self.cursor_.execute(f'''

                    SELECT * FROM Landslide WHERE (Type LIKE '{text_keyword}' AND Location LIKE '{text_location}')

                ''')

            items = self.cursor_.fetchall()
            return items
        else:
            self.cursor_.execute(f'''

                    SELECT * FROM Landslide WHERE (Type LIKE '{text_keyword}')

            ''')

            items = self.cursor_.fetchall()
            return items

    def insert(self, title, content, type_, location, casualty_injured, severity_label, text_summary, cron_job_date_, date_):
        set_ = (title.lower(), content.lower(), type_.lower(), ",".join(location).lower(), casualty_injured,
                severity_label[0].lower(), text_summary, cron_job_date_, date_)
        self.cursor_.execute("INSERT INTO Landslide values(?, ?, ?, ?, ?, ?, ?, ?, ?)", set_)
        self.connect_.commit()


if __name__ == '__main__':
    obj = DAOOperations()
    # obj.clean_table()
    # obj.create_table()
    res = obj.query_all('landslide', 'India')
    print(res)
    obj.connect_.close()