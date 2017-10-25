import util
import sqlite3
import os


def map_md_row_to_dict(game_md_row):
    return {
        'name': game_md_row[1],
        'appid': game_md_row[2],
        'image': game_md_row[3],
        'platforms': game_md_row[4].split(':'),
        'genres': game_md_row[5].split(':'),
        'tags': game_md_row[6].split(':'),
        'global_owners': game_md_row[7],
        'developer': game_md_row[8],
        'publisher': game_md_row[9],
        'store_page': util.derive_store_page_from_appid(game_md_row[2]),
        'price': game_md_row[10],
        'multiplayer': bool(game_md_row[11]),
    }

def map_user_md_row_to_dict(user_md_row):
    return {
        'steamid': user_md_row[1],
        'avatar': user_md_row[2],
        'username': user_md_row[3],
        'profile_url': user_md_row[4],
        'name': user_md_row[5]
    }

def get_cached_md_for_games(steamGame_ids,sql_db_file):
    games_not_found_in_db = { str(appid): True for appid in steamGame_ids }
    
    missing = []
    metadata = {}
    
    if not os.path.isfile(sql_db_file):
        createDB(sql_db_file)
        missing = steamGame_ids
        return metadata, missing
    
    conn = sqlite3.connect(sql_db_file)
    cur = conn.cursor()

    select_q = "SELECT * FROM Game WHERE appid IN ({arg_seq})"

    arg_seq = ', '.join(['?'] * len(steamGame_ids)) # '?, ?, ?, ...'

    select_q = select_q.format(arg_seq=arg_seq)
    # "SELECT * FROM Game WHERE appid in (?, ?, ?, ...)"

    rows = cur.execute(select_q, tuple(map(str, steamGame_ids)))

    game_datas = []

    for row in rows.fetchall():
        game_data = map_md_row_to_dict(row)
        game_datas.append(game_data)
        if str(game_data['appid']) in games_not_found_in_db:
            del games_not_found_in_db[str(game_data['appid'])]

    conn.close()

    return game_datas, list(games_not_found_in_db.keys())

def get_cached_md_for_users(steamIds, sql_db_file):
    if not os.path.isfile(sql_db_file):
        createDB(sql_db_file)
        return [], steamIds

    users_not_found_in_db = { str(steamid): True for steamid in steamIds }

    conn = sqlite3.connect(sql_db_file)
    cur = conn.cursor()

    select_q = "SELECT * FROM Users WHERE steamid IN ({arg_seq})"

    arg_seq = ', '.join(['?'] * len(steamIds)) # '?, ?, ?, ...'

    select_q = select_q.format(arg_seq=arg_seq)
    # "SELECT * FROM Users WHERE steamid in (?, ?, ?, ...)"

    rows = cur.execute(select_q, tuple(map(str, steamIds)))

    user_summaries = []

    for row in rows.fetchall():
        user_summary = map_user_md_row_to_dict(row)
        user_summaries.append(user_summary)
        if str(user_summary['steamid']) in users_not_found_in_db:
            del users_not_found_in_db[str(str(user_summary['steamid']))]

    conn.close()
    return user_summaries, list(users_not_found_in_db.keys())

def storeGameDatas(game_metaDatas, sql_db_file):
    if not os.path.isfile(sql_db_file):
        createDB(sql_db_file)
    conn = sqlite3.connect(sql_db_file)
    cur = conn.cursor()
    for game in game_metaDatas:
        #  if not game.get('price'):
            #  continue
        storeGameData(game,cur)
    conn.commit()
    conn.close()

def storeUserDatas(userDatas, sql_db_file):
    if not os.path.isfile(sql_db_file):
        createDB(sql_db_file)
    conn = sqlite3.connect(sql_db_file)
    cur = conn.cursor()
    for user in userDatas:
        storeUserData(user,cur)
    conn.commit()
    conn.close()

    
def storeGameData(game_metaData,cur):
    
    cur.execute("""
    Insert into Game(name,appid,image,platforms,genres,tags,global_owners,developer,publisher,price,multiplayer)
    Values(:name,:appid, :image, :platforms, :genres, :tags, :global_owners, :developer, :publisher, :price, :multiplayer)
    """, {
            'name': game_metaData["name"],
            'appid': game_metaData["appid"],
            'image': game_metaData["image"],
            'platforms': ':'.join(game_metaData["platforms"]),
            'genres': ':'.join(game_metaData['genres']),
            'tags': ':'.join(game_metaData["tags"]),
            'global_owners': game_metaData["global_owners"],
            'developer': game_metaData["developer"],
            'publisher': game_metaData["publisher"],
            'price': game_metaData["price"],
            'multiplayer': str(int(game_metaData["multiplayer"])),
        })

def storeUserData(user_metaData,cur):
    
    cur.execute("""
    Insert into Users(steamid,avatar,username,profile_url,name)
    Values(:steamid,:avatar,:username,:profile_url,:name)
    """,{
            'steamid': user_metaData["steamid"],
            'avatar': user_metaData["avatar"],
            'username': user_metaData["username"],
            'profile_url': user_metaData["profile_url"],
            'name' : user_metaData["name"],
        })

def createDB(sql_db_file):
    conn = sqlite3.connect(sql_db_file)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE `Game` (
	id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	name	TEXT,
	appid	INTEGER UNIQUE,
	image	TEXT,
	platforms  TEXT,
        genres TEXT,
	tags	TEXT,
	global_owners	INTEGER,
	developer TEXT,
	publisher TEXT,
	price INTEGER,
        multiplayer INTEGER
)""")

    cur.execute("""CREATE TABLE `Users` (
	`Id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`steamid`	INTEGER,
	`avatar`	TEXT,
	`username`	TEXT,
	`profile_url`	TEXT,
	`name`          TEXT
)""")
    conn.close()


    
