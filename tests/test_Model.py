from unittest import TestCase

from src.InputHandler import InputHandler
from src.Model import *


class TestExerciseModel(TestCase):
    path = "D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine\\tests\\example.txt"
    handler = InputHandler(path)
    model = ExerciseModel(handler.readFile())

    def test_create_model_(self):
        self.assertIsNotNone(self.model)

    def test_init_description(self):
        self.assertEquals(self.model.description, "negacja")

    def test_init_states(self):
        self.assertEquals({"0", "1", "k"}, self.model.states)

    def test__init_instructions_list(self):
        instructionForZeroWhenOne = ['1', '0', '1', 'r']
        instructionForZeroWhenZero = ['0', '0', '1', 'r']
        instructionForZeroWhenEmpty = ['_', 'k', '_', 's']
        self.assertEquals(instructionForZeroWhenZero, self.model.instructions[('0', '0')].getAsList())
        self.assertEquals(instructionForZeroWhenOne, self.model.instructions[('0', '1')].getAsList())
        self.assertEquals(instructionForZeroWhenEmpty, self.model.instructions[('0', '_')].getAsList())

    def test__init_begin_state_(self):
        self.assertEquals("0", self.model.begin_state)

    def test__init_end_state_(self):
        self.assertEquals("k", self.model.end_state)

    def test__init_word_len_(self):
        self.assertEquals("6", self.model.word_len)

    def test__init_alphabet(self):
        self.assertEquals({"0", "1", "_"}, self.model.alphabet)

    def test__init_word_(self):
        self.assertEquals("011001", self.model.word)


class TestMachine(TestCase):
    path = "D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine\\tests\\example.txt"
    handler = InputHandler(path)
    model = ExerciseModel(handler.readFile())
    machine = Machine(model)


class TestMachineState(TestCase):
    path = "D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine\\tests\\example.txt"
    handler = InputHandler(path)
    model = ExerciseModel(handler.readFile())
    head = Head(model)

    def test_to_string(self):
        self.fail()

    def test_set_head_at_begin(self):
        self.head.set_head_at_begin()
        self.assertEqual(0, self.head.head_pos)
