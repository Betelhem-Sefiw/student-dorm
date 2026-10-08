import csv
import os
from flask import Flask, render_template, request

app = Flask(__name__)

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "students.csv")


def load_students():
    students = {}
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row["student_id"].strip().upper()
            students[sid] = row
    return students


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    query = ""

    if request.method == "POST":
        query = request.form.get("student_id", "").strip().upper()
        if not query:
            error = "Please enter your Student ID."
        else:
            students = load_students()
            if query in students:
                result = students[query]
            else:
                error = f"No dorm assignment found for ID: {query}"

    return render_template("index.html", result=result, error=error, query=query)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)