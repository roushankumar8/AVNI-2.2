import asyncio
import os
import tempfile
import threading

import edge_tts
import pygame
import speech_recognition as sr

from config import WAKE_PHRASES, SPEECH_LANGUAGE


class VoiceEngine:

    def __init__(self):

        # -------------------------
        # Speech Recognition
        # -------------------------

        self.recognizer = sr.Recognizer()

        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.7

        # -------------------------
        # TTS
        # -------------------------

        self.tts_voice = "hi-IN-SwaraNeural"
        self.tts_rate = "+0%"
        self.tts_volume = "+0%"

        self.tts_lock = threading.Lock()

        # -------------------------
        # Audio Player
        # -------------------------

        pygame.mixer.init()

        print("Hindi TTS voice:", self.tts_voice)

    # =========================================================
    # MICROPHONE CALIBRATION
    # =========================================================

    def calibrate(self, microphone):

        print("Calibrating microphone...")

        with microphone as source:

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

        print("Microphone calibrated.")

    # =========================================================
    # SPEECH RECOGNITION
    # =========================================================

    def listen(self, microphone):

        with microphone as source:

            print("Listening...")

            try:

                audio = self.recognizer.listen(
                    source,
                    phrase_time_limit=8
                )

            except Exception as error:

                print("Microphone error:", error)

                return ""

        try:

            text = self.recognizer.recognize_google(
                audio,
                language=SPEECH_LANGUAGE
            )

            print("You:", text)

            return text.strip()

        except sr.UnknownValueError:

            print("Could not understand audio.")

            return ""

        except sr.RequestError as error:

            print(
                "Speech recognition error:",
                error
            )

            return ""

    # =========================================================
    # WAKE WORD DETECTION
    # =========================================================

    def is_wake_word(self, text):

        normalized = " ".join(
            text.lower().strip().split()
        )

        print(
            "Checking wake word:",
            repr(normalized)
        )

        wake_variations = [

            # English
            "hey avni",
            "hi avni",
            "hii avni",
            "avni",
            "hello avni",
            "helo avni",

            # Hindi
            "अवनी",
            "अवनि",
            "हे अवनी",
            "हे अवनि",
            "हाय अवनी",
            "हाय अवनि",
            "हेलो अवनी",
            "हेलो अवनि",
        ]

        # Exact match
        if normalized in wake_variations:

            print(
                "Wake phrase matched:",
                normalized
            )

            return True

        # Sometimes speech recognition adds extra words.
        # Example:
        # "हे अवनी जी"
        # "हेलो अवनी"
        # "अवनी सुनो"

        for phrase in wake_variations:

            if normalized.startswith(phrase + " "):

                print(
                    "Wake phrase matched:",
                    phrase
                )

                return True

        return False

    # =========================================================
    # TEXT TO SPEECH
    # =========================================================

    def speak(self, text):

        if not text:

            print("TTS: Empty response")

            return

        print(
            "TTS RECEIVED:",
            repr(text)
        )

        with self.tts_lock:

            temp_file = None

            try:

                # ---------------------------------
                # Temporary MP3 file
                # ---------------------------------

                fd, temp_file = tempfile.mkstemp(
                    suffix=".mp3"
                )

                os.close(fd)

                # ---------------------------------
                # Generate speech
                # ---------------------------------

                asyncio.run(
                    self.generate_speech(
                        text,
                        temp_file
                    )
                )

                print(
                    "TTS generated:",
                    temp_file
                )

                # ---------------------------------
                # Play speech
                # ---------------------------------

                pygame.mixer.music.load(
                    temp_file
                )

                pygame.mixer.music.play()

                print("TTS STARTING...")

                while pygame.mixer.music.get_busy():

                    pygame.time.Clock().tick(20)

                print("TTS FINISHED")

                pygame.mixer.music.stop()

                pygame.mixer.music.unload()

            except Exception as error:

                print(
                    "TTS ERROR:",
                    repr(error)
                )

            finally:

                # ---------------------------------
                # Delete temporary audio
                # ---------------------------------

                if temp_file:

                    try:

                        if os.path.exists(temp_file):

                            os.remove(temp_file)

                    except Exception as error:

                        print(
                            "Could not delete temp file:",
                            error
                        )

    # =========================================================
    # EDGE TTS GENERATION
    # =========================================================

    async def generate_speech(
        self,
        text,
        output_file
    ):

        communicate = edge_tts.Communicate(

            text=text,

            voice=self.tts_voice,

            rate=self.tts_rate,

            volume=self.tts_volume
        )

        await communicate.save(
            output_file
        )