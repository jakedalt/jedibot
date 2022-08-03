import psycopg2
import os
from dotenv import load_dotenv

async def vcJoin(discord_id):
    load_dotenv()
    UN = os.getenv('DB_USERNAME')
    PW = os.getenv('DB_PASSWORD')
    SCHEMA = os.getenv('SCHEMA')
    TABLE = os.getenv('TABLE')

    conn = psycopg2.connect(
        database="d5nlcc5k9d83qo", user=UN, password=PW, host='ec2-3-213-228-206.compute-1.amazonaws.com',
        port='5432'
    )

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
    UN = os.getenv('DB_USERNAME')
    PW = os.getenv('DB_PASSWORD')
    SCHEMA = os.getenv('SCHEMA')
    TABLE = os.getenv('TABLE')

    conn = psycopg2.connect(
        database="d5nlcc5k9d83qo", user=UN, password=PW, host='ec2-3-213-228-206.compute-1.amazonaws.com',
        port='5432'
    )

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
    UN = os.getenv('DB_USERNAME')
    PW = os.getenv('DB_PASSWORD')
    SCHEMA = os.getenv('SCHEMA')
    TABLE = os.getenv('TABLE')

    conn = psycopg2.connect(
        database="d5nlcc5k9d83qo", user=UN, password=PW, host='ec2-3-213-228-206.compute-1.amazonaws.com',
        port='5432'
    )

    cursor = conn.cursor()

    cursor.execute('SET SCHEMA \'' + SCHEMA + '\'')

    cursor.execute('SELECT messages_sent, vc_joins from ' + TABLE + ' WHERE id=' + str(discord_id))

    result = cursor.fetchone()

    conn.close()

    return result