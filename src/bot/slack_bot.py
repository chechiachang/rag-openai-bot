
import os

from dotenv import find_dotenv
from dotenv import load_dotenv
from loguru import logger
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from .conversational_retrieval_agent import ConversationalRetrievalAgent
from .slack_template import DocumentRetrieverTemplate

load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))
k8s_bot = ConversationalRetrievalAgent(
    collection_name=os.environ["QDRANT_COLLECTION_NAME_K8S"]
)

# slack
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    #signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

def start_bot():

    k8s_bot.setup_bot()

    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

@app.command("/k8s")
def document_retrieve(ack, respond, command, say):
    ack()
    question = command['text']
    answer = k8s_bot.ask_question(question)

    logger.info(answer)

    template = DocumentRetrieverTemplate()
    template.set_title(question)
    template.set_user(command['user_name'])
    say(
        attachments = template.attachments(answer),
        text = "" # placeholder
    )

@app.command("/quip")
def answer_question_from_quip(ack, respond, command, say):
    ack()
    question = command['text']
    answer = k8s_bot.ask_question(question)

    logger.info(answer)

    # TODO: template
    say(
        text = answer
    )

@app.event("reaction_added")
def update_emoji(event, say):
    """Update the onboarding welcome message after receiving a "reaction_added"
    event from Slack. Update timestamp for welcome message as well.
    """
    # Get the ids of the Slack user and channel associated with the incoming event
    event.get("item", {}).get("channel")
    event.get("user")
    reaction = event["reaction"]

    logger.info(event)

    reaction = event["reaction"]

    if reaction == "scroll":
        # TODO
        say("scroll")

    elif reaction == "question":
        # TODO mark the question task
        say("question")

    elif reaction == "raising_hand":
        # TODO mark the anwser
        say("raising_hand")

    # Post the message in Slack
    #updated_message = client.chat_update(**message)

@app.event({"type": "message"})
def message(event, say):
    user, text = event["user"], event["text"]
    logger.info(f"The user {user} send the message: {text}")

#@app.event({"type": "message", "subtype": "message_replied"})
#def message_replied(event, say):
#    user, text = event["user"], event["text"]
#    logger.info(f"The user {user} replied the message to {text}")
#
#@app.event({"type": "message", "subtype": "message_changed"})
#def log_message_change(logger, event):
#    user, text = event["user"], event["text"]
#    logger.info(f"The user {user} changed the message to {text}")

# ===WIP===

#@app.command("/learn")
#def faq_learn(ack, respond, command):
#    ack()
#    respond(f"{command['text']}")
#    text = command['text']
#
#    # TODO send text to llm
#    if text == "start":
#        respond(f"{command['text']}")
#
#@app.command("/answer")
#def faq_answer(ack, respond, command):
#    ack()
#    # TODO anwser the question with agent
#    if text == "start":
#        respond(f"{command['text']}")
#    else:
#        respond(f"I don't know what you mean by {command['text']}")
