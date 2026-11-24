"""Run with system Python in terminal 1; leave it running."""
# BLOCK 1: Load the original SunFounder camera library.
from signal import pause
from vilib import Vilib

# BLOCK 2: Open the camera once and expose its local web stream.
Vilib.camera_start()
try:
    Vilib.face_detect_switch(True)
    Vilib.display(local=False, web=True)
    print('Camera is running. Keep this terminal open.', flush=True)
    # BLOCK 3: Keep the stream available to recognition until Ctrl+C.
    pause()
except KeyboardInterrupt:
    print('Stopping camera.')
finally:
    # BLOCK 4: Release the camera cleanly.
    Vilib.camera_close()
