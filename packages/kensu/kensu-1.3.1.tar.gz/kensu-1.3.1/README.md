# kensu-client-python
Kensu Data Activity Manager - Official Python Client

To use the Python client, install Anaconda (https://www.anaconda.com/distribution/)

In the environment tab, create a new environment: 
Click on Create - Define a name - Check the Python box and select Python 3.7. 

In your shell, execute the following commands:
`source "/anaconda3"/bin/activate NAMEOFENVIRONMENT`

> on Windows (having conda in your PATH):
> `conda activate <NAMEOFENVIRONMENT>`


Then install the library in your environment:
`pip install -r requirements.txt .`


## Run tests

`python -m unittest discover -s tests/unit`