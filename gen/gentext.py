import requests, base64
invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
stream = False
from gen.tts import begin as tts_begin

def read_b64(path):
  with open(path, "rb") as f:
    return base64.b64encode(f.read()).decode()

def saveResponse(headers, payload):
    response = requests.post(invoke_url, headers=headers, json=payload, stream=stream)
    if stream:
        for line in response.iter_lines():
            if line:
                print(line.decode("utf-8"))
    else:
        print(response.json())
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
                    "You are to generate an entertaining reddit AITA story. " +
                    "Make it as believable or unbelievable as you want. " +
                    "However, you must follow some specific rules. "
                    "First: You must NOT generate a title or original poster. " +
                    "Second: You are to denote when the story starts by saying \"STORY_BEGIN\" exactly as typed." +
                    "Third: You do not have to include post comments, but you can. If you do, you must first list " +
                    "the user (i.e \"u/exampleusername\"), and then the comment" +
                    "You must denote when the FIRST comment starts by saying \"COMMENT_BEGIN\" exactly as I have."}],
    "max_tokens": 16384,
    "temperature": 0.60,
    "top_p": 0.95,
    "stream": stream,
    "chat_template_kwargs": {"enable_thinking":True},
    }
   saveResponse(headers, payload)
   next(NIVIDA_API_KEY)

