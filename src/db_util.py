import psycopg2

from urllib.parse import urlparse
from constants import DATABASE_URL, SCHEMA, TABLE


def get_conn_from_url():
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


async def vc_join(discord_id, username):
    conn = get_conn_from_url()

    cursor = conn.cursor()

    cursor.execute('SET SCHEMA \'' + SCHEMA + '\'')

    cursor.execute('SELECT * from ' + TABLE + ' WHERE id=' + str(discord_id))

    result = cursor.fetchone()

    if result is None:
        cursor.execute('INSERT INTO ' +
                       TABLE + '(id, username) VALUES (' + str(discord_id) + ', \'' + str(username) + '\');')

    conn.commit()

    cursor.execute('UPDATE ' + TABLE + ' SET vc_joins = vc_joins + 1 WHERE id =' + str(discord_id))

    conn.commit()

    conn.close()

    return result


async def message_received(discord_id, username):
    conn = get_conn_from_url()

    cursor = conn.cursor()

    cursor.execute('SET SCHEMA \'' + SCHEMA + '\'')

    cursor.execute('''SELECT * from ''' + TABLE + ''' WHERE id=''' + str(discord_id))

    result = cursor.fetchone()

    if result is None:
        cursor.execute('INSERT INTO ' +
                       TABLE + '(id, username) VALUES (' + str(discord_id) + ', \'' + str(username) + '\');')

    conn.commit()

    cursor.execute('UPDATE ' + TABLE + ' SET messages_sent = messages_sent + 1 WHERE id =' + str(discord_id))

    conn.commit()

    conn.close()

    return result


def get_user_stats(discord_id):
    conn = get_conn_from_url()

    cursor = conn.cursor()

    cursor.execute('SET SCHEMA \'' + SCHEMA + '\'')

    cursor.execute('SELECT messages_sent, vc_joins from ' + TABLE + ' WHERE id=' + str(discord_id))

    result = cursor.fetchone()

    conn.close()

    return result
