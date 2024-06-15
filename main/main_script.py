"""Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
import os
from google.cloud import texttospeech
from utils import constant, mergeMap3
import random

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

if not os.path.exists(constant.Constants.OUTPUT_BASE_FOLDER):
    os.makedirs(constant.Constants.OUTPUT_BASE_FOLDER)

if not os.path.exists(constant.Constants.INPUT_BASE_FOLDER):
    os.makedirs(constant.Constants.INPUT_BASE_FOLDER)

# Instantiates a client
client = texttospeech.TextToSpeechClient()


def get_linse(input_file):
    # 读取文件并将每一行存储到一个列表中
    with open(input_file, 'r', encoding='utf-8') as file:
        output_lines = file.readlines()

    # 移除每行末尾的换行符，并创建一个新的列表
    output_lines = [output_line.strip() for output_line in output_lines]
    return output_lines


def synthesis_voice(text, output, voice_name):
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(f'{constant.Constants.OUTPUT_BASE_FOLDER}/{output}.mp3', "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(f'audio content written to file "{output}"')


class RandomRobin:

    def __init__(self, length):
        self.current_index = 0
        self.length = length

    def get_index(self):
        if self.current_index >= self.length - 1:
            self.current_index = 0
            return 0
        else:
            self.current_index = self.current_index + 1
        return self.current_index


if __name__ == '__main__':
    voice_names = [constant.Constants.JOURNEY_F_NAME, constant.Constants.JOURNEY_D_NAME,
                   constant.Constants.JOURNEY_O_NAME]
    voice_map = {"Alice": constant.Constants.JOURNEY_F_NAME, "Bob": constant.Constants.JOURNEY_D_NAME}
    randomRobin = RandomRobin(len(voice_names))

    topic_name = 'Discussion on Financial Settlements'
    lines = get_linse(f'{constant.Constants.INPUT_BASE_FOLDER}/txt/{topic_name}.txt')
    # 遍历列表
    for index in range(len(lines)):
        voice_name = voice_names[randomRobin.get_index()]
        line = lines[index]
        line = line.strip()
        output_file = f'{constant.Constants.OUTPUT_BASE_FOLDER}/tmp/{topic_name}-{str(index).zfill(10)}'
        if line != '' and not os.path.isfile(f'{output_file}.mp3'):
            voice_name_name_text = line.split(": ")
            if len(voice_name_name_text) > 1:
                voice_name = voice_map[voice_name_name_text[0]]
                text = voice_name_name_text[1]
            else:
                voice_name = constant.Constants.JOURNEY_O_NAME
                text = line
            print(f'{index}:{voice_name} - {text}')
            synthesis_voice(text, output_file, voice_name)
    mergeMap3 = mergeMap3.MergeMap3(f'{constant.Constants.OUTPUT_BASE_FOLDER}/tmp/',
                                    f'{constant.Constants.OUTPUT_BASE_FOLDER}/{topic_name}-3.mp3')
    mergeMap3.merge()
