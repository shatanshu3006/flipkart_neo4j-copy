from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import re
import spacy
from collections import defaultdict
from neo4j import GraphDatabase
from nltk.stem import WordNetLemmatizer


app = Flask(__name__)
CORS(app)  # Allow requests from React frontend

# Neo4j Credentials
NEO4J_URI = "neo4j+s://be36b918.databases.neo4j.io"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "pvkX5XeO_sWXQqwE9BNDZkf8csnlADKfKho__evcabg"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
lemmatizer = WordNetLemmatizer()
nlp = spacy.load("en_core_web_sm")

def lemmatize_word(word):
    return lemmatizer.lemmatize(word.lower())

def preprocess_input(user_input):
    stopwords = {"and", "or", "the", "of", "with", "for", "in"}
    words = re.split(r'\s+', user_input.lower())
    return [lemmatize_word(word.strip()) for word in words if word not in stopwords]

def get_pos_tags(user_input):
    doc = nlp(user_input)
    return {token.text.lower(): token.pos_ for token in doc}

def fetch_products_by_lemmatized_attributes(user_input):
    keywords = preprocess_input(user_input)
    if not keywords:
        return []

    query = """
    MATCH (p:Product)
    OPTIONAL MATCH (p)-[r]->(a)  
    WITH p, 
         COALESCE(a, {name: "N/A"}) AS a,  
         [key IN keys(p) | toLower(toString(p[key]))] AS product_values,  
         [key IN keys(a) | toLower(toString(a[key]))] AS attribute_values
    WITH p, attribute_values + product_values AS all_values, a
    WHERE any(keyword IN $keywords WHERE 
              any(value IN all_values WHERE value CONTAINS keyword))
    RETURN DISTINCT 
        p.uniq_id AS Product_ID, 
        p.product_name AS Product_Name, 
        p.brand AS Brand, 
        p.retail_price AS Price, 
        COLLECT(DISTINCT a.name) AS Matching_Attributes, 
        [keyword IN $keywords WHERE 
            any(value IN all_values WHERE value CONTAINS keyword)] AS Matched_Words
    """

    with driver.session() as session:
        results = session.run(query, keywords=keywords)
        products = [record.data() for record in results]

    if not products:
        return []

    df_results = pd.DataFrame(products)

    if "Matched_Words" not in df_results.columns or df_results.empty:
        return []

    df_results["Matched_Words"] = df_results["Matched_Words"].apply(lambda x: ", ".join(x) if x else "N/A")
    df_results["Matched_Word"] = df_results["Matched_Words"].apply(lambda x: x.split(", ")[0] if x != "N/A" and x else "N/A")

    return reorder_results(df_results, user_input)

def reorder_results(df_results, user_input):
    pos_tags = get_pos_tags(user_input)
    
    if "Matched_Word" not in df_results.columns:
        return df_results.to_dict(orient="records")

    grouped_results = defaultdict(list)
    for _, row in df_results.iterrows():
        match_word = row["Matched_Word"].lower() if isinstance(row["Matched_Word"], str) else "N/A"
        pos = pos_tags.get(match_word, "OTHER")
        grouped_results[pos].append(row)

    pos_order = ["NOUN", "OTHER", "VERB", "ADJ"]
    reordered = []
    for pos in pos_order:
        if pos in grouped_results:
            reordered.extend(grouped_results[pos])

    return pd.DataFrame(reordered).to_dict(orient="records")

@app.route("/search", methods=["GET"])
def search():
    user_input = request.args.get("query", "")
    print(user_input)

    if not user_input.strip():
        return jsonify({"error": "Invalid input"}), 400

    results = fetch_products_by_lemmatized_attributes(user_input)
    results = [{"Product_Name": item["Product_Name"]} for item in results]  # Extract product names correctly

    print(results)
    answer = jsonify(results)
    print(answer)
    return results

if __name__ == "__main__":
    app.run(debug=True)
