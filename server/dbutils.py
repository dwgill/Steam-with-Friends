import sqlite3

def get_cached_md_for_games(steamGame_ids,sql_db_file):
    conn = sqlite3.connect(sql_db_file)
    cur = conn.cursor()
    missed = []
    metadata = {}
    for id in steamGame_ids:
        row = cur.execute("Select * from Game where gameId=" + id)
        if len(row) == 0:
            missed.append(id)
        else:
            metadata[id] = row[0]

    return metadata,missing
