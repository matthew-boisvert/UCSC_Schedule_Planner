from flask import Flask, render_template, request
import pydal
import course_finder
import update_calendar
import url_shortener

app = Flask(__name__)


email = ""

@app.route("/", methods=['GET', 'POST'])
def index():
    controller = course_finder.DatabaseController()
    if(request.method == "GET"):
        return render_template("index.html", prefixes=controller.get_prefixes(), names=controller.get_course_names(), email="", numClasses="")
    elif(request.method == "POST"):
        print(request.form);
        email = request.form['email']
        numClasses = request.form['numClasses']
        return render_template("index.html", prefixes=controller.get_prefixes(), names=controller.get_course_names(), email=email, numClasses=numClasses)

@app.route("/submit", methods = ['POST', 'GET'])
def submit_form():
    data = []
    controller = course_finder.DatabaseController()
    for element in request.form:
        if("class_name" in element):
            if(controller.find_course(request.form[element]).date_time.isspace()):
                data.append({"name": request.form[element], "success": "No", "link": "Class is remote, no schedule available"})
            else:
                data.append({"name": request.form[element], "success": "Yes", "link": url_shortener.shorten_url(update_calendar.update_calendar(request.form[element], email))})
    return render_template("results.html", data=data)


if __name__ == "__main__":
    app.run(debug=True, port=5051)