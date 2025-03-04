from telegram import Update


def get_message_text(update: Update, include_reply_to_message: bool = True) -> str:
    message = update.message
    if not message:
        return ""

    message_text = message.text or ""
    message_text = strip_command(message_text)
    if not include_reply_to_message:
        return message_text

    reply_text = message.reply_to_message.text if message.reply_to_message and message.reply_to_message.text else ""

    return f"{reply_text}\n{message_text}" if reply_text else message_text

def strip_command(text: str) -> str:
    """Remove the command from the text.
    For example:
    Input: "/sum 1 2 3"
    Output: "1 2 3"

    Input: "hello"
    Output: "hello"
    """
    if text.startswith("/"):
        command, *args = text.split(" ", 1)
        return args[0] if args else ""
    return text

