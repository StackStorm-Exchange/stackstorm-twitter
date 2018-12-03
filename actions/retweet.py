from twitter import Twitter
from twitter import OAuth
from twython import Twython

import base64
import requests
import os
import StringIO

from st2common.runners.base_action import Action

# 1 MB chunks
DOWNLOAD_CHUNK_SIZE_BYTES = 1 * 1024 * 1024

__all__ = [
    'UpdateStatusAction'
]


class UpdateStatusAction(Action):

    def download_url(self, url):
        data_buffer = StringIO.StringIO()
        req = requests.get(url, stream=True)
        for chunk in req.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE_BYTES):
            data_buffer.write(chunk)
        return data_buffer.getvalue()

    def read_path_or_url(self, path_or_url):
        # If path_or_url is a URL, then download the file
        # Else create a file object for the given path
        if path_or_url.startswith('http'):
            data = self.download_url(path_or_url)
        else:
            with open(os.path.realpath(path_or_url), 'rb') as f:
                data = f.read()
        return data

    def run(self, tweet_id, accounts=[]):

        rt_accounts = []

        # Iterate over provided list of accounts to retweet from
        for account in accounts:

            # Iterate over accounts in config, making sure the requested account exists
            for config_account in self.config['accounts']:
                if config_account['name'] == account:
                    rt_accounts.append(
                        {
                            "consumer_key": config_account['consumer_key'],
                            "consumer_secret": config_account['consumer_secret'],
                            "access_token": config_account['access_token'],
                            "access_token_secret": config_account['access_token_secret']
                        }
                    )
                    break
            else:
                raise Exception("Unable to find referenced account in config")
    
        # Iterate over final list and retweet from each account
        for account in rt_accounts:
            auth = OAuth(
                token=account['access_token'],
                token_secret=account['access_token_secret'],
                consumer_key=account['consumer_key'],
                consumer_secret=account['consumer_secret']
            )
            client = Twitter(auth=auth)
            client.statuses.retweet(id=tweet_id)

        return True
