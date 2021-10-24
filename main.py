from flask import Flask, render_template, request, flash
from SearchEngine import SearchEngine

app = Flask(__name__)
app.secret_key = 'trabalho123'

# data = [
#     {"name": 'test1'},
#     {"name": 'test2'},
#     {"name": 'test3'}
# ]

@app.route("/")
def initial_page():
    return render_template("main_page.html")

@app.route("/search", methods=["POST", "GET"])
def search_page():
    data = []
    flash(request.form['search_input'])
    palavra_buscada = request.form['search_input']
    SE = SearchEngine()
    response = SE.PerformSearch(palavra_buscada)
    for result in response["response"]:
        data.append({
            "url": result["url"],
            "title": result["title"],
            "extract": result["text"],
            })
    return render_template("search_results.html", data=data)