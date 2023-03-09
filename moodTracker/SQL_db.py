import sqlite3
import numpy as np
import pandas as pd
import plotly.express as px

import matplotlib.pyplot as plt
class MoodDatabase:
 # keep track of daily moods along with allow user to input
    def connect_db(self):
        self.conn_db = sqlite3.connect("moodtracker.db")
        self.db = self.conn_db.cursor()

    def createTable(self):
        self.db.execute("""CREATE TABLE IF NOT EXISTS mood_tracker
                (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Date DATETIME,  Mood TEXT, Journal TEXT)""")
    
    def addColumn(self):
        self.db.execute("""ALTER TABLE mood_tracker ADD Time TIME""")

    def insertData(self, date, time, mood, journal):
        sql = f"""INSERT INTO mood_tracker(Date, Time, Mood, Journal)
                    VALUES (?, ?, ?, ?)"""
        self.db.execute(sql, [date, time, mood, journal])

    def clearTable(self):
        self.db.execute("DELETE FROM mood_tracker")

    def close_db(self):
        self.conn_db.commit()
        self.conn_db.close()

    def conversion(self):
        self.df = pd.read_sql_query("SELECT * from mood_tracker", self.conn_db)
        self.tocsv= self.df.to_csv('output.csv',index=False)

    
    def summarizeData(self):


        # create a pie chart of moods by date
        color = plt.cm.RdBu(np.linspace(0, 1, 20))
        query = '''
        SELECT Mood, COUNT(Date) as num_dates
        FROM mood_tracker
        GROUP BY Mood
        ORDER BY num_dates DESC
        LIMIT 20
        '''
        results = pd.read_sql_query(query, self.conn_db)
        results.plot.pie(y='num_dates', labels=results['Mood'], colors=color, autopct='%0.1f%%')
        plt.title('Moods by date')
        plt.axis('off')
        plt.show()

        # create a bar chart of the top 15 moods
        query = '''
        SELECT Mood, COUNT(Date) as num_dates
        FROM mood_tracker
        GROUP BY Mood
        ORDER BY num_dates DESC
        LIMIT 15
        '''
        results = pd.read_sql_query(query, self.conn_db)
        results.plot.barh(x='Mood', y='num_dates', color='blue', title='User\'s Moods')
        plt.show()


        time_query = '''SELECT time, mood FROM mood_tracker'''
        df_time = pd.read_sql_query(time_query, self.conn_db)
        fig_time = px.bar(df_time, x='Time', y='Mood', color_discrete_sequence=['#2B3A67'], title='Mood by Time')
        fig_time.show()

        # Query data for bar plot by date
        date_query = '''SELECT date, mood FROM mood_tracker'''
        df_date = pd.read_sql_query(date_query, self.conn_db)
        fig_date = px.bar(df_date, x='Date', y='Mood', color_discrete_sequence=['crimson'], title='Daily Mood')
        fig_date.show()

            
                