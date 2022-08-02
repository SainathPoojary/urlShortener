
from ast import Try
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/utility/create", methods=["GET"])
def create():
    data = dict()
    url = request.args.get("longUrl")
    shortName = request.args.get("shortName")
    print("==========================>",url, shortName)

    if(Links.query.filter_by(shortName=shortName).first()):
        print(Links.query.filter_by(shortName=shortName).first())
        data["valid"] = False
        return data
    link = Links(shortName=shortName, url=url)
    db.session.add(link)
    db.session.commit()
    data["url"] = f'{request.url_root}{shortName}'
    data["valid"] = True
    return jsonify(data)


@app.route("/<shortName>")
def navigate(shortName):
    if(Links.query.filter_by(shortName=shortName).first()):
        link = Links.query.filter_by(shortName=shortName).first()
        return redirect(link.url)
    else:
        return render_template("index.html")


class Links(db.Model):
    shortName = db.Column(db.Text, primary_key=True)
    url = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"[{self.shortName},{self.url}]"


if(__name__ == "__main__"):
    app.run("0.0.0.0", 8080, debug=True)
