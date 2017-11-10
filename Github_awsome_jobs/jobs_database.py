import requests
import sqlite3
from markdown import markdown


def job_table():
    with sqlite3.connect('chjck.db') as db:
        c = db.cursor()

        c.execute('drop table if exists jobs')
        c.execute('CREATE TABLE jobs '
                  '(numb INTEGER, name TEXT, content TEXT)'
                  )

        page = 1
        done = False

        while done is False:
            resp = requests.get('https://api.github.com/repos/awesome-'
                                'jobs/vietnam/issues?page={}'.format(page)
                                )
            data = resp.json()
            result = []

            if not data:
                done = True
                break
            else:
                for job_info in data:
                    result.append((job_info['number'],
                                   job_info['title'],
                                   markdown(job_info['body'])
                                   ))

            page += 1
            c.executemany('insert into jobs values (?, ?, ?)', result)


def main():
    job_table()


if __name__ == '__main__':
    main()
