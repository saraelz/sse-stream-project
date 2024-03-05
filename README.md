## Storing Server Sent Events arriving from a Stream of SSEs


At `https://live-test-scores.herokuapp.com/scores` you'll find a service that follows the [Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events) protocol. You can connect to the service using cURL:

        curl https://live-test-scores.herokuapp.com/scores

Periodically, you'll receive a JSON payload that represents a student's test score (a JavaScript number between 0 and 1), the exam number, and a student ID that uniquely identifies a student. For example:

        event: score
        data: {"exam": 3, "studentId": "foo", score: .991}

This represents that student foo received a score of `.991` on exam #3. 

Your job is to build an application that consumes this data, processes it, and stores it efficiently such that the data can be queried for various purposes.

Code
Issues
Pull requests
Actions
Projects
Wiki
Security
Insights

    Settings

Breadcrumbs

    sse-stream-p



My solution:

* My source is the data stream. The data sink is the SQL database. Downstream of the database we can use Flask to surface the results.

* The input is a single threaded data stream - if the server can't catch up to the single threaded stream then you lag behind the stream and may never catch up again. One process is responsible for reading data, but a multi-threaded queue is responsible for writing to SQL server. 

Running the Project:

You need three applications running:
(1) app.py
(2) listener.py
(3) PostgreSQL

Additional Commands

* Within the consumer function, queue.get() waits until the producer adds something to the queue. It continues processing data as long as the queue is not empty.

* Three processes compete for messages in the queue based on availability. When one consumer picks up data from the queue, it is removed from the queue.

* The Big O complexity is O(n), where n is the number of events. For each event, an SQL operation is performed.

Limitations
* The program can lag behind the data source if there is an excessive amount of data. This can be mitigated by adding more consumers.

Solutions:

* Vertical scaling (upgrading hardware) can help if the server cannot keep up with the data source.

* Horizontal scaling (adding more servers) can be beneficial for handling large data volumes.

* Data recovery is not possible in the event of a node failure. Distributed systems like Apache Spark offer solutions for distributed data processing with horizonatal scaling. I would consider implementing a distributed system with multiple nodes for enhanced scalability and fault tolerance.

How to run:

You need to install PostgreSQL, C++, and Python. Add the directory for pg_config and pip to your PATH env file.

This project is developed using Python version 3.11.

To view HTTP request headers, you can use the following command:

```
curl -i https://live-test-scores.herokuapp.com/scores
```


First, ensure that you have the latest version of pip by running:

```
python.exe -m pip install --upgrade pip
```

Then, install the necessary packages, including sseclient, by executing:

```
py -m pip install -r requirements.txt
```

You can run tests using pytest:
 
```
pytest test_app.py
```

For running the code in a virtual environment, follow these terminal commands:

```
# Activate the virtual environment (on Windows)
myenv\Scripts\activate
# Activate the virtual environment (on macOS/Linux)
# source myenv/bin/activate
# Install packages
python.exe -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

You should run the following applications in separate tabs in the terminal and leave them open:
```
py app.py
py listener.py
```
