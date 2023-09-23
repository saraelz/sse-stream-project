## Coding test


At `https://live-test-scores.herokuapp.com/scores` you'll find a service that follows the [Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events) protocol. You can connect to the service using cURL:

        curl https://live-test-scores.herokuapp.com/scores

Periodically, you'll receive a JSON payload that represents a student's test score (a JavaScript number between 0 and 1), the exam number, and a student ID that uniquely identifies a student. For example:

        event: score
        data: {"exam": 3, "studentId": "foo", score: .991}

This represents that student foo received a score of `.991` on exam #3. 

Your job is to build an application that consumes this data, processes it, and stores it efficiently such that the data can be queried for various purposes. 

You may build this application in any language or stack that you prefer; we will use this project as part of your onsite interviews, so pick a language and tech stack with which you would be comfortable in a live coding session. You may use any open-source libraries or resources that you find helpful. **As part of the exercise, please replace this README file with instructions for building and running your project.** We will run your code as part of our review process.

Here are the purposes for which we might want to query the data and for which you should include SQL for reading from the data store:

1. List all users that have received at least one test score
2. List the test results for a specified student, and provides the student's average score across all exams
3. List all the exams that have been recorded
4. List all the results for the specified exam, and provides the average score across all students

Coding tests are often contrived, and this exercise is no exception. To the best of your ability, make your solution reflect the kind of code you'd want shipped to production. A few things we're specifically looking for:

* Well-structured, well-written, idiomatic, safe, performant code.
* Tests, reflecting the level of testing you'd expect in a production service.
* Good data schema design. Whatever that means to you, make sure your implementation reflects it, and be able to defend your design.
* Ecosystem understanding. Your code should demonstrate that you understand whatever ecosystem you're coding against— including project layout and organization, use of third party libraries, and build tools.

That said, we'd like you to cut some corners so we can focus on certain aspects of the problem:

* You don't need to worry about the “ops” aspects of deploying your service — load balancing, high availability, deploying to a cloud provider, etc. won't be necessary.

That's it. Commit your solution to the provided GitHub repository (this one) and submit the solution using the Greenhouse link we emailed you. When you come in, we'll pair with you and walk through your solution and extend it in an interesting way.



My solution:

My source is the data stream. The data sink is the SQL database. Downstream of the database we can use Flask to surface the results.

The input is a single threaded data stream - if the server can't catch up to the single threaded stream then you lag behind the stream and may never catch up again. One process is responsible for reading data, but a multi-threaded queue is responsible for writing to SQL server. 


How to run this file:

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
# Run applications in separate tabs and leave them open
python3 app.py
python3 listener.py


You need three applications running:
(1) app.py
(2) listener.py
(3) postgres


Show the headers for the http request:
curl -i https://live-test-scores.herokuapp.com/scores 

inside the consumer function, queue.get() is going to just wait until the producer puts something inside the queue. while true: if queue is empty then wait

three proceses fighting over messages in queue based on availability
when one consumer picks up data from the queue, it gets deleted from the queue

make sure consumer doesn't die 
try 
print
if consumer fails it wont share error

add if json = {}
then print error

test - 
make queue
fake some data
see how consumer reacts

big o is the number of events O(n) where n is the number of events. in an event do operation sql

postgres is usually running away from application in real life

Limitation - my program can lag behind the source - we improve it by having more consumers but 

1. what if theres so much data that my server isn't keeping up at the data source
2. not enough consumers
3. everything on one node

Limitations - 
vertical scaling - throw money - buy a better computer with more CPU that runs functions faster and supports more processes - a better computer can run more processes
horizontal scaling - more computers to do the same job
what happens when this one node goes down? multi distributed system like Spark might have some horizontal scaling options
we have one producer, multiple consumers
no way to recover lost data if the node goes down
Spark might try to answer distributed system and multiple consumers and producers and they wouldn't exist on one server it would be multiple servers.


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

Show the headers for the http request:
curl -i https://live-test-scores.herokuapp.com/scores 
