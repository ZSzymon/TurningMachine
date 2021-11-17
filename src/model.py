from __future__ import unicode_literals
from collections import defaultdict
from dataclasses import field, dataclass
from string import ascii_letters, whitespace, punctuation
from typing import Set, List
from .exceptions import *


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


@dataclass
class ExerciseModel:
    instructions = defaultdict()
    description: str = "Exercise description"
    states: Set[str] = field(default_factory=Set)
    alphabet_with_out_empty_char: Set[str] = field(default_factory=Set)
    word_len: int = 0
    word: List[str] = field(default_factory=List)
    end_states: str = "k"
    begin_state: str = "b"
    empty_char: str = "_"

    def __init__(self, raw_content):
        self._init_all(raw_content)
        stop = 1
        self.validate()
        pass

    def validate(self):
        validator = Validator(self)
        validator.validate_model()

    def _init_all(self, raw_content):
        lines = raw_content.split("\n")
        self._init_description_(lines[0])
        self._init_states(lines[1])
        self._init_empty_char(lines[2])
        self._init_alphabets(lines[2])
        self._init_word_len_(lines[3])
        self._init_word_(lines[4])
        self._init_end_state_(lines[5])
        self._init_begin_state_(lines[6])
        self._init_instructions_list(lines[8:])

    def _init_instructions_list(self, instruction_lines):

        alphabet_len = len(self.alphabet)
        """There is (states - end_states)*alphabet instructions."""
        states_len = len(self.states) - len(self.end_states)
        counter = 0
        instructions = defaultdict(Instruction)
        try:
            for i in range(states_len):
                state = instruction_lines[counter].split(":")[0]
                counter += 1
                for j in range(alphabet_len):
                    instruction_line = instruction_lines[counter]
                    instruction = Instruction(instruction_line)
                    instructions[state, instruction.forChar] = instruction
                    counter += 1
        except IndexError as e:
            print(e)
            print("Possible not enough instructions for given alphabet/states.")
        self.instructions = instructions

    def _init_begin_state_(self, line):
        self.begin_state = line.split(":")[1].replace(" ", "")

    def _init_end_state_(self, line):
        self.end_states = line.split(":")[1].replace(" ", "").split(",")

    def _init_word_len_(self, line):
        self.word_len = line.split(":")[1].replace(" ", "")

    def _init_description_(self, line):
        description = [char for char in line.split(":")[1] if char in ascii_letters or char.isspace()]
        self.description = "".join(description)

    def _init_states(self, line):
        states = set()
        for state in line.split(":")[1].split(","):
            if state not in whitespace:
                states.add("".join(state.split()))
        self.states = states

    def _init_alphabets(self, line):
        self.alphabet_with_out_empty_char = set()
        def can_add(character):
            return character not in [",",";",":"] and not character.isspace()

        for char in line.split(":")[1]:
            if can_add(char):
                self.alphabet_with_out_empty_char.add(char)

        self.alphabet = set(symbol for symbol in self.alphabet_with_out_empty_char)
        self.alphabet.add(self.empty_char)
        stop = 1

    def _init_word_(self, line):
        self.word = [char for char in line.split(":")[1].replace(" ", "")]
        pass

    def _init_empty_char(self, line):
        """ I assume that the last char in alphabet represent empty char.
        """
        self.empty_char = line.split(":")[1][-1]


class MachineState:
    stepCounter: int
    current_state: str
    head_pos: int
    machine_tape_state: List[str]
    empty_chars = int

    def __init__(self, current_state, head_pos, machine_tape_state):
        self.current_state = current_state
        self.head_pos = head_pos
        self.machine_tape_state = [char for char in machine_tape_state]

    def __str__(self) -> str:
        return self.to_string()

    def to_string(self):
        state = " " * self.head_pos + "|" + "  "
        state += "state: " + self.current_state + "\n"
        state += "".join(self.machine_tape_state) + "\n"
        return state




@dataclass
class Validator:
    model: ExerciseModel = None

    def validate_model(self):
        self.validate_word()
        self.validate_instructions()

    def validate_word(self):
        word = self.model.word
        for char in word:
            if char not in self.model.alphabet:
                raise BadChar(f"Character {char} not in alphabet: {self.model.alphabet}")

    def validate_instructions(self):
        """Check is end state possible to approach"""

        if not any(instruction.next_state in self.model.end_states for instruction in self.model.instructions.values()):
            raise EndStateNotException("There is not way to go in to end state.")
