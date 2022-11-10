from ai import AIBot
import _init.ballparkexplore
import os
import stream
import tweepy
import twitter

client = tweepy.Client(consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
                       consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
                       access_token=os.environ["TWITTER_ACCESS_TOKEN"],
                       access_token_secret=os.environ["TWITTER_ACCESS_SECRET"])

def respond_to_tweet(tweet):
# Callback function for stream/streamingclient, for generality.
    tweet_text = twitter.strip_sender_from_replies(tweet.text)
    tweet_id = tweet.id
    tweet_sender_handle = twitter.twitter_handle_from_id(tweet.author_id)

    tweet_history = twitter.twitter_chat_history_from_id(tweet_id, bot_handle=bot_handle, participant_handle=tweet_sender_handle)
    tweet_history = twitter.append_tweet_history(tweet_history, tweet_sender_handle=tweet_sender_handle, tweet_text=tweet_text)

    # Custom (but not necessary) conditional, uses the AI seed values for short conversations.
    use_seed_thread = False
    if tweet_history.count("\n") < 5:
        use_seed_thread = True

    print("* Data received: " + str(tweet_id) + "/" + tweet_sender_handle + "/" + tweet_text +".")
    ai = AIBot(bot_handle=bot_handle, participant_handle=tweet_sender_handle, conversation_thread=tweet_history, use_seed_thread=use_seed_thread)
    response = ai.response_completion()
    print(twitter.reply_to_tweet(tweet_text=response, reply_id=tweet_id))


bot_handle = os.environ["TWITTER_HANDLE"]
twitter_stream = stream.stream_tweets(bot_handle=bot_handle, callback=respond_to_tweet)