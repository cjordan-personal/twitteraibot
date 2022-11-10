import os
import re
import tweepy

client = tweepy.Client(consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
                       consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
                       access_token=os.environ["TWITTER_ACCESS_TOKEN"],
                       access_token_secret=os.environ["TWITTER_ACCESS_SECRET"])

def strip_sender_from_replies(tweet_fulltext):
# Nuance of StreamingClient - the sender handle is included in the fulltext, so we strip it.
    return(re.sub(r"^@[^\s]+\s+", "", tweet_fulltext))

def twitter_handle_from_id(id):
# Returns a Twitter handle, given an ID.
    client = tweepy.Client(bearer_token=os.environ["TWITTER_BEARER_TOKEN"])
    return("@" + client.get_user(id=id).data.username)

def id_from_twitter_handle(handle):
# Returns an ID, given a Twitter handle.
    client = tweepy.Client(bearer_token=os.environ["TWITTER_BEARER_TOKEN"])
    return(client.get_user(username=re.sub(r"^@", "", handle)).data.id)

def conversation_id_from_tweet(tweet_id):
# Returns the conversation ID given a tweet ID.
    client = tweepy.Client(bearer_token=os.environ["TWITTER_BEARER_TOKEN"])

    # A nuance of the API, get_tweet (singular) function won't return conversation ID - thus, get a list.
    test = client.get_tweets(ids=[tweet_id], tweet_fields=["conversation_id"])
    for t in test.data:
        return(t["conversation_id"])

def construct_conversation_dict(conversation_tweets):
# Parses a tweet list object from a query and returns a dictionary.
    conversation_dict = {}
    author_dict = {}
    for conversation_tweet in conversation_tweets:
        # To avoid making an API call for every handle, we build a dictionary as we go.
        if conversation_tweet.author_id not in author_dict.keys():
            author_dict[conversation_tweet.author_id] = twitter_handle_from_id(conversation_tweet.author_id)

        conversation_dict[conversation_tweet.created_at] = [author_dict[conversation_tweet.author_id],
                                                            conversation_tweet.text,
                                                            conversation_tweet.in_reply_to_user_id,
                                                            conversation_tweet.author_id]

    return(conversation_dict)

def chatify_tweet(conversation_line):
# Stringifies tweet objects into a "chat"-like format.
    return(conversation_line[0] + ": " + strip_sender_from_replies(conversation_line[1]) + "\n")

def twitter_chat_history_from_id(tweet_id, bot_handle, participant_handle=None, omit_self_replies=False):
# Given a tweet ID, returns a string with the full prior conversation related to said ID.
    client = tweepy.Client(bearer_token=os.environ["TWITTER_BEARER_TOKEN"])

    conversation_id = conversation_id_from_tweet(tweet_id)
    conversation_tweets = client.search_recent_tweets(query="conversation_id:" + str(conversation_id), tweet_fields=["created_at"], expansions=["author_id", "in_reply_to_user_id"], max_results=100).data
    if conversation_tweets is None:
        return(None)

    conversation_dict = construct_conversation_dict(conversation_tweets=conversation_tweets)

    bot_id = id_from_twitter_handle(bot_handle)
    participant_id = id_from_twitter_handle(participant_handle) if isinstance(participant_handle, str) else None

    # Construct a conversation (chat) string, given provided parameters and return.
    # Additional branching logic to be added, e.g. omitted self-replies NYI.
    chat_thread = ""
    for tweet_at in sorted(conversation_dict):
        # If participant_handle is given, assemble a two-way conversation.
        if isinstance(participant_handle, str):
            if conversation_dict[tweet_at][0] in [bot_handle, participant_handle]:
                chat_thread = chat_thread + chatify_tweet(conversation_line=conversation_dict[tweet_at])
        # Otherwise, include all participants in the conversation.
        else:
            chat_thread = chat_thread + chatify_tweet(conversation_line=conversation_dict[tweet_at])

    return(chat_thread)

def append_tweet_history(history, tweet_sender_handle, tweet_text):
# Append question/sender interaction to conversation thread (if one exists).
    if history is None:
        history = tweet_sender_handle + ": " + tweet_text + "\n"
    else:
        history = history.rstrip() + "\n" + tweet_sender_handle + ": " + tweet_text + "\n"
    return(history)

def reply_to_tweet(tweet_text, reply_id):
    client.create_tweet(text=tweet_text,in_reply_to_tweet_id=reply_id)
    return("\t** Tweeted \"" + tweet_text + "\" in reply to ID#: " + str(reply_id) + ".")