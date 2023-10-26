import json
import pytest
import requests
import sseclient
from app import create_app, get_db_connection
from listener import RawEvent


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_connection():
    # Call the get_db_connection function
    conn = get_db_connection()

    # Check that the returned connection is not None
    assert conn is not None
    return conn


def test_index(client):
    """Test the / endpoint.
    If this fails, try to run listener.py"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'total_scores' in data
    assert 'scores' in data
    print('/', data)


def test_users_with_scores(client):
    """Test the /users-with-scores endpoint."""
    response = client.get('/users-with-scores')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert isinstance(data, list)


def test_student_scores(client, db_connection):
    """Test the /student/<student_id> endpoint."""
    # First, get a list of current student ids
    cursor = db_connection.cursor()
    row = None
    while not row:
        cursor.execute('SELECT studentId FROM scores;')
        row = cursor.fetchone()
    cursor.close()
    db_connection.close()
    # Use with a valid student ID from your test data
    student_id = row[0]
    response = client.get(f'/student/{student_id}')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'student_results' in data
    assert 'average_score' in data


def test_exams(client):
    """Test the /exams endpoint."""
    response = client.get('/exams')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert isinstance(data, list)


def test_exam_results(client, db_connection):
    """Test the /exam/<exam_id> endpoint."""
    # First, get a list of current exam ids
    cursor = db_connection.cursor()
    row = None
    while not row:
        cursor.execute('SELECT exam FROM scores;')
        row = cursor.fetchone()
    cursor.close()
    db_connection.close()
    # Use with a valid exam ID from your test data
    exam_id = row[0]
    response = client.get(f'/exam/{exam_id}')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'exam_results' in data
    assert 'average_score' in data


def test_queue_is_represented(client):
    n_events = 5
    URL = 'https://live-test-scores.herokuapp.com/scores'
    response = requests.get(URL, stream=True)
    stream = sseclient.SSEClient(response)
    i = 0
    for event in stream.events():
        raw_event = RawEvent(event.event, event.data)
        # Use with a valid student ID from your test data
        student = json.loads(raw_event.raw_data)
        student_id = student['studentId']
        # Check response of /student/student_id
        response = client.get(f'/student/{student_id}')
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert 'student_results' in data
        assert 'average_score' in data
        # Check response of /exam/exam_id
        exam_id = student['exam']
        response = client.get(f'/exam/{exam_id}')
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert 'exam_results' in data
        assert 'average_score' in data

        i = i + 1
        if i > n_events:
            return True


if __name__ == '__main__':
    pytest.main()
