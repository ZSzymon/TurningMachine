from unittest import TestCase
from src.inputHandler import InputHandler
from src.machine import *


def get_test_tuple(path=None):
    if not path:
        path = "D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine\\tests\\example.txt"
    handler = InputHandler(path)
    model = ExerciseModel(handler.readFile())
    machine = Machine(model, debug=True)
    return path, handler, model, machine


class TestExerciseModel(TestCase):


    def test_create_model_(self):
        self.assertIsNotNone(self.model)

    def test_init_description(self):
        path, handler, model, machine = get_test_tuple()
        self.assertEquals(model.description, "negacja")

    def test_init_states(self):
        self.assertEquals({"0", "1", "k"}, self.model.states)

    def test__init_instructions_list(self):
        instructionForZeroWhenOne = ['1', '0', '0', 'r']
        instructionForZeroWhenZero = ['0', '0', '1', 'r']
        instructionForZeroWhenEmpty = ['_', 'k', '_', 's']
        path, handler, model, machine = get_test_tuple()
        self.assertEquals(instructionForZeroWhenZero, model.instructions[('0', '0')].getAsList())
        self.assertEquals(instructionForZeroWhenOne, model.instructions[('0', '1')].getAsList())
        self.assertEquals(instructionForZeroWhenEmpty, model.instructions[('0', '_')].getAsList())

    def test__init_begin_state_(self):
        path, handler, model, machine = get_test_tuple()
        self.assertEquals("0", model.begin_state)

    def test__init_end_state_(self):
        path, handler, model, machine = get_test_tuple()
        self.assertEquals("k", model.end_states)

    def test__init_word_len_(self):
        path, handler, model, machine = get_test_tuple()
        self.assertEquals("6", model.word_len)

    def test__init_alphabet(self):
        path, handler, model, machine = get_test_tuple()
        self.assertEquals({"0", "1", "_"}, model.alphabet_with_out_empty_char)

    def test__init_word_(self):
        path, handler, model, machine = get_test_tuple()
        self.assertEquals(list("011001"), model.word)



class TestValidator(TestCase):
    #path = "D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine\\tests\\example.txt"
    #handler = InputHandler(path)
    #model = ExerciseModel(handler.readFile())

    def test_validate_model_success(self):
        _, _, model, _ = get_test_tuple()
        validator = Validator(model)
        validator.validate_word()

    def test_validate_alphabet_model_failure(self):
        #inside of model is creating Validator
        file_with_wrong_alphabet = "D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine\\tests\\example_wrong_alphabet.txt"
        with self.assertRaises(BedChar):
            _, _, model, _ = get_test_tuple(file_with_wrong_alphabet)

    def test_validate_instructions_failure(self):
        file_with_wrong_instructions = "D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine\\tests" \
                                   "\\example_wrong_instructions.txt "
        with self.assertRaises(EndStateNotException):
            _, _, model, _ = get_test_tuple(file_with_wrong_instructions)


class TestMachine(TestCase):

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
        path, handler, model, machine = get_test_tuple()
        tape_before = machine.machine_tape
        machine.solve()
        tape_after = machine.machine_tape
        self.assertEqual(self.prepare_inversed_tape(tape_before), tape_after)

    def test_init_machine_tape(self):
        _, _, _, machine = get_test_tuple()
        expected_tape = "__011001__"
        self.assertEqual(list(expected_tape), machine.machine_tape)

    def test_infinite_loop(self):
        path, handler, model, machine = get_test_tuple("D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine\\"
                                                       "tests\\example_infinite_loop.txt")
        machine.max_same_state_counter = 99

        self.assertRaises(InfiniteLoopException, machine.solve)

    def test_create_raport(self):
        _, _, _, machine = get_test_tuple()
        machine.solve()
        machine.create_raport("D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine"
                              "\\tests\\raports\\example_raport.txt")

    def test_zad8(self):
        path = "D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine\\" \
               "tests\\example_zad8.txt"
        handler = InputHandler(path)
        model = ExerciseModel(handler.readFile())
        machine = Machine(model, debug=True)
        machine.solve()
        self.assertEqual("T",machine.current_state)

    def test_zad8_false(self):
        path = "D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine\\" \
               "tests\\example_zad8_false.txt"
        handler = InputHandler(path)
        model = ExerciseModel(handler.readFile())
        machine = Machine(model, debug=True)
        machine.solve()
        self.assertEqual("F", machine.current_state)

