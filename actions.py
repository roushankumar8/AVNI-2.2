import os
import re
import subprocess
import webbrowser
from urllib.parse import quote_plus


# ==========================================
# YT-DLP
# ==========================================

try:
    import yt_dlp

    YT_DLP_AVAILABLE = True

except ImportError:

    yt_dlp = None

    YT_DLP_AVAILABLE = False


class ActionManager:

    def __init__(self):
        pass

    # ==========================================
    # OPEN URL
    # ==========================================

    def open_url(self, url):

        webbrowser.open(url)

    # ==========================================
    # GOOGLE SEARCH
    # ==========================================

    def search_google(self, query):

        url = (
            "https://www.google.com/search?q="
            + quote_plus(query)
        )

        self.open_url(url)

    # ==========================================
    # YOUTUBE SEARCH
    # ==========================================

    def search_youtube(self, query):

        url = (
            "https://www.youtube.com/results?search_query="
            + quote_plus(query)
        )

        self.open_url(url)

    # ==========================================
    # FIND CHROME
    # ==========================================

    def find_chrome(self):

        chrome_paths = [

            os.path.expandvars(
                r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"
            ),

            os.path.expandvars(
                r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe"
            ),

            os.path.expandvars(
                r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
            )
        ]

        for path in chrome_paths:

            if os.path.exists(path):

                return path

        return None


    # ==========================================
    # OPEN VIDEO WITH AUTOPLAY
    # ==========================================

    def open_video(self, video_url):

        chrome = self.find_chrome()

        if chrome:

            try:

                subprocess.Popen([
                    chrome,

                    # Chrome autoplay policy
                    "--autoplay-policy=no-user-gesture-required",

                    # Start maximized
                    "--start-maximized",

                    # Open YouTube video
                    video_url

                ])

                print("Chrome opened with autoplay enabled.")

                return True

            except Exception as e:

                print(
                    "Chrome error:",
                    repr(e)
                )

        # ======================================
        # FALLBACK
        # ======================================

        try:

            self.open_url(video_url)

            return True

        except Exception as e:

            print(
                "Browser error:",
                repr(e)
            )

            return False

    # ==========================================
    # PLAY SONG
    # ==========================================

    def play_song(self, query):

        query = query.strip()

        if not query:

            return (
                "कौन सा गाना चलाऊँ?"
            )

        print()
        print("=" * 50)
        print(
            "SONG REQUEST:",
            query
        )
        print("=" * 50)

        # ======================================
        # YT-DLP NOT INSTALLED
        # ======================================

        if not YT_DLP_AVAILABLE:

            print(
                "yt-dlp is not installed."
            )

            self.search_youtube(
                query + " song"
            )

            return (
                f"{query} का गाना "
                "YouTube पर खोल रही हूँ।"
            )

        # ======================================
        # SEARCH YOUTUBE
        # ======================================

        try:

            ydl_options = {

                "quiet": True,

                "no_warnings": True,

                "extract_flat": True,

                "skip_download": True,

                "noplaylist": True
            }

            # ==================================
            # FIRST SEARCH
            # ==================================

            search_query = (
                f"ytsearch1:{query} song"
            )

            print(
                "YouTube search:",
                search_query
            )

            with yt_dlp.YoutubeDL(
                ydl_options
            ) as ydl:

                result = ydl.extract_info(
                    search_query,
                    download=False
                )

            entries = result.get(
                "entries",
                []
            )

            # ==================================
            # SECOND SEARCH
            # ==================================

            if not entries:

                print(
                    "First search returned "
                    "no result."
                )

                search_query = (
                    f"ytsearch5:{query}"
                )

                with yt_dlp.YoutubeDL(
                    ydl_options
                ) as ydl:

                    result = ydl.extract_info(
                        search_query,
                        download=False
                    )

                entries = result.get(
                    "entries",
                    []
                )

            # ==================================
            # VIDEO FOUND
            # ==================================

            if entries:

                video = entries[0]

                video_id = video.get(
                    "id"
                )

                title = video.get(
                    "title",
                    query
                )

                print(
                    "Found:",
                    title
                )

                # ==================================
                # VIDEO ID
                # ==================================

                if video_id:

                    video_url = (
                        "https://www.youtube.com/watch?v="
                        + video_id
                        + "&autoplay=1"
                    )

                    print(
                        "Video URL:",
                        video_url
                    )

                    # Open + Auto Play
                    success = self.open_video(
                        video_url
                    )

                    if success:

                        return (
                            f"{title} चला रही हूँ।"
                        )

            # ==================================
            # SEARCH RESULT NOT FOUND
            # ==================================

            print(
                "No direct video found."
            )

            self.search_youtube(
                query + " song"
            )

            return (
                f"{query} का गाना "
                "YouTube पर खोज रही हूँ।"
            )

        except Exception as e:

            print()
            print(
                "YT-DLP ERROR:",
                repr(e)
            )

            print(
                "Using YouTube fallback."
            )

            self.search_youtube(
                query + " song"
            )

            return (
                f"{query} का गाना "
                "YouTube पर खोज रही हूँ।"
            )

    # ==========================================
    # EXECUTE COMMAND
    # ==========================================

    def execute(self, command):

        if not command:

            return None

        text = command.lower().strip()

        print()
        print(
            "COMMAND:",
            text
        )

        # ==================================================
        # SONG / MUSIC
        # ==================================================

        music_patterns = [

            # ------------------------------------------
            # English
            # ------------------------------------------

            r"^play (.+)$",

            r"^play (.+?) song$",

            r"^play (.+?) music$",

            r"^listen to (.+)$",

            r"^listen to (.+?) song$",

            # ------------------------------------------
            # Hinglish
            # ------------------------------------------

            r"^(.+?) ka song chalao$",

            r"^(.+?) ka gaana chalao$",

            r"^(.+?) ka gana chalao$",

            r"^(.+?) ka music chalao$",

            r"^(.+?) song chalao$",

            r"^(.+?) gaana chalao$",

            r"^(.+?) gana chalao$",

            r"^(.+?) chalao$",

            r"^(.+?) bajao$",

            r"^music chalao (.+)$",

            r"^music bajao (.+)$",

            r"^song chalao (.+)$",

            r"^song bajao (.+)$",

            r"^gaana chalao (.+)$",

            r"^gana chalao (.+)$",

            # ------------------------------------------
            # Hindi
            # ------------------------------------------

            r"^गाना बजाओ (.+)$",

            r"^गाना चलाओ (.+)$",

            r"^गाना बजा दो (.+)$",

            r"^म्यूजिक चलाओ (.+)$",

            r"^म्यूजिक बजाओ (.+)$",

            r"^गाना (.+) बजाओ$",

            r"^गाना (.+) चलाओ$"
        ]

        for pattern in music_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                query = match.group(1).strip()

                if query:

                    # ----------------------------------
                    # Remove extra words
                    # ----------------------------------

                    query = re.sub(
                        r"\s+(song|music|gaana|gana)$",
                        "",
                        query,
                        flags=re.IGNORECASE
                    ).strip()

                    print(
                        "Detected song:",
                        query
                    )

                    return self.play_song(
                        query
                    )

        # ==================================================
        # NOTEPAD
        # ==================================================

        if any(x in text for x in [

            "notepad",
            "note pad",
            "नोटपैड",
            "नोट पैड"

        ]):

            subprocess.Popen([
                "notepad.exe"
            ])

            return (
                "नोटपैड ओपन कर रही हूँ।"
            )

        # ==================================================
        # CALCULATOR
        # ==================================================

        if any(x in text for x in [

            "calculator",
            "calc",
            "कैलकुलेटर"

        ]):

            subprocess.Popen([
                "calc.exe"
            ])

            return (
                "कैलकुलेटर ओपन कर रही हूँ।"
            )

        # ==================================================
        # FILE EXPLORER
        # ==================================================

        if any(x in text for x in [

            "file explorer",
            "explorer",
            "files",
            "फाइल एक्सप्लोरर",
            "फाइल खोलो",
            "फाइल ओपन"

        ]):

            subprocess.Popen([
                "explorer.exe"
            ])

            return (
                "File Explorer ओपन कर रही हूँ।"
            )

        # ==================================================
        # DOWNLOADS
        # ==================================================

        if any(x in text for x in [

            "downloads",
            "download folder",
            "डाउनलोड",
            "डाउनलोड्स"

        ]):

            downloads = os.path.join(
                os.path.expanduser("~"),
                "Downloads"
            )

            if os.path.exists(downloads):

                subprocess.Popen([
                    "explorer.exe",
                    downloads
                ])

                return (
                    "Downloads folder "
                    "ओपन कर रही हूँ।"
                )

        # ==================================================
        # DESKTOP
        # ==================================================

        if any(x in text for x in [

            "desktop",
            "डेस्कटॉप"

        ]):

            desktop = os.path.join(
                os.path.expanduser("~"),
                "Desktop"
            )

            if os.path.exists(desktop):

                subprocess.Popen([
                    "explorer.exe",
                    desktop
                ])

                return (
                    "Desktop ओपन कर रही हूँ।"
                )

        # ==================================================
        # CHROME
        # ==================================================

        if any(x in text for x in [

            "chrome",
            "google chrome",
            "क्रोम"

        ]):

            chrome = self.find_chrome()

            if chrome:

                subprocess.Popen([
                    chrome
                ])

                return (
                    "Google Chrome "
                    "ओपन कर रही हूँ।"
                )

            self.open_url(
                "https://www.google.com"
            )

            return (
                "Chrome नहीं मिला, "
                "इसलिए Google खोल रही हूँ।"
            )

        # ==================================================
        # VS CODE
        # ==================================================

        if any(x in text for x in [

            "vs code",
            "visual studio code",
            "vscode",
            "वीएस कोड"

        ]):

            try:

                subprocess.Popen(
                    ["code"],
                    shell=True
                )

                return (
                    "VS Code ओपन कर रही हूँ।"
                )

            except Exception:

                return (
                    "VS Code नहीं मिल पाया।"
                )

        # ==================================================
        # CMD
        # ==================================================

        if any(x in text for x in [

            "command prompt",
            "cmd",
            "कमांड प्रॉम्प्ट"

        ]):

            subprocess.Popen([
                "cmd.exe"
            ])

            return (
                "Command Prompt "
                "ओपन कर रही हूँ।"
            )

        # ==================================================
        # POWERSHELL
        # ==================================================

        if any(x in text for x in [

            "powershell",
            "पावरशेल"

        ]):

            subprocess.Popen([
                "powershell.exe"
            ])

            return (
                "PowerShell ओपन कर रही हूँ।"
            )

        # ==================================================
        # YOUTUBE SEARCH
        # ==================================================

        youtube_search_patterns = [

            # English / Hinglish

            r"youtube (?:par|pe|me) (.+?) (?:search karo|search kar do|search)",

            r"youtube (?:par|pe|me) (.+?) (?:dhundo|dhoondo)",

            r"youtube (?:par|pe|me) (.+?) kholo",

            r"youtube (?:par|pe|me) (.+)",

            r"youtube search (.+)",

            r"search youtube (.+)",

            # Hindi

            r"यूट्यूब (?:पर|पे|में) (.+?) (?:सर्च करो|सर्च कर दो|सर्च)",

            r"यूट्यूब (?:पर|पे|में) (.+?) (?:ढूंढो|ढूंढिए|खोजो)",

            r"यूट्यूब (?:पर|पे|में) (.+?) खोलो",

            r"यूट्यूब (?:पर|पे|में) (.+)",

            r"यूट्यूब सर्च (.+)",

            r"सर्च यूट्यूब (.+)",

            r"यूट्यूब पर (.+?) खोजो",

            r"यूट्यूब पर (.+?) ढूंढो",

            r"यूट्यूब में (.+?) खोजो",

            r"यूट्यूब में (.+?) ढूंढो"
        ]

        for pattern in youtube_search_patterns:

            match = re.search(
                pattern,
                text
            )

            if match:

                query = match.group(1).strip()

                if query:

                    self.search_youtube(
                        query
                    )

                    return (
                        f"YouTube पर {query} "
                        "search कर रही हूँ।"
                    )

        # ==================================================
        # GOOGLE SEARCH
        # ==================================================

        google_patterns = [

            r"google (?:par|pe|me) (.+?) search karo",

            r"google (?:par|pe|me) (.+?) search kar do",

            r"google (?:par|pe|me) (.+)",

            r"search google (.+)",

            r"google search (.+)",

            # Hindi

            r"गूगल (?:पर|में) (.+?) सर्च करो",

            r"गूगल (?:पर|में) (.+?) सर्च कर दो",

            r"गूगल (?:पर|में) (.+)",

            r"गूगल पर (.+?) खोजो",

            r"गूगल में (.+?) खोजो",

            r"गूगल पर (.+?) ढूंढो",

            r"गूगल में (.+?) ढूंढो",

            r"गूगल (.+?) सर्च करो",

            # Hindi + English

            r"search करो (.+)",

            r"search कर दो (.+)",

            r"खोजो (.+)",

            r"ढूंढो (.+)"
        ]

        for pattern in google_patterns:

            match = re.search(
                pattern,
                text
            )

            if match:

                query = match.group(1).strip()

                if query:

                    self.search_google(
                        query
                    )

                    return (
                        f"Google पर {query} "
                        "search कर रही हूँ।"
                    )

        # ==================================================
        # YOUTUBE
        # ==================================================

        if any(x in text for x in [

            "youtube",
            "you tube",
            "यूट्यूब",
            "युटुब"

        ]):

            self.open_url(
                "https://www.youtube.com"
            )

            return (
                "YouTube ओपन कर रही हूँ।"
            )

        # ==================================================
        # YOUTUBE MUSIC
        # ==================================================

        if any(x in text for x in [

            "youtube music",
            "यूट्यूब म्यूजिक",
            "म्यूजिक खोलो"

        ]):

            self.open_url(
                "https://music.youtube.com"
            )

            return (
                "YouTube Music "
                "ओपन कर रही हूँ।"
            )

        # ==================================================
        # SPOTIFY
        # ==================================================

        if any(x in text for x in [

            "spotify",
            "स्पॉटिफाई"

        ]):

            self.open_url(
                "https://open.spotify.com"
            )

            return (
                "Spotify ओपन कर रही हूँ।"
            )

        # ==================================================
        # WHATSAPP
        # ==================================================

        if any(x in text for x in [

            "whatsapp",
            "what's app",
            "व्हाट्सएप",
            "व्हाट्स ऐप"

        ]):

            self.open_url(
                "https://web.whatsapp.com"
            )

            return (
                "WhatsApp ओपन कर रही हूँ।"
            )

        # ==================================================
        # INSTAGRAM
        # ==================================================

        if any(x in text for x in [

            "instagram",
            "इंस्टाग्राम"

        ]):

            self.open_url(
                "https://www.instagram.com"
            )

            return (
                "Instagram ओपन कर रही हूँ।"
            )

        # ==================================================
        # INSTAGRAM
        # ==================================================

        if any(x in text for x in [

            "निखिल का चैट ओपन करो"

        ]):

            self.open_url(
                "https://www.instagram.com/direct/t/17843120168906357/"
            )

            return (
                "Instagram पर निखिल का चैट ओपन कर रही हूँ।"
            )        

        # ==================================================
        # FACEBOOK
        # ==================================================

        if any(x in text for x in [

            "facebook",
            "फेसबुक"

        ]):

            self.open_url(
                "https://www.facebook.com"
            )

            return (
                "Facebook ओपन कर रही हूँ।"
            )

        # ==================================================
        # GMAIL
        # ==================================================

        if any(x in text for x in [

            "gmail",
            "जीमेल",
            "email",
            "ईमेल"

        ]):

            self.open_url(
                "https://mail.google.com"
            )

            return (
                "Gmail ओपन कर रही हूँ।"
            )

        # ==================================================
        # GOOGLE
        # ==================================================

        if text in [

            "google",
            "गूगल",
            "google kholo",
            "गूगल खोलो",
            "गूगल ओपन करो",
            "ओपन गूगल"

        ]:

            self.open_url(
                "https://www.google.com"
            )

            return (
                "Google ओपन कर रही हूँ।"
            )

        # ==================================================
        # WEATHER
        # ==================================================

        if any(x in text for x in [

            "weather",
            "weather kholo",
            "मौसम",
            "मौसम खोलो",
            "मौसम बताओ",
            "वेदर बताओ",
            "वेदर"

        ]):

            self.search_google(
                "weather in delhi"
            )

            return (
                "Weather ओपन कर रही हूँ।"
            )

        # ==================================================
        # NO ACTION
        # ==================================================

        return None