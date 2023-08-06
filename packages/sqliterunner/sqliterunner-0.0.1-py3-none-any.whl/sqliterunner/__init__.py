from sqlite3 import connect


def make_sql_query(dbfile, query, commit=True, fetch=False):
    dbconn = connect(dbfile)
    queryres = dbconn.execute(query)
    if commit and fetch:
        raise Exception("You can not commit & fetch an sql query.")
    if commit:
        dbconn.commit()
        dbconn.close()
        return True
    if fetch == 'all':
        queryres = queryres.fetchall()
        dbconn.close()
    if fetch == 'one':
        queryres = queryres.fetchone()
        dbconn.close()
    return queryres
