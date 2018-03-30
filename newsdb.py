#!/usr/bin/env python3

import psycopg2
import sys

DBNAME = 'news'


def get_popular_articles():
    """Finds and prints the most popular three articles of all time, sorted by
    article views, with the most popular article at the top.
    """

    query = """select articles.id, articles.title, count(log.path) as views
                from articles left join log
                on log.path like concat('%', articles.slug)
                group by articles.id
                order by views desc
                limit 3;
                """
    results = select_query(query)
    title = "What are the most popular three articles of all time?"
    print_results(title, results)


def get_popular_authors():
    """Finds and prints the most popular article authors of all time, sorted by
    article views, with the most popular author at the top.
    """

    query = """select authors.id, authors.name, count(log.path) as views
                from authors
                left join articles
                on authors.id = articles.author
                left join log
                on log.path like concat('%', articles.slug)
                group by authors.id
                order by views desc;
                """
    results = select_query(query)
    title = "Who are the most popular article authors of all time?"
    print_results(title, results)


def get_error_dates():
    """Finds the dates where more than 1% of requests led to errors in the log.
    """

    query = """select date from (
                    select time::date as date,
                    sum(case when status not like '200%' then 1 else 0 end)
                    as error,
                    count(*) as total
                    from log
                    group by time::date
                ) as stats
                where (100.0 * error / total) > 1.0;
                """
    results = select_query(query)
    title = "On which days did more than 1% of requests lead to errors?"
    print_results(title, results)


def select_query(query):
    """Queries the PostgreSQL database based on the string argument provided.

    Args:
        query (str): The select query

    Returns:
        results (tuple): A tuple containing the header (list) from the query
        results and the corresponding data from each row (list).
    """
    conn = psycopg2.connect("dbname={}".format(DBNAME))
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    headers = [header[0] for header in cursor.description]
    conn.close()
    return headers, rows


def print_results(title, results):
    """Prints the results of a query to the command line and a text file.

    Args:
        title (string): The title of the results table
        results (tuple): Tuple consisting of two elements. The first is the
        header (list) of the table, and the second is the data (list) from each
        row.
    """
    printer(title, results)
    printer(title, results, open("results.txt", "a"))
    return


def printer(title, results, file_handle=sys.stdout):
    """Prints content to the command line or a text file.

    Args:
        title (string): The title of the results table
        results (tuple): Tuple consisting of two elements. The first is the
        header (list) of the table, and the second is the data (list) from each
        row.
        file_handle (object): Object handle containing the output destination
        of the print function, which is the command line or a file.
    """
    print(title, file=file_handle)
    headers = results[0]
    rows = results[1]
    n_col = len(headers)
    for i, header in enumerate(headers):
        if i == n_col - 1:
            print(header, file=file_handle)
        else:
            print(header + ' -- ', end='', file=file_handle)
    for row in rows:
        for i, col in enumerate(row):
            if i == n_col - 1:
                print(str(col), file=file_handle)
            else:
                print(str(col) + ' -- ', end='', file=file_handle)
    print(file=file_handle)
    return


if __name__ == '__main__':
    get_popular_articles()
    get_popular_authors()
    get_error_dates()
