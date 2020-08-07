from flask import Flask, render_template
import pydal
import course_finder
import update_calendar

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    controller = course_finder.DatabaseController()
    return render_template("index.html", data=controller.get_course_names())


@app.route("/submit", methods = ['POST', 'GET'])
def submit_form():
    msg = update_calendar.update_calendar("CSE 138", "mboisver@ucsc.edu")
    return render_template("results.html", data=msg)


if __name__ == "__main__":
    app.run(debug=True, port=5051)