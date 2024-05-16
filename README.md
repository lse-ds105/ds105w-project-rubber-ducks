[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/9sIefOXK)

# Rubber Ducks Weather Analysis Project 🦆

## Our website link is:
[Rubber Ducks Weather Analysis Project](https://lse-ds105-ds105w-project-rubber-ducks-docshome-eaej5q.streamlit.app/) built using Streamlit.

## How to use this repository
The repository is organised into three main folders:
- Data
- Docs
- Notebooks

The notebooks folder is where all of the code that we used to gather and analyse our data is housed along with our ```custom_functions.py``` module. We chose to separate our code into **NB01-Data_Collection** and **NB02-Data_Analysis** so we could work on one task without disrupting the other.

The data folder is where we saved all of our data to once we had finished collecting it. Firstly it was saved as CSVs and JSONs before being combined into a SQL database for storage and querying efficiencies.

Finally, the docs folder contains the contents of our webpage.

## Set Up
### Create a new conda environment

Please create a new conda environment using the following terminal commands:
```bash
conda create -n venv-rubberducks python=3.11 ipython
conda activate venv-rubberducks
```
Install ```pip``` before installing the other required packages.
```bash
conda install pip
```
Use ```pip``` to install the ```requirements.txt```.
```bash
python -m pip install -r requirements.txt
```
You should now be ready to use our repository.

## How to recreate the work we produced...

After completing the setup, you should have all the necessary packages installed to run all of our notebooks and scripts.

### Data Collection and Preparation

To recreate our data collection process, open the NB01-Data_Collection notebook and hit 'run all' or if you'd prefer, run each cell separately in order.

Once that is complete, you are 95% of the way there. The final step is to follow the instructions at the bottom of the notebook that explain how we transformed our CSV data into a SQL database.

### Data Analysis

The next stage is to recreate our data analysis which is done by running our NB02-Data_Analysis notebook. This is where all the main plots for our site and a few others that didn't quite make the cut were initially drawn up.

### Website building

We built our website using Streamlit which is a python based web framework for producing data forward websites and dashboards. The home page is named 'Home.py' and can be found in the docs folder. The additional pages are stored in a subfolder called 'pages' as per the streamlit documentation. When running the website locally, you can use the terminal command ```streamlit run docs/Home.py```. This is what allowed us to view the site and make changes in real time before deploying it once we were ready.

---

And that's it 🤷🏼‍♂️. We hope you enjoy looking at our work as much as we enjoyed making it!
