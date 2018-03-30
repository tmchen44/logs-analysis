# Logs Analysis Tool

This reporting tool extracts and summarizes data from a mock news article website.

## Quick Start

What you'll need:
- Python 3
- PostgreSQL
- psycopg2

What to do:
1. Download the database file used for the project [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).
2. Once you have extracted the `newsdata.sql` file, in the same directory, run the command `psql -d news -f newsdata.sql`. This will set up the database and tables used in the logs analysis.
3. Run the script analysis with the command `python3 newsdb.py`. The results will appear in the terminal as well as in a file named `results.txt`.

## Project Overview

This project serves as a reporting tool for a mock news article website. The data resides in a PostgreSQL database that consists of three tables:
- Two of the tables hold information about the articles and authors, respectively.
- The third table provides information about the HTTP requests made to different paths within the website, and whether those requests were successful or not.

The Python script connects to the database using the psycopg2 module and makes several queries to the database. These queries can be used to answer useful data analysis questions, such as "What are the most popular articles?" or "Who are the most popular authors?" The results of each query can be printed to the command prompt as well as written to a plain text file.
