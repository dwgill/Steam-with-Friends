import sqlite3
import os

def get_cached_md_for_games(steamGame_ids,sql_db_file):
    
    missing = []
    metadata = {}


    if not os.path.isfile(sql_db_file):
        createDB(sql_db_file)
        missing = steamGame_ids
        return metadata, missing
    
    conn = sqlite3.connect(sql_db_file)
    cur = conn.cursor()
    
    for id in steamGame_ids:
        row = cur.execute("Select * from Game where gameId=" + str(id))
        record = row.fetchone()
        if record == None:
            missing.append(id)
        else:
            metadata[id] = record
    return metadata,missing

def get_cached_md_for_users(steamIds,sql_db_file):
    missing = []
    metadata = {}

    if not os.path.isfile(sql_db_file):
        createDB(sql_db_file)
        missing = steamGame_ids
        return metadata, missing
    
    conn = sqlite3.connect(sql_db_file)
    cur = conn.cursor()
    
    for id in steamIds:
        row = cur.execute("Select * from Users where SteamId=" + str(id))
        record = row.fetchone()
        if record == None:
            missing.append(id)
        else:
            gamesList = []

            rows = cur.execute("Select gameId from GameToUsers where userId=" +str(record[0]))
            for val in rows.fetchall():
                row = cur.execute("Select gameId from Game where id =" + str(val[0]))
                record = row.fetchone()
                gamesList.append(record[0])

            record = (record,gamesList)
            metadata[id] = record
    return metadata,missing




def createDB(sql_db_file):
    conn = sqlite3.connect(sql_db_file)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE `Game` (
	id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	name	TEXT,
	pictures	TEXT,
	genre	TEXT,
	urlToStore	TEXT,
	gameType	TEXT,
	gameId	INTEGER)""")

    cur.execute("""CREATE TABLE `GameToUsers` (
	`Id`	INTEGER NOT NULL,
	`gameId`	INTEGER,
	`userId`	INTEGER,
	FOREIGN KEY(`gameId`) REFERENCES `Game`(`id`),
	PRIMARY KEY(`Id`),
	FOREIGN KEY(`userId`) REFERENCES `Users`(`Id`)
)""")

    cur.execute("""CREATE TABLE `Users` (
	`Id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`Name`	TEXT,
	`SteamId`	INTEGER,
	`AvatarUrl`	TEXT,
	`ProfileUrl`	TEXT
)""")


    
