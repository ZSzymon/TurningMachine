from __future__ import unicode_literals

from collections import defaultdict
from dataclasses import field, dataclass
from string import ascii_letters, whitespace, punctuation
from typing import Set


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
    empty_char: str = "_"

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
    empty_chars = int

    def __init__(self, current_state, head_pos, tape):
        self.current_state = current_state
        self.head_pos = head_pos
        global machineTape
        machineTape = tape

    def __str__(self) -> str:
        return self.to_string()

    def to_string(self):
        state = " " * self.head_pos
        state += "state: " + self.current_state + "\n"
        state += self.tape + "\n"
        return state


class Head:
    head_pos: int

    def __init__(self, head_pos):
        self.head_pos = head_pos

    def readChar(self):
        char = machineTape[self.head_pos]
        return char

    def writeChar(self, char_to_write):
        machineTape[self.head_pos] = char_to_write

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

    def set_head_at_begin(self):
        self.head_pos = 0


class Machine:
    model: ExerciseModel
    current_state: str
    next_state: str
    head: Head
    tape: str
    machine_states: list

    def getMachineState(self):
        return MachineState(self.current_state, self.head.head_pos, self.tape)

    def __init__(self, model):
        self.begin_state = model.begin_state
        self.model = model
        self.current_state = model.begin_state
        self.head = Head(self.get_index_first_not_empty_char())
        self.head.set_head_at_begin()
        self.machine_states = []

    def get_index_first_not_empty_char(self):
        empty_char = self.model.empty_char
        for i, char in enumerate(self.model.word):
            if char == empty_char:
                return i

    def is_in_end_state(self):
        return self.current_state == self.model.end_state

    def solve(self, debug=True):
        """run run run."""
        cond = True
        while cond:

            currentMachineState = self.getMachineState()
            if debug:
                print(currentMachineState)
            self.machine_states.append(currentMachineState)
            currentChar = self.head.readChar()
            instruction = self.model.instructions[(self.current_state, currentChar)]
            self.head.writeChar(instruction.changeTo)
            self.current_state = instruction.nextState
            self.head.go(instruction.moveDirection)
