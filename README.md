# RAG Project

This RAG project is a simple framework which provides an outline for the different elements required to add a RAG component to an LLM. This is designed as a demonstration and not meant to be used in production.

## Structure 

ui - Provides an interface for accepting user queries and adding documents to the context corpus. 
server - Accepts input from UI, finds the document with the greatest similarity and generates prompt using both elements. 
database - Contains the context corpus and all elements needed to calculate similarity. 

## Requirements 
  - Python

## Installation 

### UI 

No UI exists at present. 

### Server

To set up the project clone the repository. The following instructions assume that all the requirements have been met and that all commands are executed from the project server directory. 

Create a virtual environment 

`pip3 -m venv ./venv`

activate the environment (May differ depending on OS please check the correct command for your system)

`source ./venv/bin/activate`

Install all requirements

`pip3 install -r requirements.txt`

Start server 

`python3 main.py`

To stop the server press ctrl + C. 

## Usage 

There are several endpoints available. The examples will use curl to demonstrate the system. 

### Query the system 

The purpose of the system is to take a user query, process it to add context, send the response to a LLM and return the response. As this is just a demonstration project the system just returns the updated query to the user.

example: What film should I watch? 

`curl -i http://localhost:5000/query?What%20film%20should%20I%20watch`


### Add a document to the system 

To add a document to the system the request should be formatted in JSON 

example 1: films

`curl -X POST http://localhost:5000/add-document -d '{"name": "films", "contents": "Great films to watch are Star Wars: Return of the Jedi, Avatar and Mortal Engines."}'`

example 2: sports

`curl -X POST http://localhost:5000/add-document -d '{"name": "sports", "contents": "Some sports include: Horse Riding, Rugby, Basketball and Ice Hockey."}'`



## Glossary

RAG - Retrieval-Augmented Generation.
LLM - Large Language Model.
UI - User Interface.
context corpus - The group of documents used to provide context to a user request before being sent to the LLM. 
TF - Term Frequency
IDF - Inverse Document Frequency
TF-IDF - Similarity measure combining TF and IDF
