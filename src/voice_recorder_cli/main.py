import argparse
import time
from voice_recorder import VoiceRecorder  # Assume the class is saved in `voice_recorder.py`


def run_start(args: argparse.Namespace):
    """
    Starts recording audio based on the provided arguments and continues until Ctrl+C is pressed.
    """
    recorder = VoiceRecorder(
        output_filename=args.output_filename,
        rate=args.rate,
        max_length=args.max_length
    )

    print("Press Ctrl+C to stop recording.")
    recorder.start()

    try:
        # Keep recording until interrupted by Ctrl+C
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nRecording interrupted by user.")
    finally:
        recorder.stop()
        print("Recording stopped and saved.")


def main():
    parser = argparse.ArgumentParser(description="Voice Recorder CLI")

    # Subparsers for `start` and `stop` commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Start command
    start_parser = subparsers.add_parser("start", help="Start recording audio")
    start_parser.add_argument(
        "--output_filename",
        type=str,
        default="meeting_recording",
        help="Base filename for the output recording files"
    )
    start_parser.add_argument(
        "--rate",
        type=int,
        default=44100,
        help="Sample rate for recording"
    )
    start_parser.add_argument(
        "--max_length",
        type=int,
        default=10,
        help="Maximum length of each recording chunk in seconds"
    )

    # Stop command (mostly illustrative in this setup)
    subparsers.add_parser("stop", help="Stop recording audio")

    # Parse arguments
    args = parser.parse_args()

    # Call appropriate function based on the command
    if args.command == "start":
        run_start(args)
    elif args.command == "stop":
        print("not implemented")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
