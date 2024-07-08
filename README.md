# autocomplete_api

This is a starting point for creating an auto complete / suggest dropdown with FastAPI and Opensearch.

Make sure you have opensearch installed and running.

Create a virtual environment.

`python -m venv venv`

Enable the venv.

`source venv/bin/activate`

Run the create_index.py script.

`python3 ./create_index.py`

Start the api.

`uvicorn main:app --reload`

Open the index.html file in a browser and enter some text.

[Open Demo Web Page](./index.html)
