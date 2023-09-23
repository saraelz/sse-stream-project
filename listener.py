
import pdb
import json
import requests
import sseclient
import psycopg2  # Import the PostgreSQL library
import multiprocessing
from dataclasses import dataclass

NUM_CONSUMERS = 3
DELETE_TABLE_QUERY = 'DROP TABLE IF EXISTS scores;'
CREATE_TABLE_QUERY = '''
    CREATE TABLE scores (
        id SERIAL PRIMARY KEY,
        exam INTEGER,
        studentId TEXT,
        score REAL
    )
'''


@dataclass
class RawEvent:
    event: str
    raw_data: dict


def get_db_connection():
    # Set up PostgreSQL connection
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    return conn


conn = get_db_connection()
with conn.cursor() as cursor:
    cursor.execute(DELETE_TABLE_QUERY)
    cursor.execute(CREATE_TABLE_QUERY)
    conn.commit()
cursor.close()


def producer(queue: multiprocessing.Queue):
    URL = 'https://live-test-scores.herokuapp.com/scores'
    response = requests.get(URL, stream=True)
    client = sseclient.SSEClient(response)
    for event in client.events():
        event = RawEvent(event.event, event.data)
        queue.put(event)


def consumer(queue: multiprocessing.Queue, consumer_id: str):
    print('hello from consumer #', consumer_id)
    while True:
        raw_event = queue.get()
        print(consumer_id, 'recieved a message')
        try:
            if raw_event.event == 'score':
                parsed_data = json.loads(raw_event.raw_data)
                insert_into_scores_table(parsed_data)
        except Exception as error:
            # handle the exception
            print(raw_event.raw_data)
            print('An exception occurred: ', error)


def insert_into_scores_table(scores_dict):
    # insert data into PostgreSQL
    if scores_dict and isinstance(scores_dict, dict):
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO scores (exam, studentId, score)
                VALUES (%s, %s, %s)
            ''', (scores_dict.get('exam'), scores_dict.get('studentId'), scores_dict.get('score')))
            conn.commit()


def main():
    queue = multiprocessing.Queue()

    consumer_procs = []
    for i in range(NUM_CONSUMERS):
        consumer_procs.append(
            multiprocessing.Process(
                target=consumer,
                args=(queue, str(i))
            )
        )
    # start processes
    for consumer_proc in consumer_procs:
        consumer_proc.start()

    producer(queue)


if __name__ == '__main__':
    main()
