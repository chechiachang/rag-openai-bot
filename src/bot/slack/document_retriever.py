import secrets

emoji_mapping = {
    1: ":one:",
    2: ":two:",
    3: ":three:",
    4: ":four:",
    5: ":five:",
}

class DocumentRetrieverTemplate:
    def __init__(self):
        self.user_id = "dummy_user"
        self.title = "dummy title"

    def set_user(self, user_id):
        self.user_id = user_id

    def set_title(self, title):
        self.title = title

    def attachements(self, prediction):
        return [
            {
                "fallback": "Plain-text summary of the attachment.",
                "color": "#" + secrets.token_hex(3),
                "blocks": self.blocks(prediction),
            }
        ]

    def blocks(self, prediction):
        result = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": (self.title[:147] + '..') if len(self.title) > 150 else self.title,
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Asked by <@{self.user_id}>"
                }
            }
        ]
        for idx, answer in enumerate(prediction['answers']):
            result.append(
                {
                    "type": "divider"
                }
            )
            result.append(
                {
                    "type": "section",
                    "text": {
                    "type": "mrkdwn",
                    "text": emoji_mapping[idx+1] +
                    f" *{answer.answer}*\n {answer.context} \n _score:{answer.score:f}_"
                },
                    #"accessory": {
                    #	"type": "button",
                    #	"text": {
                    #		"type": "plain_text",
                    #		"emoji": True,
                    #		"text": "Vote"
                    #	},
                    #	"value": "click_me_123"
                    #}
                }
            )
        return result
