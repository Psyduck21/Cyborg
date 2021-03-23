import sqlite3
db_path = "./data/db/bot_database.sqlite"
db = sqlite3.connect(db_path)
cursor = db.cursor()
cursor.execute("SELECT level FROM users WHERE user_id = 800286958348795935 and guild_id = 740418138075693107")
result = cursor.fetchone()
lvl = result[0]

#lvl = [i[0] for i in result]
print(lvl)
if lvl ==1:
    print("working")
else:
    print("You are noob.")

