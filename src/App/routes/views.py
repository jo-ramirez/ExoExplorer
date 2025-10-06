from flask import Flask, render_template

from App import app
from App.database import query_by_id, query_rows


@app.route("/simulation_curve", methods=["GET"])
def simulation_curve():
    return render_template("simulation_curve.html")

@app.route("/", methods=["GET"])
def index():
    results = query_rows(12)

    table_columns = results.columns.tolist()
    table_rows    = results.to_dict(orient="records")

    return render_template(
        "index.html",
        table_columns=table_columns,
        table_rows=table_rows,
    )