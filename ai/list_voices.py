from google.cloud import texttospeech
import os
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

client = texttospeech.TextToSpeechClient()

# 获取所有可用的声音选项
voices = client.list_voices()
for voice in voices.voices:
    print(f"Name: {voice.name}")
    print(f"Language codes: {voice.language_codes}")
    print(f"SSML gender: {voice.ssml_gender.name}")
    print()