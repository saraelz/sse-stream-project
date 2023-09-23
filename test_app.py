import json
import pytest
from app import app, get_db_connection


def test_db_connection():
    # Call the get_db_connection function
    conn = get_db_connection()

    # Check that the returned connection is not None
    assert conn is not None


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """Test the / endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'total_scores' in data
    assert 'scores' in data


def test_scores_database_populated(client):
    """Returns true if scores database has at least one entry.
    If this fails, try to run listener.py"""
    response = client.get('/')
    if response.status_code == 200:
        data = json.loads(response.data.decode('utf-8'))
        print('entries: ', data['total_scores'])
        assert data['total_scores'] > 0
    assert True


def test_users_with_scores(client):
    """Test the /users-with-scores endpoint."""
    response = client.get('/users-with-scores')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert isinstance(data, list)


def test_student_scores(client):
    """Test the /student/<student_id> endpoint."""
    # First, get a list of current student ids
    user_response = client.get('/users-with-scores')
    users_list = json.loads(user_response.data.decode('utf-8'))
    # Use with a valid student ID from your test data
    student_id = users_list[0]
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


def test_exam_results(client):
    """Test the /exam/<exam_id> endpoint."""
    # First, get a list of current exam ids
    exams_response = client.get('/exams')
    exams_list = json.loads(exams_response.data.decode('utf-8'))
    # Use with a valid exam ID from your test data
    exam_id = exams_list[0]
    response = client.get(f'/exam/{exam_id}')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'exam_results' in data
    assert 'average_score' in data


if __name__ == '__main__':
    pytest.main()
