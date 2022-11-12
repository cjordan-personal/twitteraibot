# Twitter AI Bot
## Summary
Twitter bot that will respond to mentions, reply to threads using OpenAI's GPT-3.  Note that this is a "passive" bot that does not Tweet unsolicedly.

The example case given is [@BallparkExplore](https://twitter.com/BallparkExplore/with_replies) - a travel blogger that visits Major League Baseball parks (and surrounding cities) to take in the local culture, providing commentary and suggestions.
## Service Configuration
- Twitter:
  - From a valid Twitter account, sign up for a Developer account - ensuring a valid email is linked to the account.
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
