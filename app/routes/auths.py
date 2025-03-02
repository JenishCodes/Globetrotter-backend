from flask import jsonify, request

from app.models import User, Destination


def signup():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    user = User.get_username(username)
    if user and not user.check_password(password):
        return jsonify({"error": "Invalid password"}), 400
    if not user:
        user = User(username=username)
        user.hash_password(password)

        user.save()

    return jsonify({"token": user.get_token(), "error": None}), 200


def loader():
    import json

    with open("./app/data/data.json") as f:
        data = json.load(f)
        for dest in data:
            d = Destination(
                city=dest["city"],
                country=dest["country"],
                clue_1=dest["clues"][0],
                clue_2=dest["clues"][1],
                fun_fact_1=dest["fun_fact"][0],
                fun_fact_2=dest["fun_fact"][1],
                trivia_1=dest["trivia"][0],
                trivia_2=dest["trivia"][1],
            )
            d.save()
    return jsonify({"message": "Data loaded successfully"}), 200
