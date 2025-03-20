import logging
from functools import wraps

from flask import Blueprint

from app.jwt import token_required
from app.routes import auths, questions, users, sessions


# Initialize the Blueprint for user-related users
main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__, url_prefix="/auth")
question = Blueprint("question", __name__, url_prefix="/question")
user = Blueprint("user", __name__, url_prefix="/user")
session = Blueprint("session", __name__, url_prefix="/session")


# Error handler for all routes
def handle_exception(controller):
    @wraps(controller)
    def wrapper(*args, **kwargs):
        try:
            return controller(*args, **kwargs)
        except Exception as e:
            logging.error(e)
            return {"error": "Internal server error"}, 500

    return wrapper


# Register each route to the main blueprint
main.add_url_rule(
    "/", view_func=lambda: "Welcome to the Globetrotter API", methods=["GET"]
)


# Register each route to the auth blueprint
auth.add_url_rule("", view_func=handle_exception(auths.signup), methods=["POST"])
auth.add_url_rule("/loader", view_func=handle_exception(auths.loader), methods=["GET"])


# Register each route to the movie blueprint
question.add_url_rule(
    "",
    view_func=handle_exception(token_required(questions.get_question, optional=True)),
    methods=["GET"],
)
question.add_url_rule(
    "/answer",
    view_func=handle_exception(
        token_required(questions.answer_question, optional=True)
    ),
    methods=["POST"],
)
question.add_url_rule(
    "/hint",
    view_func=handle_exception(token_required(questions.take_hint, optional=True)),
    methods=["POST"],
)


# Register each route to the user blueprint
user.add_url_rule(
    "/<string:user_id>",
    view_func=handle_exception(token_required(users.get_user, optional=True)),
    methods=["GET"],
)
user.add_url_rule(
    "/challenger/<string:uri>",
    view_func=handle_exception(users.get_linked_user),
    methods=["GET"],
)
user.add_url_rule(
    "/challenges",
    view_func=handle_exception(token_required(users.create_challenge)),
    methods=["POST"],
)
user.add_url_rule(
    "/challenges/<string:uri>",
    view_func=handle_exception(users.challenge_page),
    methods=["GET"],
)
user.add_url_rule(
    "/dynamic-images/<string:challenge_id>.png",
    view_func=handle_exception(users.generate_image),
    methods=["GET"],
)


session.add_url_rule(
    "/<string:session_id>",
    view_func=handle_exception(token_required(sessions.get_session)),
    methods=["GET"],
)
session.add_url_rule(
    "/",
    view_func=handle_exception(token_required(sessions.create_session)),
    methods=["POST"],
)
session.add_url_rule(
    "/<string:session_id>/question/<string:ord>",
    view_func=handle_exception(token_required(sessions.get_session_question)),
    methods=["GET"],
)
session.add_url_rule(
    "/<string:session_id>",
    view_func=handle_exception(token_required(sessions.increment_current_question)),
    methods=["PUT"],
)

