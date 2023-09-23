This project is written in Python using version 3.11.

First, you can upgrade pip if you run python.exe -m pip install --upgrade pip. Now, if you run python3 -m pip install -r requirements.txt, it will install the specified packages, including sseclient.

You can run pytest test_app.py or specific test functions such as pytest test_app.py::test_exams

Since it's a Flask application which I also tested with Postman, I used the following terminal commands:
python3 -m venv myenv
# Activate the virtual environment (on Windows)
myenv\Scripts\activate
# Activate the virtual environment (on macOS/Linux)
# source myenv/bin/activate
# Install packages
python.exe -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
# Run Flask application 
python3 app.py


You need three applications running 
(1)
(2)
(3) postgres


Show the headers for the http request:
curl -i https://live-test-scores.herokuapp.com/scores 

The input is a single threaded data stream - if the server can't catch up to the single threaded stream then you lag behind the stream and may never catch up again. One process is responsible for reading data, but multiple multi-threaded queue are responsible for writing to SQL server. My source is the data stream. The data sink is the SQL database. Downstream of the database I've used Flask to surface the results.
