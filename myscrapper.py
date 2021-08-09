from flask import Flask, render_template, request, redirect
from scrapper import get_jobs

app = Flask("myScrapper")


@app.route("/")  # @에 붙은 상황이 일어나면, "바로 아래" 있는 함수를 실행시키는 역할을 한다.
def home():
    return render_template("main.html")


@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        jobs = get_jobs(word)
        print(jobs)
    else:
        return redirect("/")
    return render_template("report.html", searchingBy=word)


app.run(debug=True)
