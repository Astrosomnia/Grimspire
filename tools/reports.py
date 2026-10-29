#!/usr/bin/env python3
"""Pull in-game field reports from Firestore and print them as JSON, oldest first.

Signs in anonymously over REST, the same way the game does. The key is the game's public
Firebase web key (it already ships in index.html). Each item can then go onto the
Grimspire Field Reports board as New.

Usage: python3 tools/reports.py [--since <epoch ms>]
"""
import json, sys, urllib.request

KEY = "AIzaSyAecN2qYUyBBhjC0rdzEgq18WxD_1q8FiE"
PROJECT = "grimspire-9cf6a"


def req(url, data=None, tok=None):
    headers = {"Content-Type": "application/json"}
    if tok:
        headers["Authorization"] = "Bearer " + tok
    body = json.dumps(data).encode() if data is not None else None
    return json.load(urllib.request.urlopen(urllib.request.Request(url, data=body, headers=headers), timeout=15))


def val(v):
    k = next(iter(v)); x = v[k]
    return int(x) if k == "integerValue" else float(x) if k == "doubleValue" else x


def main():
    since = int(sys.argv[sys.argv.index("--since") + 1]) if "--since" in sys.argv else 0
    tok = req(f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={KEY}", {"returnSecureToken": True})["idToken"]
    out, page = [], None
    while True:
        u = f"https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)/documents/reports?pageSize=300"
        if page:
            u += "&pageToken=" + page
        d = req(u, tok=tok)
        for doc in d.get("documents", []):
            f = {k: val(v) for k, v in doc.get("fields", {}).items()}
            f["id"] = doc["name"].split("/")[-1]
            out.append(f)
        page = d.get("nextPageToken")
        if not page:
            break
    out = [r for r in out if r.get("at", 0) > since]
    out.sort(key=lambda r: r.get("at", 0))
    items = [{"id": r["id"], "type": r.get("kind", "Bug"), "dev": r.get("dev", ""), "title": r.get("title", ""),
              "body": r.get("body", ""), "who": r.get("who", ""), "ver": r.get("ver", ""), "at": r.get("at", 0)} for r in out]
    json.dump(items, sys.stdout, indent=1)
    print()


if __name__ == "__main__":
    main()
