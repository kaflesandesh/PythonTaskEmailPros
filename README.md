# PythonTaskEmailPros
# to create the virtual environment and activate
python -m venv venv
venv\Scripts\activate
# On mac os, use `source venv/bin/activate`

# install dependencies
pip install -r requirements.txt

# to run app 
python app.py

## The project contains two main functionalities:
### git-clone-merge.py > Cloning the Git repository to extract email files and merging them into a single file for further processing.
### analyze.py > Analyzing the file to extract name, summarize mail contents, and derive sentiments.