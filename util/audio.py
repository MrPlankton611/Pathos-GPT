import os
from threading import Thread
from dotenv import load_dotenv #type:ignore
from elevenlabs.client import ElevenLabs #type:ignore
from elevenlabs import play #type:ignore

load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("AUDIO_API_KEY"),
)

def playaudio(text):
    audio = client.text_to_speech.convert(
        text= text,
        voice_id="c9UR7RCuRfZGBwNp0CSh",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    
    def playThread():
        play(audio)

    Thread(target = playThread).start()

    #        <button class="chat-button" id="chat-button" onclick="sendMessage()">Send</button>
