import json
import os


class MemoryManager:

    def __init__(self):

        self.file = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            "memory.json"
        )

        self.memory = self.load_memory()

    # ==============================
    # LOAD
    # ==============================

    def load_memory(self):

        if not os.path.exists(self.file):
            return {}

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception as error:

            print("Memory load error:", error)

            return {}

    # ==============================
    # SAVE FILE
    # ==============================

    def save_file(self):

        try:

            with open(
                self.file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    self.memory,
                    f,
                    ensure_ascii=False,
                    indent=4
                )

            print("Memory saved.")

        except Exception as error:

            print(
                "Memory save error:",
                error
            )

    # ==============================
    # SET
    # ==============================

    def set(self, key, value):

        key = key.strip().lower()
        value = value.strip()

        self.memory[key] = value

        self.save_file()

    # ==============================
    # GET
    # ==============================

    def get(self, key):

        return self.memory.get(
            key.strip().lower()
        )

    # ==============================
    # DELETE
    # ==============================

    def delete(self, key):

        key = key.strip().lower()

        if key in self.memory:

            del self.memory[key]

            self.save_file()

            return True

        return False

    # ==============================
    # GET ALL
    # ==============================

    def get_all(self):

        return self.memory