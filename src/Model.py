from __future__ import unicode_literals

from collections import defaultdict
from dataclasses import field, dataclass
from string import ascii_letters, whitespace, punctuation
from typing import Set, List


class Instruction:
    forChar: str
    next_state: str
    changeTo: str
    move_direction: str

    def __init__(self, line):
        splited = list(char for char in line.replace(",", ";").split(";") if not char.isspace())
        self.forChar = splited[0]
        self.next_state = splited[1]
        self.changeTo = splited[2]
        self.move_direction = splited[3]

    def getAsList(self):
        return [self.forChar, self.next_state, self.changeTo, self.move_direction]


class BedChar(Exception):
    """Not Valid character"""


@dataclass
class ExerciseModel:
    instructions = defaultdict()
    description: str = "Exercise description"
    states: Set[str] = field(default_factory=Set)
    alphabet_with_out_empty_char: Set[str] = field(default_factory=Set)
    word_len: int = 0
    word: List[str] = field(default_factory=List)
    end_state: str = "k"
    begin_state: str = "b"
    empty_char: str = "_"

    def __init__(self, raw_content):
        self._init_all(raw_content)
        pass

    def _init_all(self, raw_content):
        lines = raw_content.split("\n")
        self._init_description_(lines[0])
        self._init_state_list(lines[1])
        self._init_empty_char(lines[2])
        self._init_alphabets(lines[2])
        self._init_word_len_(lines[3])
        self._init_word_(lines[4])
        self._init_end_state_(lines[5])
        self._init_begin_state_(lines[6])
        self._init_instructions_list(lines[8:])

    def _init_instructions_list(self, instruction_lines):
        alphabet_len = len(self.alphabet_with_out_empty_char)
        "alphabet_len-1 because there will be alphabet - 1" \
        " instruction list for each char in alphabet without '_'"
        counter = 0
        instructions = defaultdict(Instruction)
        for i in range(alphabet_len - 1):
            state = instruction_lines[counter].split(":")[0]
            counter += 1
            for j in range(alphabet_len):
                instruction_line = instruction_lines[counter]
                instruction = Instruction(instruction_line)
                instructions[state, instruction.forChar] = instruction
                counter += 1

        self.instructions = instructions

    def _init_begin_state_(self, line):
        self.begin_state = line.split(":")[1].replace(" ", "")

    def _init_end_state_(self, line):
        self.end_state = line.split(":")[1].replace(" ", "")

    def _init_word_len_(self, line):
        self.word_len = line.split(":")[1].replace(" ", "")

    def _init_description_(self, line):
        description = [char for char in line.split(":")[1] if char in ascii_letters]
        self.description = "".join(description)

    def _init_state_list(self, line):
        states = set()
        for state in line.split(":")[1].split(","):
            if state not in whitespace:
                states.add("".join(state.split()))
        self.states = states

    def _init_alphabets(self, line):
        self.alphabet_with_out_empty_char = set()

        def can_add(char):
            return char == self.empty_char or \
                   (not char.isspace() and char not in punctuation) or False

        for char in line.split(":")[1]:
            if can_add(char):
                self.alphabet_with_out_empty_char.add(char)

        self.alphabet = self.alphabet_with_out_empty_char
        self.alphabet.add(self.empty_char)

    def _init_word_(self, line):
        self.word = [char for char in line.split(":")[1].replace(" ", "")]
        pass

    def _init_empty_char(self, line):
        """ I assume that the last char in alphabet represent empty char.
        :return:
        """
        self.empty_char = line.split(":")[1][-1]


@dataclass
class Validator():
    model: ExerciseModel = None

    def validate_model(self):
        self.validate_alphabet()

    def validate_alphabet(self):
        word = self.model.word
        for char in word:
            if char not in self.model.alphabet:
                raise BedChar(f"Character {char} not in alphabet: {self.model.alphabet}")


class MachineState:
    stepCounter: int
    current_state: str
    head_pos: int
    machine_tape_state: List[str]
    empty_chars = int

    def __init__(self, current_state, head_pos, machine_tape_state):
        self.current_state = current_state
        self.head_pos = head_pos
        self.machine_tape_state = machine_tape_state

    def __str__(self) -> str:
        return self.to_string()

    def to_string(self):
        state = " " * self.head_pos + "|" + "  "
        state += "state: " + self.current_state + "\n"
        state += "".join(self.machine_tape_state) + "\n"
        return state


class Head:
    head_pos: int

    def __init__(self, head_pos):
        self.head_pos = head_pos

    def read_char(self, machine_tape):
        char = machine_tape[self.head_pos]
        return char

    def write_char(self, machine_tape, char_to_write):
        machine_tape[self.head_pos] = char_to_write
        return machine_tape

    def goRight(self):
        self.head_pos += 1

    def go(self, direction):
        if direction == "r":
            self.goRight()
        if direction == "l":
            self.goLeft()
        if direction == "s":
            pass

    def goLeft(self):
        self.head_pos -= 1


class Machine:
    model: ExerciseModel
    current_state: str
    next_state: str
    head: Head
    machine_tape: List[str]
    machine_states: list
    same_state_for: int = 0

    def get_machine_state(self):
        return MachineState(self.current_state, self.head.head_pos, self.machine_tape)

    def __init__(self, model):
        self.begin_state = model.begin_state
        self.model = model

        self._init_machine_tape()
        self.current_state = model.begin_state
        self.head = Head(self.get_index_first_not_empty_char())
        self.machine_states = []

    def _init_machine_tape(self):
        two_empty_chars = list(2 * self.model.empty_char)
        self.machine_tape = two_empty_chars + list(self.model.word) + two_empty_chars

    def get_index_first_not_empty_char(self):
        empty_char = self.model.empty_char
        for i, char in enumerate(self.machine_tape):
            if char != empty_char:
                return i
        return -1

    def is_in_end_state(self):
        return self.current_state == self.model.end_state

    def prevent_infinite_loop(self, next_state):
        """Count number of same state for every loop"""
        if self.current_state == next_state:
            self.same_state_for += 1
        else:
            self.same_state_for = 0
        self.same_state_for = 0 if self.current_state != next_state else self.same_state_for + 1

    def solve(self, debug=True):
        """run run run."""
        is_solved = self.is_in_end_state()
        while not is_solved:
            current_machine_state = self.get_machine_state()
            if debug:
                print(current_machine_state)
            self.machine_states.append(current_machine_state)
            current_char = self.head.read_char(self.machine_tape)
            if debug:
                current_state = self.current_state
            instruction = self.model.instructions[(self.current_state, current_char)]
            self.machine_tape = self.head.write_char(self.machine_tape, instruction.changeTo)
            self.current_state = instruction.next_state
            self.head.go(instruction.move_direction)
            is_solved = self.is_in_end_state()

        if debug:
            current_machine_state = self.get_machine_state()
            print(current_machine_state)
