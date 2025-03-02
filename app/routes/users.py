from flask import jsonify, request, send_file, render_template
from PIL import Image, ImageDraw, ImageFont

from app.models import Question, Link, User
from app.config import Config

URL = Config.URL
FRONTEND_URL = Config.FRONTEND_URL


def get_user(user_id=None):
    if user_id == "me":
        user_id = request.user_id
        if not user_id:
            return jsonify({"user": None, "error": "User not found"}), 404

    user = User.get_user(user_id)
    score = Question.get_user_score(user_id)

    user = user.to_dict()
    user["score"] = score

    return jsonify({"user": user, "error": None}), 200


def get_linked_user(uri):
    links = Link.get_uri_link(uri)

    return jsonify({"user_id": links.user_id, "error": None}), 200


def create_challenge():
    user_id = request.user_id

    link = Link.get_user_link(user_id)
    if link:
        return jsonify({"uri": link.uri, "error": None}), 200

    link = Link(user_id=user_id, uri=Link.generate_uri())
    link.save()

    return jsonify({"uri": link.uri, "error": None}), 200


def challenge_page(uri):
    invite_image = f"{URL}/dynamic-images/{uri}.png"

    return render_template(
        "challenge.html",
        URL=URL,
        FRONTEND_URL=FRONTEND_URL,
        uri=uri,
        invite_image=invite_image,
    )


def generate_image(challenge_id):
    img = Image.new("RGB", (600, 300), color=(73, 109, 137))
    draw = ImageDraw.Draw(img)

    font = ImageFont.load_default()
    draw.text(
        (50, 120), f"Challenge ID: {challenge_id}", fill=(255, 255, 255), font=font
    )

    img_path = f"./app/data/temp_{challenge_id}.png"
    img.save(img_path)

    return send_file(f"./data/temp_{challenge_id}.png", mimetype="image/png")
