#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Text-To-Speech API sample application .

Example usage:
    python synthesize_text.py --text "hello"
    python synthesize_text.py --ssml "<speak>Hello there.</speak>"
"""

import argparse


# [START tts_synthesize_text]
def synthesize_text(text):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        # language_code='ja-JP', # JP
        # language_code='fil-PH', # PH
        language_code='en-US', # EN
        # name='ja-JP-Wavenet-C' # JP Driver
        # name='ja-JP-Wavenet-D' # JP Optimal
        # name='ja-JP-Wavenet-B' # JP Explorer
        # name='ja-JP-Wavenet-A' # JP Familiarization
        # name='en-US-Wavenet-A' # EN Familiarization
        name='en-US-Wavenet-D' # EN Driver 
        # name='en-US-Wavenet-E' # EN Optimal
        # name='en-US-Wavenet-B' # EN Explorer
        # name='fil-PH-Wavenet-A' # PH Agent
        # ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL
        )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        effects_profile_id=['handset-class-device']
        # ,pitch=3.6      # PH Driver
        # ,pitch=-3.20    # PH Optimal
        # ,pitch=0        # PH Explorer
        # ,pitch=1.0      # PH Familiarization
        # ,speaking_rate=1.20
        )

    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

    # The response's audio_content is binary.
    fileName = 'study4/generic_right_optimal.mp3'
    with open(fileName, 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file ', fileName)
# [END tts_synthesize_text]


# [START tts_synthesize_ssml]
def synthesize_ssml(ssml):
    """Synthesizes speech from the input string of ssml.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/

    Example: <speak>Hello there.</speak>
    """
    from google.cloud import texttospeech
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.types.SynthesisInput(ssml=ssml)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Standard-B'
        # ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL
        )

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
# [END tts_synthesize_ssml]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--text',
                       help='The text from which to synthesize speech.')
    group.add_argument('--ssml',
                       help='The ssml string from which to synthesize speech.')

    args = parser.parse_args()

    if args.text:
        synthesize_text(args.text)
    else:
        synthesize_ssml(args.ssml)
