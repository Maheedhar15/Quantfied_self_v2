<---------------- QuantifiedSelf V2 application ----------------->


This is a manual for the users on how to use the QuantifiedSelf V2 application.

QuantifiedSelf aims to track your progression via numbers or explicitly by the data that the user provides concurrently.

Instructions on how to run the code:

1) Setup a redis-server on your linux environment and turn the server on using the command 
   "redis-server" on the terminal.
2) Navigate to the project directory and open three more terminals.
3) In one of the terminals, use the command cd frontend/ to go to the frontend folder and use the command "npm run serve" to start the vue application.
4) The vue app cannot function without the flask API. 
5) Hence, go to the other two terminals and enter the command cd backend/ to go to the backend directory.
6) On the backend directory, enter the command "source flask/bin/activate" to activate the virtual environment.
7) In one of the two terminals, enter the command "python application.py" to start the flask API server
8) In the other terminal, enter the command "celery -A application.celery worker --loglevel info" to start the celery application for the asynchronous tasks to run.
9) After this, the app is ready for testing

These are the general instructions on how to use the QuantifiedSelf V2 application.



