import os
import openai
import re
import settings.ballparkexplore.ai as settings

def construct_basis(bot_handle, participant_handle, conversation_thread, use_seed_thread=False):
# Creates the basis text for GPT3.  If there's not enough history, uses the seed thread as a starting point.

    # Insert the bot handle into the general overview.
    overview = re.sub(r"XXREPLACEBOTHANDLEXX", bot_handle, settings.bot["overview"].rstrip())

    seed_thread = ""
    if use_seed_thread:
        seed_thread = re.sub(r"XXREPLACESENDERHANDLEXX", participant_handle, settings.bot["seed"])
        seed_thread = re.sub(r"XXREPLACEBOTHANDLEXX", bot_handle, seed_thread)
    return(overview + "\n" + seed_thread.rstrip() + "\n" + conversation_thread.rstrip() + "\n" + bot_handle + ": ")

def gpt_completion(texts):
# Returns AI's response to basis via GPT-3.
    openai.api_key = os.environ["OPENAI_KEY"]
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt = texts,
        temperature = 0.6,
        top_p = 1,
        max_tokens = 64,
        frequency_penalty = 0,
        presence_penalty = 0
    )
    return(response.choices[0].text)

class AIBot:
# Main object of AI.
    def __init__(self, bot_handle, participant_handle, conversation_thread, use_seed_thread=False):
        self.bot_handle = bot_handle
        self.participant_handle = participant_handle
        self.conversation_thread = conversation_thread
        self.use_seed_thread = use_seed_thread

    def response_completion(self):
    # Returns the AI's response based on the constructed basis.
        basis = construct_basis(bot_handle=self.bot_handle, participant_handle=self.participant_handle, conversation_thread=self.conversation_thread, use_seed_thread=self.use_seed_thread)
        return(gpt_completion(basis).lstrip())