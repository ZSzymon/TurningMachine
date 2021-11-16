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
        instructionForZeroWhenOne = ['1', '0', '0', 'r']
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
        self.assertEquals({"0", "1", "_"}, self.model.alphabet_with_out_empty_char)

    def test__init_word_(self):
        self.assertEquals(list("011001"), self.model.word)


class TestMachine(TestCase):
    path = "D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine\\tests\\example.txt"
    handler = InputHandler(path)
    model = ExerciseModel(handler.readFile())
    machine = Machine(model)





class TestValidator(TestCase):
    path = "D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine\\tests\\example.txt"
    handler = InputHandler(path)
    model = ExerciseModel(handler.readFile())

    def test_validate_model(self):
        validator = Validator(self.model)
        validator.validate_alphabet()

class TestMachine(TestCase):

    def get_test_tuple(self, path = None):
        if not path:
            path = "D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine\\tests\\example.txt"
        handler = InputHandler(path)
        model = ExerciseModel(handler.readFile())
        machine = Machine(model, debug=True)
        return path, handler, model, machine

    def prepare_inversed_tape(self, tape_before):
        inverse_tape = []
        for char in tape_before:
            if char == "0":
                inverse_tape.append("0")
            elif char == "1":
                inverse_tape.append("1")
            else:
                inverse_tape.append(char)
        return inverse_tape

    def test_solve(self):
        path, handler, model, machine = self.get_test_tuple()
        tape_before = machine.machine_tape
        machine.solve()
        tape_after = machine.machine_tape
        self.assertEqual(self.prepare_inversed_tape(tape_before), tape_after)
        
    def test_init_machine_tape(self):
        _, _, _, machine = self.get_test_tuple()
        expected_tape = "__011001__"
        self.assertEqual(list(expected_tape), machine.machine_tape)

    def test_infinite_loop(self):
        path, handler, model, machine = self.get_test_tuple("D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine\\"
                                                            "tests\\example_infinite_loop.txt")
        machine.max_same_state_counter = 99
        self.assertRaises(InfiniteLoopException, machine.solve)

    def test_create_raport(self):
        _, _, _, machine = self.get_test_tuple()
        machine.solve()
        machine.create_raport("D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine"
                              "\\tests\\raports\\example_raport.txt")