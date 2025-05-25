from flask import Flask, render_template, request
import sqlite3
from collections import Counter

app = Flask(__name__)


def get_stats(keyword=None):
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()

    if keyword:
        # Search job titles that contain the keyword (case-insensitive)
        query = "SELECT title, location, date_posted FROM jobs WHERE title LIKE ?"
        c.execute(query, ('%' + keyword + '%',))
    else:
        query = "SELECT title, location, date_posted FROM jobs"
        c.execute(query)

    rows = c.fetchall()
    conn.close()

    titles = [row[0] for row in rows]
    locations = [row[1] for row in rows]
    dates = [row[2] for row in rows]

    top_titles = Counter(titles).most_common(5)
    top_cities = Counter(locations).most_common(5)
    date_trends = Counter(dates).most_common()

    return top_titles, top_cities, date_trends


@app.route('/', methods=['GET', 'POST'])
def index():
    keyword = request.form.get('keyword') if request.method == 'POST' else None
    top_titles, top_cities, date_trends = get_stats(keyword)
    return render_template('index.html', top_titles=top_titles,
                           top_cities=top_cities, date_trends=date_trends,
                           keyword=keyword)


if __name__ == '__main__':
    app.run(debug=True)
