from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    lat = 51.74708
    lon = 19.45404
    return render_template("example.html", lat=lat, lon=lon)


if __name__ == "__main__":
    app.run(debug=True)
