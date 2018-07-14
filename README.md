# Twitter Integration Pack

Pack which allows integration with Twitter.

## Use cases

* [HOWTO: Broadcast Twitter mentions about your Company to Slack channel](http://stackstorm.com/2014/12/22/monitor-twitter-and-fire-automations-based-on-twitter-keywords-using-stackstorm/)

## Configuration

Copy the example configuration in [twitter.yaml.example](./twitter.yaml.example)
to `/opt/stackstorm/configs/twitter.yaml` and edit as required.

It should contain:

* ``consumer_key`` - Twitter API consumer key.
* ``consumer_secret`` - Twitter API consumer secret.
* ``access_token`` - Twitter API access token.
* ``access_token_secret`` - Twitter API access token secret.
* ``query`` - A query to search the twitter timeline for. Must be an array.
  By default OR is applied for array items, and you can refine your results
  further via rule criteria.
  You can use all the query operators described at https://dev.twitter.com/rest/public/search
* ``count`` - Number of latest tweets matching the criteria to retrieve.
  Defaults to 30, maximum is 100.
* ``language`` - If specified, only return tweets in the provided language.
  For example: `en`, `de`, `jp`, etc.

You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`

### Obtaining API credentials

To obtain API credentials, you need to first register your application on the
[Twitter Application Management](https://apps.twitter.com/) page.

![Step 1](/etc/twitter_create_app.png)

After you have done that, go to the `Keys and Access Tokens` tab where you can
find your consumer key and secret. On the same page you can also generate an
access token (click on the ``Create my access token`` button).

![Step 2](/etc/twitter_obtain_consumer_key.png)

For the sensor a "Read only" token is sufficient, but for the action you need
to use a token with a "Read and Write" access.

![Step 3](/etc/twitter_create_access_token.png)

![Step 4](/etc/twitter_obtain_access_token.png)

## Sensors

### TwitterSearchSensor

This sensor searches Twitter for recent tweets matching the criteria defined in
the config. When a matching Tweet is found, a trigger is dispatched.

## Actions

* ``update_status`` - Action which updates your status / posts a new tweet.
* ``direct_message`` - Action to direct message a user.
* ``follow`` - Action to follow a user.

### Updating Status with Media (Pictures)

The ``update_status`` action supports uploading of media (pictures specifically)
along with your textual status update. This is accomplished by passing
either the path to a local file, or a ``http/s`` URL to the ``media`` parameter.
``media`` is an ``array`` and can be used to uploaded multiple media in a single
tweet.

Example(s):

``` shell
# upload a single image from the filesystem
st2 run twitter.update_status status="Check out my local file" media=

# upload a single image from a URL
st2 run twitter.update_status status="Check out this picutre on the internet" media="https://apod.nasa.gov/apod/image/1806/_SSH1593jsm1024.jpg"

# upload multiple images
st2 run twitter.update_status status="Check out these pics" media='["/opt/data/picture.png", "https://apod.nasa.gov/apod/image/1806/_SSH1593jsm1024.jpg"]'
```

## Rules

### relay_tweet_to_slack

Rule which shows how to relay every matched tweet to the Slack channel.
