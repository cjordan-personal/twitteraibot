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
TBI

## Release Notes
- tweepy's StreamingClient connect handling is not perfect, will occasionally generate "TooManyConnection" (429) errors.  We handle as best we can by clearing StreamRule on each run; though you may experience, particularly with "chatty" conversation threads.
