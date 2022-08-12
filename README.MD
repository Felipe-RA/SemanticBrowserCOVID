

## Instructions

- Install the required dependencies (a requirements file is provided below)
- Run the `run.py` file

## Some considerations

We noted that the server providing access to the API is located in Europe. Since a sizable lattency was detected (around 600ms avg.), we decided to bulk the access to the API into as few calls as possible. Lattency does add up, specially for common queries.


## Proposals to improve this project

This implementation was made in a hurry, lots of things were not implemented, as a way to acknowledge the shortcomings of this implementation (and as a possible roadmap), we propose to work on the following:

- Work upon the design of a complete schema for the Database (or fully implement the one designed at **inspirehep**)
- Define DB constrains for critical data
- Lots of data are missing, but perhaps some of them can be infered through clever relationships between the provided APIs. (this will need a more careful look at the APIs)
- Create indexes for the collection to improve query performance
- As we dont know the resources available for the deployment of the DB server, we do not have the criteria to recommend a sharded cluster deployment.



## Requirements

To install the required dependencies you have two options:

- **With pip:** 
>`pip install -r requirements.txt`
- **If you work with Conda Environments:** 
>`conda env create -f environment.yml`

Both `requirements.txt` and `environment.yml` are provided at this repo.