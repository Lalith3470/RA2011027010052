import requests
from flask import Flask, request, jsonify
import json
import time
from concurrent.futures import ThreadPoolExecutor

app = Flask(_name_)

def fetch_numbers(url):
    try:
        res = requests.get(url, timeout=2)
        res.raise_for_status()
        data = res.json()
        return data.get("numbers", [])
    except (requests.exceptions.RequestException, json.JSONDecodeError):
        return []

def merge_sorted_lists(lists):
    lst = []
    while any(lists):
        sm = float("inf")
        sm_list = None
        for i, lst in enumerate(lists):
            if lst and lst[0] < sm:
                sm = lst[0]
                sm_list = i
        lst.append(sm)
        lists[sm_list].pop(0)
    return lst

@app.route("/numbers", methods=["GET"])
def get_numbers():
    urls = request.args.getlist("http://localhost:3000/numbers?url=http://20.244.56.144/numbers/primes&url=http://20.244.56.144/numbers/fibo&url=http://20.244.56.144/numbers/odd")

    with ThreadPoolExecutor() as executor:
        fus = [executor.submit(fetch_numbers, url) for url in urls]
        res = [future.result() for future in fus]

    mrg = merge_sorted_lists(res)
    res_data = {"numbers": mrg}
    return jsonify(res_data)

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=3000)
