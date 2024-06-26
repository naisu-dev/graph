import sympy as sp
import numpy as np
from flask import Flask, request, send_file, abort
import matplotlib.pyplot as plt
import io
import seaborn as sns

sns.set()
sns.set_style("whitegrid",{"grid.linestyle": "--"})

import japanize_matplotlib

app = Flask(__name__)

@app.route("/",methods=["GET"])
def main():
    try:
        formula = request.args.get("formula").replace(" ","+").split(",")
        x = sp.Symbol("x")
        img = sp.plotting.plot(*formula,(x,-8,8),ylim=(-8,8),legend=True,show=False)
        file = io.BytesIO()
        img.save(file)
        file.seek(0)
        return send_file(file,mimetype="image/png")
    except:
        return abort(400,"Generation Error")

@app.route("/line",methods=["POST"])
def line():
    data = request.get_json()

    plt.clf()
    plt.plot(data["x"],data["y"],color="red")
    plt.title(data["title"])
    plt.xlabel(data["xLabel"])
    plt.ylabel(data["yLabel"])
    plt.grid(True)
    plt.tick_params(axis="x",labelsize=data.get("xFont") or 12)
    plt.tick_params(axis="y",labelsize=data.get("yFont") or 12)

    file = io.BytesIO()
    plt.savefig(file,format="png",dpi=300)
    plt.clf()
    plt.cla()
    plt.close()

    file.seek(0)
    return send_file(file,mimetype="image/png")

@app.route("/pie",methods=["POST"])
def pie():
    data = request.get_json()

    plt.clf()
    plt.pie(
        data["data"],
        startangle=90,
        autopct="%.1f%%",
        counterclock=False,
        pctdistance=0.8,
        labels=data["label"],
        labeldistance=1.1,
        colors=data["color"]
    )
    plt.title(data["title"],fontsize=18)

    file = io.BytesIO()
    plt.savefig(file,format="png",dpi=300)
    plt.clf()
    plt.cla()
    plt.close()
    file.seek(0)
    return send_file(file,mimetype="image/png")

@app.route("/table",methods=["POST"])
def table():
    data = request.get_json()

    plt.clf()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.axis("off")
    ax.table(
        cellText=data["data"],
        colLabels=data["label"],
        cellLoc="center",
        loc="center"
    )

    fig.tight_layout()

    file = io.BytesIO()
    plt.savefig(file,format="png",dpi=300,bbox_inches="tight")

    plt.clf()
    plt.cla()
    plt.close()
    file.seek(0)
    return send_file(file,mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=4000)
