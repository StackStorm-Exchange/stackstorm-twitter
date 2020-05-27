from twitter import Twitter
from twitter import OAuth

from lib import get_twitter_tokens
from st2common.runners.base_action import Action

__all__ = [
    'FollowAction'
]


class FollowAction(Action):
    def run(self, screen_name, account=""):
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
        client.friendships.create(screen_name=screen_name)

        return True
