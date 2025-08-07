from flask import Flask, render_template, request, redirect, url_for
from model_loader import load_model_and_search
from model_labels import MODEL_LABELS
import json
import os

app = Flask(__name__)

RELEVANSI_FILE = 'data/relevansi.json'

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    expanded_query = []
    query = ""
    mode = ""
    selected_model_label = ""

    if request.method == "POST":
        query = request.form["query"]
        model_name = request.form["model"]
        mode = request.form["mode"]

        search_result = load_model_and_search(query, model_name, mode)
        expanded_query = search_result["expanded_query"]
        results = search_result["results"]

        selected_model_label = MODEL_LABELS.get(model_name, model_name)

    return render_template("index.html", results=results, expanded_query=expanded_query, query=query, mode=mode, selected_model_label=selected_model_label)

@app.route("/simpan_relevansi", methods=["POST"])
def simpan_relevansi():
    query = request.form.get("query")
    model = request.form.get("model")
    data = request.form.to_dict()

    relevan = []
    tidak_relevan = []

    for k, v in data.items():
        if k.startswith("relevansi_"):
            doc_id = k.split("_")[1]
            if v == "relevan":
                relevan.append(doc_id)
            elif v == "tidak":
                tidak_relevan.append(doc_id)

    simpanan = {
        "query": query,
        "model": model,
        "dokumen_relevan": relevan,
        "dokumen_tidak_relevan": tidak_relevan,
        "total_relevan": len(relevan),
        "total_tidak_relevan": len(tidak_relevan)
    }

    # Load file lama
    if os.path.exists(RELEVANSI_FILE):
        with open(RELEVANSI_FILE, "r") as f:
            all_data = json.load(f)
    else:
        all_data = []

    all_data.append(simpanan)

    with open(RELEVANSI_FILE, "w") as f:
        json.dump(all_data, f, indent=2)

    return redirect(url_for("lihat_relevansi"))

# Placeholder route untuk melihat hasil
@app.route("/lihat_relevansi")
def lihat_relevansi():
    if os.path.exists(RELEVANSI_FILE):
        with open(RELEVANSI_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    return render_template("relevansi.html", data=data)

#------Route untuk menghapus----#
@app.route("/relevansi/hapus/<int:index>")
def hapus_relevansi(index):
    # Misalnya kamu simpan relevansi di file JSON
    with open("data/relevansi.json", "r") as f:
        data = json.load(f)

    if 0 <= index < len(data):
        data.pop(index)

        with open("data/relevansi.json", "w") as f:
            json.dump(data, f, indent=4)

    return redirect(url_for("lihat_relevansi"))


if __name__ == "__main__":
    app.run()





