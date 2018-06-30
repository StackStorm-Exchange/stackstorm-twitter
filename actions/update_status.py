from tempfile import NamedTemporaryFile
from twitter import Twitter
from twitter import OAuth

import requests

from st2common.runners.base_action import Action

# 1 MB chunks
DOWNLOAD_CHUNK_SIZE_BYTES = 1 * 1024 * 1024

__all__ = [
    'UpdateStatusAction'
]


class UpdateStatusAction(Action):

    def http_url_to_file(http_url):
        data_file = NamedTemporaryFile()
        req = requests.get(http, stream=True)
        for chunk in req.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE_BYTES):
            data_file.write(chunk)
        return data_file

    def read_media_file_or_url(media_path_or_url):
        # If media_path_or_url is a URL, then download the file
        # Else create a file object for the given path
        if passed_media.startswith('http'):
            data_file = http_url_to_file(media_path_or_url)
        else:
            data_file = open(os.path.realpath(media_path_or_url), 'rb')
        return data_file.read()

    def run(self, status, media):
        auth = OAuth(
            token=self.config['access_token'],
            token_secret=self.config['access_token_secret'],
            consumer_key=self.config['consumer_key'],
            consumer_secret=self.config['consumer_secret']
        )
        client = Twitter(auth=auth)

        if media:
            media_ids = []
            for m in media:
                imagedata = read_media_file_or_url(m)
                m_id = t_upload.media.upload(media=imagedata)["media_id_string"]
                media_ids.append(m_id)

            # - finally send tweet with the list of media ids:
            client.statuses.update(status=status, media_ids=",".join(media_ids))
        else:
            client.statuses.update(status=status)

        return True
