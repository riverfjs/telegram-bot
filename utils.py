import os
import json
import configparser
import openai
import googleapiclient.discovery
import googleapiclient.errors

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

def test(text):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    developerKey = config["YOUTUBE"]["DEVELOPER_KEY"]

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=developerKey)
    request = youtube.search().list(
        part="snippet",
        q=text,
    )
    response = request.execute()
    try:
        print("https://youtube.com/v/" + response["items"][0]["id"]["videoId"])
        return "https://youtube.com/v/" + response["items"][0]["id"]["videoId"]
    except Exception:
        return "换个关键词吧！"

def chat(text):
    openai.api_key = config["OPENAI"]["KEY"]
    try:
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0.5,
        max_tokens=1200,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        # stop=["You:"]
        )
        return response["choices"][0]["text"]
    except Exception:
        return "换个问题吧！"
    
    print(response)
if __name__ == "__main__":
    # test("nb")
    chat()