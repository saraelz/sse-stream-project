import json
from flask import Flask, Response, jsonify
import psycopg2  # Import the PostgreSQL library
from psycopg2.extras import RealDictCursor

app = Flask(__name__)


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


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT id, exam, studentid, score FROM scores;')
    scores = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({
        'total_scores': len(scores),
        'scores': scores
    })


@app.route('/users-with-scores')
def users_with_scores():
    """List all users that have received at least one test score"""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT DISTINCT studentId FROM scores')
        users = [row[0] for row in cursor.fetchall()]

    return jsonify(users)


@app.route('/student/<student_id>')
def student_scores(student_id):
    """List the test results for a specified student, and student's average score across all exams"""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        # Get test results for a specified student
        cursor.execute(
            'SELECT studentid, exam, score FROM scores WHERE studentId = %s', (student_id,))
        student_results = cursor.fetchall()

        # Calculate the student's average score
        total_score = sum(result['score'] for result in student_results)
        average_score = total_score / \
            len(student_results) if len(student_results) > 0 else 0

    return jsonify({
        'student_results': student_results,
        'average_score': average_score
    })


@app.route('/exams')
def exams():
    """List all exams that have been recorded"""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT DISTINCT exam FROM scores')
        exams = [row[0] for row in cursor.fetchall()]

    return jsonify(exams)


@app.route('/exam/<exam_id>')
def exam_results(exam_id):
    """List all the results for the specified exam, and average score across all students"""
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        # List all results for the specified exam
        cursor.execute(
            'SELECT studentid, exam, score FROM scores WHERE exam = %s', (exam_id,))
        exam_results = cursor.fetchall()

        # Calculate the average score across all students for the exam
        total_score = sum(result["score"] for result in exam_results)
        average_score = total_score / \
            len(exam_results) if len(exam_results) > 0 else 0

    return jsonify({
        'exam_results': exam_results,
        'average_score': average_score
    })


if __name__ == '__main__':
    app.run(debug=True)
