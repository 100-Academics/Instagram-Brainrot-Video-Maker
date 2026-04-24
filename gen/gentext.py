import requests, base64
import json
import re

invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
stream = False
from gen.tts import begin as tts_begin

def read_b64(path):
  with open(path, "rb") as f:
    return base64.b64encode(f.read()).decode()

def cleanFile():
    with open("response.txt", "r") as f:
        content = f.read()
        cleaned_content = re.sub(r'\n{2,}', '\n', content)

    with open("response.txt", "w") as f:
        f.write(cleaned_content)

def saveResponse(headers, payload):
    response = requests.post(invoke_url, headers=headers, json=payload, stream=stream)
    stillGoing = True
    while(stillGoing):
        if response.status_code != 200:
            print("Error: " + str(response.status_code) + " - " + response.text)
            break

        if stream:
            for line in response.iter_lines():
                if line:
                    print(line.decode("utf-8"))
        else:
            print(response.json())
            stillGoing = False
            break
        
    
    response_data = response.json()
    with open("response.txt", "w") as f:
        with open("response.json", "w") as j:
            data = response_data["choices"][0]["message"]["content"]
            cleaned_data = re.sub(r'\n{2,}', '\n', data)
            f.write(cleaned_data)
            json.dump(response_data, j)

def next(NVIDIA_API_KEY):
    tts_begin(NVIDIA_API_KEY)


def run(NVIDIA_API_KEY):
   headers = {
  "Authorization": f"Bearer {NVIDIA_API_KEY}",
  "Accept": "text/event-stream" if stream else "application/json"
   }

   payload = {
    "model": "qwen/qwen3.5-122b-a10b",
    "messages": [{"role":"user","content":
                    "Follow these instructions carefully: " +
                    "You are to generate an entertaining Reddit Am I the Asshole (AITA) story. " +
                    "Make it as believable or unbelievable as you want, be sure to make it unique. " +
                    "It must remain grounded in realism, however. " +
                    "That is not say, nothing supernatural, for example. It should be a tad extreme. " +
                    "However, you MUST follow some specific rules: \n " +
                    "First: You must NOT generate a title or original poster. \n" +
                    "Second: You are to denote when the story starts by saying \"STORY_BEGIN\" exactly as typed.\n" +
                    "Third: You do not have to include post comments, but you can. If you do, you must first list " +
                    "the user (i.e \"u/exampleusername\"), and then the comment. " + 
                    "You MUST come up with convincing usernames for the commentors, something that sounds real. " +
                    "The comments must also be realistic.\n" +
                    "Fourth: You must denote when the FIRST comment starts by saying \"COMMENT_BEGIN\" exactly as I have. \n\n" +
                    "Now please generate the story following the above instructions. " +
                    "Remember to follow the instructions carefully and to denote the " +
                    "beginning of the story and comments as specified."
                    }],
    "max_tokens": 16384,
    "temperature": 0.60,
    "top_p": 0.95,
    "stream": stream,
    "chat_template_kwargs": {"enable_thinking":False},
    }
   print("Generating story...")
   saveResponse(headers, payload)
   print("Done generating story. Moving on to TTS...")
   next(NVIDIA_API_KEY)

