import os
import imdb
import openai

from flask import Flask, redirect, render_template, request, url_for

IMDB = imdb.IMDb()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":

        movieName = request.form["Movie"]

        search = IMDB.search_movie(movieName)

        id = search[0].movieID

        movie = IMDB.get_movie(id)

        movieDic = dict(movie)

        Plot = ""

        Plot += movieDic["plot"][0]
        
        print(Plot)

        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(Plot),
            temperature=1,
            max_tokens = 4000,
        )

        return redirect(url_for("index", result=Plot + " " + response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(Plot):
    return """Continue the story of the movie from a given plot summary: """ + Plot
