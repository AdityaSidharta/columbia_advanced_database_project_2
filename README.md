# CS6111 - Advanced Database System - Project 2

## Team Members
```
Name: Aditya Kelvianto Sidharta
UNI: aks2266
```

## List of Files
```
├── .gitignore -> Not including model files into the github repository
├── LICENSE -> MIT License for the project
├── README.md -> Readme for the project
├── display.py -> Functions that responsible to format printing to Standard Output
├── entities.py -> Functions to perform entity prediction and entity relation prediction
├── example -> Original example scripts provided by the Course Instructor
│ ├── example_relations.py 
│ ├── example_relations_original.py
│ ├── spacy_help_functions.py
│ └── spacy_help_functions_original.py
├── project2.py -> Main Script running the program
├── notebooks -> Various jupyter notebooks used to debug the algorithm and explore the functions
│ ├── beautiful_soup.ipynb
│ ├── example_relations.ipynb
│ ├── full_run.ipynb
│ ├── google_search.ipynb
│ └── spacy_help_functions.ipynb
├── pretrained_spanbert -> Folder used to save the spanbert model
│ └── config.json
├── pytorch_pretrained_bert -> Spanbert model
│ ├── __init__.py
│ ├── file_utils.py
│ ├── modeling.py
│ ├── optimization.py
│ └── tokenization.py
├── relations.txt -> List of relations supported by spanbert
├── requirements.txt -> Packages used for the program
├── scripts -> Bash Script used to download the pretrained spanbert model
│ └── download_finetuned.sh
├── search.py -> Functions used to perform google search and scrape the queried sites
├── spanbert.py -> Functions used to perform spanbert prediction
└── validation.py -> Functions used to validate the argument provided by the Standard Input
```


## Running the Program

### Setting up the program

This program assumes that you have:

1. Python 3.6 or later installed. Installation instructions can be found at: [https://www.tecmint.com/install-python-in-ubuntu/](https://www.tecmint.com/install-python-in-ubuntu/)
2. Virtual Environment Installed. Installation instructions can be found at: [https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

Setting up and Activating Virtual Environment and Installing the Required packages
```
python -m venv cs6111_proj2
source cs6111_proj2/bin/activate
pip install -U pip setuptools wheel
bash scripts/download_finetuned.sh
pip install -r requirements.txt
```

For the purpose of reproducibility, you need to setup an ipykernel that have the same environment that you have in your python program. In order to have the same environment in your jupyter notebook:
```
python -m ipykernel install --user --name adv_db2
```

### Executing the program
The syntax for running the program is as follows:
```
python -m main <google api key> <google engine id> <r> <t> <q> <k>
```

Example
```
python3 project2.py AIzaSyDhhK6kuFjOnRw4LDTfpwYaH5teRS48xLA ad8d80c3f1b726f69 1 0.7 "mark zuckerberg harvard" 17
python3 project2.py AIzaSyDhhK6kuFjOnRw4LDTfpwYaH5teRS48xLA ad8d80c3f1b726f69 2 0.7 "sundar pichai google" 35
python3 project2.py AIzaSyDhhK6kuFjOnRw4LDTfpwYaH5teRS48xLA ad8d80c3f1b726f69 3 0.7 "megan repinoe redding" 2
python3 project2.py AIzaSyDhhK6kuFjOnRw4LDTfpwYaH5teRS48xLA ad8d80c3f1b726f69 4 0.7 "bill gates microsoft" 10
```

## Internal Design of the project

### General Structure of the code
As explained in the list of files above, we separate the functions that are required to run the whole program into different python script based on its functionality. `project2.py` is used to assemble the different pieces together and act as the main program.

The reason of this code structure is modularity - we are able to change, update, or upgrade any of the modules in the program without changing other parts. For example, the `scrape` function can be easily adapted to use different method to take all the relevant text from a given webpages. 

Various parameters related to the available entity pair to be identified by Spacy as well as the entity pair relation prediction by spanBert is available in the `entities.py`. It can easily be modified to accommodate more relation predictions. Number of trimmed Characters (Currently set to 20000) can also be changed at `search.py`

### External Library Used
In order for us to freeze the environment, all the packages that we use have been included in the [requirements.txt](requirements.txt).

The main packages that we use in this project are:

- Spacy: Perform entity recognition
- PyTorch: Build spanBERT model
- Numpy: Vectorized Operation on Numerical Array
- Fire: CLI Argument
- Urllib: Opening Online sites
- BeautifulSoup: HTML Extraction
- GoogleAPIClient: Google Queries


## Step 3 Description

- Firstly, We need to decide what is the query that we are going to use. If its our first iteration, then we will select the query provided in argument. Else, we will choose query from our `result` that have not been previously explored

- We will then use urllib and beautiful soup to scrape the text content of all the links provided from our google query. Its possible that the site does not allow us to scrape the content, and thus we will skip if that is the case

- We will only choose 20000 first character, however we will discard non-complete words. Thus, we will most likely return less than 20000 Characters

- We will use spacy to detect entity pairs and spanbert to predict relations between entity pair. The relation provided in the argument is used to filter the right type of subject / object pair from the spacy result

- This proposed result will be collected, and new subject/object will be added to the overall result. If the pair has already existed, we update the confidence value if the new pair have higher confidence

## Search Engine JSON API Key and Engine ID

```
API Key: AIzaSyDhhK6kuFjOnRw4LDTfpwYaH5teRS48xLA
Engine ID: ad8d80c3f1b726f69
```

## Query Transcript of Test Cases
- [Run Logs](run_logs.txt)