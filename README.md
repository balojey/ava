# Ava

[Live app]()

[Project Writeup](https://peaceful-sleep-735.notion.site/Ava-Empowering-SUI-MOVE-Developers-An-AI-Chat-App-Leveraging-Atlas-MongoDB-1223f4d8a27d48dd81ca281b328a1282?pvs=4)

Ava is a GPT chat model perfectly geered towards Sui/Move developers due to lack of AI support in the domain.

Just like ChatGPT, but for Sui.

## Technologies

This application was brought to life using the following technologies

1. Atlas MongoDB
2. Llama Index
3. Llama API
4. Flet

## Setup

*Option 1*

Use Gitpod: go to [https://gitpod/#https://github.com/balojey/ava](https://gitpod/#https://github.com/balojey/ava)

All dependencies will be installed automatically

*Option 2*

Clone this repo: `git clone https://github.com/balojey/ava`

Then, install dependencies: `poetry install`

## Run Ava

Populate your environment variables

```
    ATLAS_URI=
    LLAMA_API_KEY=
    GITHUB_CLIENT_ID=
    GITHUB_CLIENT_SECRET=
    CHAT_DB_NAME=
    CHAT_COLLECTION_NAME=
```

Then, run: `poetry shell ; flet run -wr ava/ava_ui/main.py`