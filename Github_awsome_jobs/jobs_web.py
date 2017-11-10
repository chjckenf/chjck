import os

import sqlite3
from flask import Flask, g, render_template


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'chjck.db')
	))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def jobs():
    c = get_db()
    jobs = c.execute('SELECT * FROM jobs').fetchall()

    return render_template('base.html',
                           jobs=jobs,
                           )


@app.route('/<issue>')
def job_info(issue):
    c = get_db()
    job = c.execute('SELECT * FROM jobs WHERE numb=?',
                        (issue,)).fetchone()

    return render_template('content.html',
                           job=job
                           )


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
