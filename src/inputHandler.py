from dataclasses import dataclass


@dataclass
class InputHandler:
    filePath: str

    def readFile(self):
        with(open(self.filePath)) as file:
            content = file.read()
            return content
