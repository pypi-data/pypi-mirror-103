import json
import requests


def lookup(*args, **kwargs):
    r = requests.get("https://api.crossref.org/works/" + kwargs.get("doi"))
    data = json.loads(r.content.decode('utf-8'))
    arg = args[0]
    options = {
        "title": str(data["message"]["title"][0]),
        "author": str(data["message"]["author"][0]["given"]) + " " + str(
            data["message"]["author"][0]["family"]),
        "publisher": str(data["message"]["publisher"]),
        "link": str(data["message"]["link"][0]["URL"]),
    }

    for i in range(len(options)):
        if arg in options:
            return options[arg]
    else:
        return "Invalid Parameter"
