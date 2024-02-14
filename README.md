# data_curation
Python version used: 3.9.7.
1. Install required packeages in a dedicated environment:
- python -m pip venv venv
- source ./venv/bin/activate
- pip install -r requirements.txt

2. Run the data curation script with the tables in the same folder, depending on whether we want to include all cases (even those without any measurement):
- python data_curation_suliman.py
OR 
- python data_curation_suliman.py --include-all-cases
