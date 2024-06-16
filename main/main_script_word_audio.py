"""Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
import os
from google.cloud import texttospeech
from utils import common
import time

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

if not os.path.exists(common.Constants.OUTPUT_BASE_FOLDER):
    os.makedirs(common.Constants.OUTPUT_BASE_FOLDER)

if not os.path.exists(common.Constants.INPUT_BASE_FOLDER):
    os.makedirs(common.Constants.INPUT_BASE_FOLDER)

client = texttospeech.TextToSpeechClient()


def get_linse(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        output_lines = file.readlines()

    output_lines = [output_line.strip() for output_line in output_lines]
    return output_lines


def synthesis_voice(_text_content, output, _voice_name):
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=_text_content)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=_voice_name
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
    with open(f'{common.Constants.OUTPUT_BASE_FOLDER}/{output}.mp3', "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(f'audio content written to file "{output}"')


if __name__ == '__main__':
    voice_name = common.Constants.JOURNEY_D_NAME
    topic_name = '5500-words'
    lines = get_linse(f'{common.Constants.INPUT_BASE_FOLDER}/txt/{topic_name}.txt')
    output_folder = f'{common.Constants.OUTPUT_BASE_FOLDER}/{voice_name}'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for index in range(len(lines)):
        try:
            line = lines[index]
            line = line.strip()
            output_file = f'{output_folder}/{line}'
            if line != '' and not os.path.isfile(f'{output_file}.mp3'):
                print(f'{index}:{voice_name} - {line}')
                synthesis_voice(line, output_file, voice_name)
        except Exception as e:
            print(f"Exception: {e}")
            time.sleep(60)
