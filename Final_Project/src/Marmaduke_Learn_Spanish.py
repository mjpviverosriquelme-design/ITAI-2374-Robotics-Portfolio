#!/usr/bin/env python3
"""Reconstructed support module for Marmaduke_Telenovela_Face_Touch.py.

This is a compatible adaptation, not the recovered original Raspberry Pi file.
It provides the exact helper names used by the main program. Keep all four
scripts together. Existing private keys and face profiles are separate assets.
"""
# BLOCK 1: Import utilities without opening devices or making API calls on import.
import os
import subprocess
from pathlib import Path

# BLOCK 2: Locate the existing private key and allow microphone configuration.
ROOT = Path(__file__).resolve().parent
KEY_FILE = Path(os.environ.get(
    'MARMADUKE_KEY_FILE',
    str(Path.home() / 'pidog/examples/marmaduke_api_keys.py'),
)).expanduser()
MICROPHONE = os.environ.get('MARMADUKE_MICROPHONE', 'plughw:2,0')
PERSONALITY = (
    'You are Marmaduke, a friendly, playful robot dog. Address your conversation '
    'partner as Maria Jose, never profesora. Speak Spanish unless she requests '
    'another language. Keep responses brief, natural, and gently sarcastic. '
    'Do not claim to remember information that is not in the conversation. '
    'Do not claim that a word was saved or that a physical action occurred.'
)


def wait_for_maria():
    # BLOCK 3: Use system Python for OpenCV and the saved local face profile.
    # --once exits successfully only after three consecutive matching frames.
    script = ROOT / 'face_recognition.py'
    if not script.is_file():
        raise FileNotFoundError(f'Required recognition script is missing: {script}')
    subprocess.run(
        ['/usr/bin/python3', '-u', str(script), 'recognize', '--once'],
        check=True,
    )


def listen(client, folder):
    # BLOCK 4: Record one eight-second microphone turn as a mono PCM WAV.
    audio_path = Path(folder) / 'microphone_turn.wav'
    print('Listening now. Speak for up to 8 seconds.', flush=True)
    subprocess.run([
        'arecord', '-q', '-D', MICROPHONE, '-f', 'S16_LE',
        '-r', '16000', '-c', '1', '-d', '8', str(audio_path),
    ], check=True)
    # BLOCK 5: Transcribe the recording through OpenAI; do not save a lesson here.
    with audio_path.open('rb') as audio:
        result = client.audio.transcriptions.create(
            model='gpt-4o-mini-transcribe', file=audio, language='es',
            prompt='Conversation with Marmaduke and Maria Jose in Chilean Spanish.',
        )
    return (result.text or '').strip()


def reply(client, history):
    # BLOCK 6: Generate a response from the actual conversation history.
    # The main file supplies the acting instructions and handles speech playback.
    result = client.chat.completions.create(
        model='gpt-4o-mini', messages=history,
    )
    answer = result.choices[0].message.content
    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError('The language model returned an empty reply.')
    return answer.strip()
