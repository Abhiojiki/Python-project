from datetime import date
import SQL_db

moods = ["Happy", "Sad", "Stressed", "Frustrated", "Angry", "Excited", "Content", "Confused", 
         "Tired", "Meh","Chill",
         "chill","Hungry","Fear","anxious"]

# getting the information for the database from the users


# pulls the date automatically in the correct format
date = date.today()
time= date.today().strftime("%I:%M %p")

# gets user input for their mood
# limit the moods to preset moods atm
print(f"Are you {', '.join(moods).lower()}")
while True:
    # makes sure that the input matches the case of the moods
    mood = input("What is your mood today? ").capitalize()
    # checks to make sure that it is a valid choice
    if mood in moods:
        break

# # gets user input for the reason for their mood
journal = input(f"Why do you feel {mood.lower()}? ")

# # pulls the table from SQL_db and runs the methods
database = SQL_db.MoodDatabase()
database.connect_db()
database.createTable()
database.addColumn()
database.insertData(date,time, mood, journal)
# database.clearTable()
database.conversion()
database.summarizeData()
database.close_db()