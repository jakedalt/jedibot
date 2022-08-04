import psycopg2
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

def getConnFromUrl():
    load_dotenv()
    DATABASE_URL = os.getenv('DATABASE_URL')
    result = urlparse(DATABASE_URL)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port
    return psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname,
        port=port,
        sslmode='require'
    )

async def vcJoin(discord_id):
    load_dotenv()
    SCHEMA = os.getenv('SCHEMA')
    TABLE = os.getenv('TABLE')

    conn = getConnFromUrl()

    cursor = conn.cursor()

    cursor.execute('SET SCHEMA \'' + SCHEMA + '\'')

    cursor.execute('SELECT * from ' + TABLE + ' WHERE id=' + str(discord_id))

    result = cursor.fetchone();

    if result is None:
        cursor.execute('INSERT INTO ' + TABLE + '(id) VALUES (' + str(discord_id) + ')')

    conn.commit()

    cursor.execute('UPDATE ' + TABLE + ' SET vc_joins = vc_joins + 1 WHERE id =' + str(discord_id))

    conn.commit()

    conn.close()

    return result

async def messageReceived(discord_id):
    load_dotenv()
    SCHEMA = os.getenv('SCHEMA')
    TABLE = os.getenv('TABLE')

    conn = conn = getConnFromUrl()

    cursor = conn.cursor()

    cursor.execute('SET SCHEMA \'' + SCHEMA + '\'')

    cursor.execute('''SELECT * from test
    WHERE id=''' + str(discord_id))

    result = cursor.fetchone();

    if result is None:
        cursor.execute('INSERT INTO ' + TABLE + '(id) VALUES (' + str(discord_id) + ')')

    conn.commit()

    cursor.execute('UPDATE ' + TABLE + ' SET messages_sent = messages_sent + 1 WHERE id =' + str(discord_id))

    conn.commit()

    conn.close()

    return result

def getUserStats(discord_id):
    load_dotenv()
    SCHEMA = os.getenv('SCHEMA')
    TABLE = os.getenv('TABLE')

    conn = getConnFromUrl()

    cursor = conn.cursor()

    cursor.execute('SET SCHEMA \'' + SCHEMA + '\'')

    cursor.execute('SELECT messages_sent, vc_joins from ' + TABLE + ' WHERE id=' + str(discord_id))

    result = cursor.fetchone()

    conn.close()

    return result