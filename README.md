# Voice Recorder CLI

A simple CLI-based voice recorder that captures audio in chunks and saves each chunk as a separate WAV file. This project is useful for recording meetings, lectures, or any other continuous audio sessions.

## Features
- Record audio in chunks of a specified length (e.g., 10 seconds).
- Automatically saves each chunk to a WAV file with a timestamped filename.
- Simple CLI commands to start and stop recording.

## Requirements
- Python 3.7 or later
- `sounddevice` for audio input
- `scipy` and `numpy` for handling audio data

## Usage

### Start Recording

To start recording, use the start command. Specify the output filename prefix, sample rate, chunk length, and recording duration if needed.
```
voice-recorder start --output_filename "session" --rate 44100 --max_length 10 
```

--output_filename: Base name for the output files. (Default: meeting_recording)
--rate: Sample rate for recording. (Default: 44100)
--max_length: Maximum length (in seconds) for each recorded chunk. (Default: 10)

### Stop Recording

To stop recording, use the stop command.

```
voice-recorder stop
```

### Example

Record audio in chunks of 10 seconds, with a total duration of 30 seconds:

```
voice-recorder start --output_filename "lecture" --max_length 10 

sleep 30

voice-recorder sop
```
