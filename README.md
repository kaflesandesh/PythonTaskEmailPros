# PythonTaskEmailPros

## To create the virtual environment
python -m venv venv
## To activate
venv\Scripts\activate
## On mac os, use >> source venv/bin/activate

## Install dependencies (uncomment if the lines are commentd or add dependencies to the file and re-run the following line)
pip install -r requirements.txt

## To run app 
python app.py

## The project contains two main functionalities:
### git-clone-merge.py > Cloning the Git repository to extract email files and merging them into a single file for further processing.
### analyze.py > Analyzing the file to extract name, summarize mail contents, and derive sentiments. And we will get the results.jsonl file with required results 
