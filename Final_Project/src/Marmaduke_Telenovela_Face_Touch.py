#!/usr/bin/env python3
"""Adapted from the saved Marmaduke_Telenovela.py (version 2).

Keep this file beside the existing Marmaduke_Learn_Spanish.py.
Start the existing camera stream first. Face enrollment is not changed.
Code, comments, and terminal messages are English; spoken dialogue is Spanish.
Double touch triggers tail feedback only; this version does not save lessons.
This integration requires testing on the Raspberry Pi.
"""
from __future__ import annotations

# BLOCK 1: Import standard tools and reuse the original voice/face helpers.
import queue
import runpy
import subprocess
import threading
from pathlib import Path
from tempfile import TemporaryDirectory
from time import monotonic

from openai import OpenAI
import Marmaduke_Learn_Spanish as buddy

# BLOCK 2: Configure proximity, touch timing, and tail feedback.
NEAR_CM = 13.0
RESET_CM = 25.0
DOUBLE_TAP_SECONDS = 1.0
RELEASE_SECONDS = 0.08
TAIL_SECONDS = 3.0
HAND_LINE = "¡No puedes pegarme! ¡Es ilegal! ¡Y además, arruinarías mi actuación!"

# BLOCK 3: Describe the acting character in English, requesting Spanish speech.
TELENOVELA_PROMPT = """
You are Marmaduke, rehearsing a fictional Mexican telenovela with Maria Jose.
She is your co-star, not your teacher. Address her as Maria Jose.
Speak Spanish in short, expressive sentences with friendly sarcasm.
Improvise funny, absurd romantic or family conflicts based on what she says.
The voice has a light French accent. Do not turn the conversation into a quiz.
All arguments are fictional acting; do not encourage real violence.
Never claim a physical action occurred unless the program confirms it.
A double head touch triggers silent tail feedback. Do not announce the touches,
claim that a lesson was saved, or describe this as language-model training.
"""


def monitor_hardware(notices: queue.Queue, stop: threading.Event) -> None:
    """Own one Pidog instance for touch, tail, and ultrasonic access.

    Pidog initialization may initialize other installed components too.
    This function does not disable IMU/RGB or request walking/standing actions.
    """
    dog = None
    tail_deadline = None

    # BLOCK 4: Send bounded events without blocking sensor polling.
    def notify(event: str) -> None:
        try:
            notices.put_nowait(event)
        except queue.Full:
            pass

    try:
        from pidog import Pidog
        dog = Pidog()
        first_tap = None
        released_since = None
        ready_for_touch = False
        proximity_armed = True
        close_samples = clear_samples = 0
        next_distance_read = 0.0
        touch_enabled = proximity_enabled = True
        print("Hardware ready. Two head touches trigger a three-second tail wag.", flush=True)

        while not stop.is_set():
            now = monotonic()

            # BLOCK 5: Stop tail feedback after its deadline; keep polling meanwhile.
            if tail_deadline is not None and now >= tail_deadline:
                dog.tail_stop()
                tail_deadline = None
                print("Tail feedback complete.", flush=True)

            # BLOCK 6: Count separate contact edges, not a continuous held touch.
            # Require a stable release before each contact and two contacts <= 1 s.
            if touch_enabled:
                try:
                    touch_state = dog.dual_touch.read()
                except Exception as error:
                    touch_enabled = False
                    print(f"Touch sensor unavailable: {error}", flush=True)
                else:
                    if first_tap is not None and now - first_tap > DOUBLE_TAP_SECONDS:
                        first_tap = None
                    if touch_state == "N":
                        if released_since is None:
                            released_since = now
                        if now - released_since >= RELEASE_SECONDS:
                            ready_for_touch = True
                    elif isinstance(touch_state, str) and touch_state:
                        released_since = None
                        if ready_for_touch:
                            ready_for_touch = False
                            if tail_deadline is not None:
                                first_tap = None
                            elif first_tap is not None and now - first_tap <= DOUBLE_TAP_SECONDS:
                                first_tap = None
                                # BLOCK 7: Give physical feedback without a spoken announcement.
                                dog.do_action("wag_tail", step_count=30, speed=80)
                                tail_deadline = monotonic() + TAIL_SECONDS
                                print("Double touch detected. Tail feedback started.", flush=True)
                            else:
                                first_tap = now
                    else:
                        # Invalid readings cannot count as touches.
                        released_since = None
                        ready_for_touch = False
                        first_tap = None

            # BLOCK 8: Poll distance separately from the faster touch loop.
            # Ultrasonic sensing detects proximity, not a hand or its intention.
            if proximity_enabled and now >= next_distance_read:
                next_distance_read = now + 0.25
                try:
                    distance = float(dog.read_distance())
                except (TypeError, ValueError, OSError):
                    distance = 0.0
                except Exception as error:
                    proximity_enabled = False
                    distance = 0.0
                    print(f"Ultrasonic sensor unavailable: {error}", flush=True)
                if 1.0 <= distance <= NEAR_CM:
                    close_samples += 1
                    clear_samples = 0
                    if proximity_armed and close_samples >= 2:
                        notify("object_near")
                        proximity_armed = False
                elif distance >= RESET_CM:
                    clear_samples += 1
                    close_samples = 0
                    if clear_samples >= 3:
                        proximity_armed = True
                else:
                    close_samples = clear_samples = 0
            stop.wait(0.02)
    except Exception as error:
        print(f"Hardware monitoring stopped: {error}", flush=True)
        print("Conversation may continue, but sensor/tail feedback is unavailable.", flush=True)
    finally:
        # BLOCK 9: Release hardware even if an exception or shutdown occurs.
        if dog is not None:
            try:
                if tail_deadline is not None:
                    dog.tail_stop()
            finally:
                dog.close()


def main() -> None:
    # BLOCK 10: Load the existing private API key without displaying its value.
    key_settings = runpy.run_path(str(buddy.KEY_FILE))
    client = OpenAI(api_key=key_settings["OPENAI_API_KEY"].strip())

    # BLOCK 11: Require the original saved-face recognition before starting.
    # This reuses the existing camera stream and profile, not another camera owner.
    print("Waiting for Maria Jose's saved face profile to match.", flush=True)
    buddy.wait_for_maria()
    print("The original face-recognition gate returned. Starting rehearsal.", flush=True)

    # BLOCK 12: Preserve the original personality and add the acting scenario.
    history = [{"role": "system", "content": buddy.PERSONALITY + "\n" + TELENOVELA_PROMPT}]
    notices: queue.Queue = queue.Queue(maxsize=1)
    stop = threading.Event()
    watcher = threading.Thread(target=monitor_hardware, args=(notices, stop), daemon=False)

    with TemporaryDirectory() as tmp:
        audio_folder = Path(tmp)

        # BLOCK 13: Generate Cedar speech and play the WAV locally on the robot.
        # French accent is a synthesis instruction, not a guaranteed voice property.
        def say(text: str) -> None:
            print("Marmaduke:", text, flush=True)
            response = client.audio.speech.create(
                model="gpt-4o-mini-tts", voice="cedar", response_format="wav",
                instructions=("Speak clearly intelligible Spanish with a light French accent. "
                              "Be theatrical, playful, warm, and expressive, like an actor "
                              "rehearsing a Mexican telenovela. Do not speak French unless asked."),
                input=text,
            )
            audio_path = audio_folder / "marmaduke_reply.wav"
            audio_path.write_bytes(response.content)
            subprocess.run(["aplay", "-q", str(audio_path)], check=True)
            history.append({"role": "assistant", "content": text})

        watcher.start()
        try:
            # BLOCK 14: Generate an opening instead of using a fixed dialogue script.
            opening = buddy.reply(client, history + [{
                "role": "system",
                "content": "Open with one funny, passionate Spanish telenovela sentence addressed to Maria Jose.",
            }])
            say(opening)

            # BLOCK 15: Keep conversational listening and replies in the main thread.
            # Touch and tail monitoring run independently in the hardware thread.
            while True:
                heard = buddy.listen(client, audio_folder).strip()
                if heard:
                    print("Maria Jose:", heard, flush=True)
                    if heard.casefold() in {"adiós marmaduke", "adios marmaduke",
                                            "terminar conversación", "terminar conversacion"}:
                        break
                    history.append({"role": "user", "content": heard})

                # BLOCK 16: Handle proximity after a listening turn to avoid overlapping audio.
                try:
                    notices.get_nowait()
                except queue.Empty:
                    pass
                else:
                    history.append({"role": "system", "content":
                                    "An object is close to the front sensor. React as fictional acting."})
                    say(HAND_LINE)

                if heard:
                    say(buddy.reply(client, history))
                # Keep the initial instructions and a short rolling dialogue history.
                history[:] = [history[0], *history[1:][-12:]]
        except KeyboardInterrupt:
            print("\nRehearsal stopped.", flush=True)
        finally:
            # BLOCK 17: Signal the hardware thread and wait for device cleanup.
            stop.set()
            print("Closing robot hardware...", flush=True)
            watcher.join()


# BLOCK 18: Run only when this file is launched directly, not when imported.
if __name__ == "__main__":
    main()
