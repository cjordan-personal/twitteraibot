# Twitter GPT-3 AI Bot
## Summary
Twitter bot that will respond to mentions, reply to threads using OpenAI's GPT-3.  Note that this is a "passive" bot that does not Tweet unsolicedly.  Uses **tweepy**, **openai** modules.

The example case given is [@BallparkExplore](https://twitter.com/BallparkExplore/with_replies) - a travel blogger that visits Major League Baseball parks (and surrounding cities) to take in the local culture, providing commentary and suggestions.
## Service Configuration
- Twitter:
  - From a valid Twitter account, sign up for a Developer account - ensuring a valid email is linked to the account.  (Note that only an Essential tier account is required, as this application using the Twitter v2 API).
  - Make note of the:
    - **API (Consumer) Key**
    - **API (Consumer) Secret**
    - **Bearer Token**
  - Go to your Project from the Developer Console, and change the permissions to **Read and write** (or **Read and write and Direct message**, if you prefer).
  - From your Project, click the **Keys and tokens** tab, then **Generate Access Token and Secret**.
  - Make note of the:
    - **Access Token**
    - **Access Token Secret**
- OpenAI:
  - Create an OpenAI API key, making note of it.
## Application Setup
- For authentication, with the keys noted above, either:
  - Update **/_init/{{bot_handle}}/__init__.py** with key information - (Not recommended) Simple, but insecure; or
  - Set environment variables locally, or within your deployment/containerization/key management tool of choice (Docker, k8s, etc.)
- Create a "persona" for your bot within **/settings/{{bot_handle}}/ai.py**, updating the bot object's **overview** and **seed** values, per below.
## Personas
A "persona" is what we provide the OpenAI GPT-3 API to give context on the bot's purpose, motivations, likes, dislikes, along with a history of the conversation (if one exists).  The **overview** value provides broader information on the bot; the **seed** acts as a starting point to direct the conversation - used where a thread is just starting.  

Note that we also include the full conversation thread history to provide relevant data, ensure replies are context sensitive.  Placeholders are used for generality.  Example:

**overview**:
```
XXREPLACEBOTHANDLEXX is a chatbot from Toronto, Ontario who has made a career visiting Major League Baseball parks (and the surrounding cities) across the United States.
They have a blog and YouTube channel where they post content about the best restaurants and places to visit in these baseball cities.
They love classic pub food, learning about the culture of American cities, and are huge Toronto Blue Jays fans - but love watching baseball, no matter the teams!
```

**seed**:
```
XXREPLACESENDERHANDLEXX: How did you like the game in Boston?
XXREPLACEBOTHANDLEXX: It was a heck of game and you always feel like you're part of history being in Fenway.  I can't believe the Jays lost by 1 though... so close!
XXREPLACESENDERHANDLEXX: What do you recommend for food after a game there?
XXREPLACEBOTHANDLEXX: I love going to Faneuil Hall every time I visit Boston - it's so vibrant.  We checked out The Black Rose and tried the burger.  Definitely recommend!
```

## Release Notes
- tweepy's StreamingClient connect handling is not perfect, will occasionally generate "TooManyConnection" (429) errors.  We handle as best we can by clearing StreamRule on each run; though you may experience, particularly with "chatty" conversation threads.
