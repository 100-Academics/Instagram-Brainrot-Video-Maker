import asyncio
import sys
import edge_tts
from edge_tts import VoicesManager
import random

OUTPUT_FILE = "voice.mp3"
SRT_FILE = "voice.srt"
TEXT = ""
def begin(NVIDIA_API_KEY,): ## pass down API key in case we need it later.
    print("Beginning TTS generation...")
    with open ("response.txt", "r") as f:
        TEXT = f.read()
    asyncio.run(amain(str(TEXT)))

async def amain(TEXT) -> None:
    # drawn from 
    # https://github.com/rany2/edge-tts/blob/master/examples/sync_audio_streaming_with_predefined_voice_subtitles_print2stdout.py
    # https://github.com/rany2/edge-tts/blob/master/examples/async_audio_gen_with_dynamic_voice_selection.p
    print("Finding right voice...")
    voices = await VoicesManager.create()
    voice = voices.find(Gender = "Male", Language = "en")
    voice_for_tts = random.choice(voice)["Name"]
    print("Voice found. I am " + voice_for_tts + ". Beginning generation...")

    communicate = edge_tts.Communicate(TEXT, voice_for_tts)
    submaker = edge_tts.SubMaker()
    stdout = sys.stdout
    audio_bytes = []
    
    with open(OUTPUT_FILE, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                submaker.feed(chunk)

    print("Done generating audio and subtitles. Saving subtitles to file...")
    with open(SRT_FILE, "w", encoding="utf-8") as file:
        file.write(submaker.get_srt())
    
    stdout.write(f"Audio file length: {len(audio_bytes)}\n")
    stdout.write(submaker.get_srt())