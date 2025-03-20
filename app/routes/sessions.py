from flask import jsonify, request
from datetime import datetime, timezone

from app.models import SessionQuestion, Session, Destination, Question


def get_session(session_id):
    user_id = request.user_id

    session = Session.find_session(session_id)
    if not session:
        return (
            jsonify(
                {"session": None, "error": "session does not exists"}
            ),
            404,
        )
    if session.user_id != user_id:
        return (
            jsonify(
                {"session": None, "error": "session does not belog to user"}
            ),
            403,
        )

    return jsonify({"session": session.to_dict(), "error": None}), 200

def increment_current_question(session_id):
    user_id = request.user_id

    session = Session.find_session(session_id)
    if not session:
        return (
            jsonify(
                {"session": None, "error": "session does not exists"}
            ),
            404,
        )
    if session.user_id != user_id:
        return (
            jsonify(
                {"session": None, "error": "session does not belog to user"}
            ),
            403,
        )
    
    if session.current_question >= 10:
        return (
            jsonify(
                {"session": None, "error": "session already completed"}
            ),
            400,
        )
    
    if session.current_question == 9:
        session.completed_at = datetime.now(timezone.utc)

    session.current_question += 1

    session.save()

    #mvcc

    return jsonify({"session": session.to_dict(), "error": None}), 200


def create_session():
    user_id = request.user_id

    session = Session.find_ongoing_session(user_id)
    if session:
        return jsonify({"session": session.to_dict(), "error": None}), 200

    session = Session(user_id=user_id)
    session.save()

    destinations = Destination.get_random_destinations(limit=10)

    questions = []
    for d in destinations:
        q = Question(user_id=user_id, destination_id=d.id)
        q.save()
        questions.append(q)
    
    o = 1
    for q in questions:
        session_q = SessionQuestion(session_id=session.id, question_id=q.id, order=o)
        session_q.save()
        o += 1

    return jsonify({"session": session.to_dict(), "error": None}), 200

def get_session_question(session_id, ord):

    question = SessionQuestion.find_session_question(int(ord), session_id)
    if not question:
        return (
            jsonify(
                {"question": None, "error": "question does not exists"}
            ),
            404,
        )
    
    q = {
            "id": question.id,
            "user_id": question.user_id,
            "hint_taken": question.hint_taken,
            "option_selected": question.option_selected,
            "points": question.points,
            "created_at": question.created_at,
        }

    return jsonify({"question": q, "error": None}), 200


