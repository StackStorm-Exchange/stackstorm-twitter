import base64
import os
import requests
from six.moves import StringIO

from twitter import Twitter
from twitter import OAuth
from twython import Twython


from st2common.runners.base_action import Action

# 1 MB chunks
DOWNLOAD_CHUNK_SIZE_BYTES = 1 * 1024 * 1024

__all__ = [
    'UpdateStatusAction'
]


class UpdateStatusAction(Action):

    def download_url(self, url):
        data_buffer = StringIO()
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

    def run(self, status, media):
        if media:
            # use twython.Twython for media updates
            # twitter.Twitter has a bug that prevents media from being uploaded
            client = Twython(self.config['consumer_key'],
                             self.config['consumer_secret'],
                             self.config['access_token'],
                             self.config['access_token_secret'])
            media_ids = []
            for m in media:
                # get data for media path (or download of it's a url)
                raw_data = self.read_path_or_url(m)
                # convert to base64
                b64_data = base64.b64encode(raw_data)
                # upload to twitter using media_data field that expects
                # base64 encoded
                response = client.upload_media(media_data=b64_data)
                media_ids.append(response['media_id'])

            # send tweet with uploaded media
            client.update_status(status=status, media_ids=media_ids)
        else:
            # use twitter.Twitter for regular status updates
            auth = OAuth(
                token=self.config['access_token'],
                token_secret=self.config['access_token_secret'],
                consumer_key=self.config['consumer_key'],
                consumer_secret=self.config['consumer_secret']
            )
            client = Twitter(auth=auth)
            client.statuses.update(status=status)

        return True
