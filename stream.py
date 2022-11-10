import os
import tweepy
import twitter

class TweetHandler(tweepy.StreamingClient):
# Subclass of StreamingClient, main function is passing the tweet object to the provided callback when data is received.
    def __init__(self, bearer_token, bot_handle, callback):
        super().__init__(bearer_token, wait_on_rate_limit=True)
        self.bot_id = twitter.id_from_twitter_handle(bot_handle)
        self.callback = callback

    def on_tweet(self, tweet):
        if tweet.author_id != self.bot_id:
            self.callback(tweet)

    def on_connection_error(self):
        # Moving connection errors (which are frequent with v2 API) to custom handling - TBI.
        pass

    def on_request_error(self, status_code):
        # Invokes, but still prints the error response text - backend is handled, it's just chatty.
        pass

def stream_tweets(bot_handle, callback):
# Streaming consumer, will watch for mentions/messages to bot_handle and pass tweet object to callback.
    bearer_token = os.environ["TWITTER_BEARER_TOKEN"]

    client = TweetHandler(bearer_token, bot_handle=bot_handle, callback=callback)

    # Clear old rules (Twitter API leaves all previous rules in place, causes connection errors).
    previous_rules = client.get_rules().data
    if previous_rules:
        client.delete_rules(previous_rules)
    rule = tweepy.StreamRule(value=bot_handle)

    client.add_rules(rule)
    client.filter(expansions="author_id", tweet_fields="created_at", threaded=False)