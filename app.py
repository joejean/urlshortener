import sqlite3, string, random
from flask import Flask, render_template, request, jsonify, redirect, g

DB = 'test.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = sqlite3.connect(DB)
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS urls(long_url text, short_url text)")
    db.commit()
    return db, cursor

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_db', None)
    if db is not None:
        db.close()


@app.route("/", methods = ['GET','POST'])
def index():
    if request.method == "POST":
        data = request.get_json()
        db, c = get_db()
        short_url = data['shortUrl']
        long_url = data['longUrl']
        if len(short_url) == 0:
            short_url = "".join(random.choice(string.ascii_lowercase) for i in range(6))
        c.execute("SELECT * FROM urls where short_url= ?", (short_url,))
        result = c.fetchone()
        if result is None:
            c.execute("INSERt INTO urls VALUES(?,?)", (long_url, short_url))
            db.commit()
            return jsonify(url="http://127.0.0.1:5000/"+short_url)
        else:
            pass
            #Todo handle case where there the short url is already in the db

    return render_template('index.html')


@app.route("/<name>")
def getLongUrl(name):
    data = request.get_json()
    db, c = get_db()
    short_url = str(name)
    c.execute("SELECT long_url FROM urls where short_url= ?", (short_url,))
    result = c.fetchone()
    if result is None:
        return jsonify(error="No such URL in our database")
    return redirect(result[0])


if __name__ == "__main__":
    app.run(debug=True)
