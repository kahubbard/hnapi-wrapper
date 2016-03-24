# hnapi-wrapper
Python wrapper for the Firebase Hacker News API

`hnapi.py` is a simple wrapper around the official HN API hosted on Firebase. `hn_job_search.py` is a sample program that uses `hnapi` to  search posts submitted by the whoishiring user.

usage: hn_job_search.py [-h] --date DATE [--hiring] [--hired] [--freelance]
                        [--all]

Hacker News Job Search

optional arguments:

  -h, --help   show this help message and exit
  
  --date DATE  month year string, e.g. 'January 2015'
  
  --hiring     only search the 'who is hiring' threads
  
  --hired      only search the 'who is looking to be hired' threads
  
  --freelance  only search the 'freelancer' threads
  
  --all        searches all submissions from 'whoishiring'
