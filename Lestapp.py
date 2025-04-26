from flask import Flask, render_template, request
import math
from collections import Counter

app = Flask(__name__)

def calculate_tfidf(word_counts, total_words, document_count):

    tf = word_counts / total_words if total_words > 0 else 0
    idf = math.log(document_count / (1 + (1 if word_counts > 0 else 0)))
    return tf * idf


@app.route("/", methods=["GET", "POST"])
def index():

    table_data = []
    if request.method == "POST":
        if "file" not in request.files:
            return render_template("index.html", error="No file part")
        file = request.files["file"]
        if file.filename == "":
            return render_template("index.html", error="No selected file")
        if file:
            try:
                text = file.read().decode("utf-8")
                words = text.lower().split()
                word_counts = Counter(words)
                total_words = len(words)
                document_count = 1


                tfidf_data = []
                for word, count in word_counts.items():
                    tfidf = calculate_tfidf(count, total_words, document_count)
                    tfidf_data.append({
                        "word": word,
                        "tf": count / total_words if total_words > 0 else 0,
                        "idf": math.log(document_count / (1 + (1 if count > 0 else 0))),
                        "tfidf": tfidf
                    })

                    sort_by = request.args.get("sort", "idf")
                    reverse = True
                    if sort_by == "tf":
                        tfidf_data.sort(key=lambda x: x["tf"], reverse=reverse)
                    else:
                        tfidf_data.sort(key=lambda x: x["idf"], reverse=reverse)

                tfidf_data.sort(key=lambda x: x["tf"], reverse=reverse)
                print(tfidf_data[:5])

                table_data = tfidf_data[:50]

            except Exception as e:
                error = f"Error processing file: {str(e)}"


    return render_template("index.html", table_data=table_data)


if __name__ == "__main__":
    app.run(debug=True)