from flask import jsonify, request

from random import shuffle

from app.models import Question, Destination


def get_question():
    user_id = request.user_id

    question = None
    if user_id:
        question = Question.get_unanswered_question(user_id)

    if question:
        destination = Destination.get_destination(question.destination_id)
        if not destination:
            return jsonify({"question": None, "error": "Destination not found"}), 404

        destinations = Destination.get_random_destinations(
            destination_id=question.destination_id, limit=3
        )

        destinations.append(destination)
    else:
        destinations = Destination.get_random_destinations(limit=4)
        question = Question(user_id=user_id, destination_id=destinations[-1].id)
        question.save()

    full_question = question.to_dict()

    full_question["clue"] = destinations[-1].clue_1

    shuffle(destinations)
    full_question["options"] = [dest.city for dest in destinations]

    return jsonify({"question": full_question, "error": None}), 200


def answer_question():
    user_id = request.user_id
    question_id = request.json.get("question_id")
    option = request.json.get("option")

    question = Question.get_question(question_id)
    if not question:
        return (
            jsonify(
                {"question": None, "error": "Question not found or already answered"}
            ),
            404,
        )
    if user_id and question.user_id != user_id:
        return (
            jsonify({"question": None, "error": "Question does not belong to user"}),
            400,
        )
    if question.option_selected:
        return jsonify({"question": None, "error": "Question already answered"}), 400

    destination = Destination.get_destination(question.destination_id)
    if not destination:
        return jsonify({"question": None, "error": "Destination not found"}), 404

    question.option_selected = option

    if destination.city.lower() == option.lower():
        question.points = 3
        if not question.hint_taken:
            question.points += 2

    question.save()

    data = {
        "points": question.points,
        "is_correct": question.points > 0,
        "destination": destination.to_dict(),
        "error": None,
    }

    return jsonify({"data": data, "error": None}), 200


def take_hint():
    user_id = request.user_id
    question_id = request.json.get("question_id")

    question = Question.get_question(question_id)
    if not question:
        return jsonify({"question": None, "error": "Question not found"}), 404
    if user_id and question.user_id != user_id:
        return (
            jsonify({"question": None, "error": "Question does not belong to user"}),
            400,
        )
    if question.option_selected:
        return jsonify({"question": None, "error": "Question already answered"}), 400

    destination = Destination.get_destination(question.destination_id)
    if not destination:
        return jsonify({"question": None, "error": "Destination not found"}), 404

    if not question.hint_taken:
        question.hint_taken = True
        question.save()

    return jsonify({"clue": destination.clue_2, "error": None}), 200
