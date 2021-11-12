from __future__ import unicode_literals

from collections import defaultdict
from dataclasses import field, dataclass
from typing import List, Tuple, Dict, Set
from string import ascii_letters, whitespace, punctuation


class Instruction:
    forChar: str
    nextState: str
    changeTo: str
    moveDirection: str

    def __init__(self, line):
        splited = list(char for char in line.replace(",", ";").split(";") if not char.isspace())
        self.forChar = splited[0]
        self.nextState = splited[1]
        self.changeTo = splited[2]
        self.moveDirection = splited[3]

    def getAsList(self):
        return [self.forChar, self.nextState, self.changeTo, self.moveDirection]


@dataclass
class ExerciseModel:
    instructions = defaultdict()
    description: str = "Exercise description"
    states: Set[str] = field(default_factory=Set)
    alphabet: Set[str] = field(default_factory=Set)
    word_len: int = 0
    word: str = ""
    end_state: str = "k"
    begin_state: str = "b"

    def __init__(self, raw_content):
        self._init_all(raw_content)
        pass

    def _init_all(self, raw_content):
        lines = raw_content.split("\n")
        self._init_description_(lines[0])
        self._init_state_list(lines[1])
        self._init_alphabet(lines[2])
        self._init_word_len_(lines[3])
        self._init_word_(lines[4])
        self._init_end_state_(lines[5])
        self._init_begin_state_(lines[6])
        self._init_instructions_list(lines[8:])

    def _init_instructions_list(self, instruction_lines):
        alphabet_len = len(self.alphabet)
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

    def _init_alphabet(self, line):
        self.alphabet = set()

        def can_add(char):
            return char == "_" or \
                   (not char.isspace() and char not in punctuation) or False

        for char in line.split(":")[1]:
            if can_add(char):
                self.alphabet.add(char)

    def _init_word_(self, line):
        self.word = line.split(":")[1].replace(" ", "")
        pass


class MachineState:
    stepCounter: int
    current_state: str
    head_pos: int
    tape: str
    def print_state(self):

    pass


class Machine:
    model: ExerciseModel
    current_state: str
    next_state: str
    head_pos: int
    tape: str
    machine_states: list
    def __init__(self, model):
        self.model = model

    def solve(self, debug = True):



