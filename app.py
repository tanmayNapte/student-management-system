# app.py
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# connect to database
def get_db():
    return sqlite3.connect("students1.db")

# create table (runs once)
with get_db() as con:
    con.execute(
        """CREATE TABLE IF NOT EXISTS students
                ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    course TEXT )
        """
    )


@app.route("/")
def index():
    con = get_db()
    students = con.execute("SELECT * FROM students").fetchall()
    return render_template("index.html", students=students)

@app.route("/add", methods=["GET", "POST"])
def add_student():

    con = get_db()
    if request.method == "POST":
        first = request.form["first_name"]
        middle = request.form["middle_name"]
        last = request.form["last_name"]

        full_name = " ".join(part for part in [first, middle, last] if part)
        age = request.form["age"]
        course = request.form["course"]
        con.execute(
            "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
            (full_name, age, course)
        )

        con.commit()
        return redirect("/")

    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    con = get_db()

    if request.method == "POST":
        first = request.form["first_name"]
        middle = request.form["middle_name"]
        last = request.form["last_name"]

        full_name = " ".join(part for part in [first, middle, last] if part)

        age = request.form["age"]
        course = request.form["course"]

        con.execute(
            "UPDATE students SET name = ?, age = ?, course = ? WHERE id = ?",
            (full_name, age, course, id)
        )
        con.commit()
        con.close()
        return redirect("/")

    student = con.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()
    con.close()

    return render_template("edit.html", student=student)


@app.route("/delete/<int:id>")
def delete_student(id):
    con = get_db()
    con.execute("DELETE FROM students WHERE id = ?", (id,))
    con.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run()

