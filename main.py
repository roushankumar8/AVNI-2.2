import threading

import speech_recognition as sr

from dashboard import Dashboard
from voice import VoiceEngine
from gemini_brain import GeminiBrain
from actions import ActionManager


class Avni:

    def __init__(self):

        self.dashboard = Dashboard()
        self.voice = VoiceEngine()
        self.brain = GeminiBrain()
        self.actions = ActionManager()

        self.running = True
        self.active = False

        threading.Thread(
            target=self.voice_loop,
            daemon=True
        ).start()

    # =========================================================
    # DASHBOARD STATE
    # =========================================================

    def set_state(self, state):

        self.dashboard.root.after(
            0,
            lambda: self.dashboard.set_state(state)
        )

    # =========================================================
    # VOICE LOOP
    # =========================================================

    def voice_loop(self):

        microphone = sr.Microphone()

        self.voice.calibrate(microphone)

        # =====================================================
        # WAIT FOR "HEY AVNI"
        # =====================================================

        while self.running and not self.active:

            print("\nWaiting for: Hey Avni...")

            self.set_state("LISTENING")

            text = self.voice.listen(microphone)

            print("Heard:", repr(text))

            if self.voice.is_wake_word(text):

                print("\n🔥 AVNI ACTIVATED")

                self.active = True

                self.set_state("SPEAKING")

                self.voice.speak(
                    "Hello Roushan… mai tumhari kaise madad kar sakti hun?"
                )

                self.set_state("IDLE")

        # =====================================================
        # ACTIVE MODE
        # =====================================================

        while self.running and self.active:

            print("\n🎤 Active mode - Listening for command...")

            self.set_state("LISTENING")

            command = self.voice.listen(microphone)

            print(
                "Command received:",
                repr(command)
            )

            if not command:

                continue

            normalized_command = (
                command
                .lower()
                .strip()
            )

            # =================================================
            # EXIT COMMAND
            # =================================================

            exit_commands = [
                "bye",
                "ok bye",
                "okay bye",
                "goodbye",
                "bye avni",
                "ok bye avni",

                "बाय",
                "ओके बाय",
                "ओके बाय अवनी",
                "गुडबाय",
                "अलविदा"
            ]

            if normalized_command in exit_commands:

                print("\n👋 AVNI SHUTTING DOWN")

                self.set_state("SPEAKING")

                self.voice.speak(
                    "ok, bye. Apna dhyaan rakhna"
                )

                self.active = False
                self.running = False

                self.set_state("IDLE")

                # Close dashboard
                self.dashboard.root.after(
                    500,
                    self.dashboard.root.destroy
                )

                break

            # =================================================
            # GEMINI
            # =================================================

            self.set_state("THINKING")

            print(
                "Checking local action:",
                command
            )

            action_response = self.actions.execute(command)

            if action_response:

                print(
                    "Action executed:",
                    action_response
                )

                self.set_state("SPEAKING")

                self.voice.speak(
                    action_response
                )

                self.set_state("IDLE")

                continue


            print(
                "Sending to Gemini:",
                command
            )

            try:

                response = self.brain.ask(command)

                print(
                    "Gemini response:",
                    response
                )

                self.set_state("SPEAKING")

                self.voice.speak(response)

                self.set_state("IDLE")

            except Exception as error:

                print(
                    "Gemini error:",
                    error
                )

                self.set_state("SPEAKING")

                self.voice.speak(
                    "माफ़ कीजिए, Gemini से कनेक्शन नहीं हो पाया।"
                )

                self.set_state("IDLE")

    # =========================================================
    # RUN DASHBOARD
    # =========================================================

    def run(self):

        self.dashboard.run()


# =============================================================
# START AVNI
# =============================================================

if __name__ == "__main__":

    app = Avni()

    app.run()