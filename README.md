# LinkedIn Company Post Scraper

This tools allows you to collect all the data of a company's LinkedIn posts for a specific month.
The date, text, reactions and link is put into a `.csv` file.

Afterwards a screenshot of each post is generated.

# Install & Run

Install the dependencies via

```
pip install -r requirements.txt
```

then run `linkedin.py` with the requested parameters
* `-u` LinkedIn username
* `-p` LinkedIn password
* `-c` the company you're interested in
* `-m` the month
* `-y` the year
