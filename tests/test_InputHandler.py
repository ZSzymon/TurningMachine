from unittest import TestCase
from Machine.InputHandler import InputHandler

class TestInputHandler(TestCase):
    path = "D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine\\tests\\example.txt"
    handler = InputHandler(path)

    def test_read_file(self):
        content = self.handler.readFile()
        self.assertIsNotNone(content)


