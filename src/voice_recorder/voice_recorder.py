import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import time
import threading
from datetime import datetime

class VoiceRecorder:
    def __init__(self, output_filename="meeting_recording", rate=44100, max_length=10):
        """
        Initialize the VoiceRecorder with recording settings.

        Parameters:
        - output_filename (str): Base name for output audio files.
        - rate (int): Sample rate for recording.
        - max_length (int): Maximum length of each recording chunk in seconds.
        """
        self.output_filename = output_filename
        self.rate = rate
        self.max_length = max_length
        self.is_recording = False
        self.frames = []
        self.file_count = 1
        self.start_time = None
        self.stream = None
        self._recording_thread = None

    def start(self):
        """Start recording audio in chunks of max_length seconds."""
        if self.is_recording:
            print("Recording is already in progress.")
            return

        try:
            self.is_recording = True
            print("Recording started...")

            self.frames = []
            self.start_time = time.time()
            self.stream = sd.InputStream(samplerate=self.rate, channels=1, callback=self._callback)
            self.stream.start()
            # Run the recording loop in a separate thread
            self._recording_thread = threading.Thread(target=self._recording_loop)
            self._recording_thread.start()
        except Exception as e:
            print(f"Failed to start recording: {e}")
            self.is_recording = False

    def _callback(self, indata, frames, time_info, status):
        """Callback function to capture audio chunks."""
        if self.is_recording:
            self.frames.append(indata.copy())

    def _recording_loop(self):
        """Continuously checks and saves audio when max_length is reached."""
        try:
            while self.is_recording:
                elapsed_time = time.time() - self.start_time
                if elapsed_time >= self.max_length:
                    self._save_file()
                    self.frames = []  # Reset frames for the next segment
                    self.start_time = time.time()  # Reset start time
                time.sleep(0.1)  # Sleep to prevent busy-waiting
        except Exception as e:
            print(f"Error during recording loop: {e}")
        finally:
            self.stop()  # Ensure proper cleanup if thread exits unexpectedly

    def stop(self):
        """Stop recording and save any remaining audio data."""
        if not self.is_recording:
            print("Recording is not in progress.")
            return

        print("Recording stopped.")
        self.is_recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        # Wait for recording thread to complete
        if self._recording_thread:
            self._recording_thread.join()

        if self.frames:
            self._save_file()  # Save remaining frames
        print("All files saved.")

    def _save_file(self):
        """Save the current audio frames to a file with a numeric suffix."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{self.output_filename}_{timestamp}_{self.file_count}.wav"
        audio_data = np.concatenate(self.frames, axis=0)
        write(output_file, self.rate, audio_data)
        print(f"Audio saved as {output_file}")
        self.file_count += 1
