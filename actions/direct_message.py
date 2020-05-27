from twitter import Twitter
from twitter import OAuth

from lib import get_twitter_tokens
from st2common.runners.base_action import Action

__all__ = [
    'DirectMessageAction'
]


class DirectMessageAction(Action):
    def run(self, screen_name, message, account=""):

        consumer_key, consumer_secret, access_token, access_token_secret = get_twitter_tokens(
            self.config, account
        )

        auth = OAuth(
            token=access_token,
            token_secret=access_token_secret,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret
        )
        client = Twitter(auth=auth)
        client.direct_messages.new(user=screen_name, text=message)

        return True
