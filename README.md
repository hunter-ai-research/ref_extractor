# Reference Extractor
A tool to extract references from STEM research papers

## Installation & Usage
> All commands are written as if you were executing them from the repository root

### Setup
The project's dependencies are listed in the `requirements.txt` file. 
To install them, run `pip install -r ./requirements.txt`.

Currently, Reference Extractor uses **Amazon Textract** for document parsing. 
Please make sure to specify `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in the environment variables before running the app.

### Run
After setting up the project, run the app using `python ./src/main.py [path to research pdf]`.
To not drain your AWS credits, you can cut all the pages except References/Bibliography section, so that Textract does not parse them.

The program will output the extracted references.

### Customizability
There is a variety of ways to deal with extracted references. You might want to
- print them
- save them to a file
- send them to your backend

or do anything else. The only thing you need to do is to edit the `handle_references` function located in `./src/handler.py` to serve your needs. 
