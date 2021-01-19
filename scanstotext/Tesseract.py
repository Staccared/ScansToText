import subprocess


class Tesseract:
    def __init__(self, language="deu", executable="/usr/bin/tesseract"):
        self.language = language
        self.executable = executable

    def extract_text(self, input_file):
        return self._extract(input_file, False)

    def _extract(self, input_file, hocr):
        cmd = [
            self.executable,
            input_file,
            "stdout",
            "-l",
            self.language,
        ]

        if hocr:
            cmd.append("hocr")

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=None)

        return result.stdout.decode()

