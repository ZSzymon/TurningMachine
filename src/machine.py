from .exceptions import *
from .model import *

class Head:
    head_pos: int
    tape_len: int

    def __init__(self, head_pos, tape_len):
        self.head_pos = head_pos
        self.tape_len = tape_len

    def read_char(self, machine_tape):
        char = machine_tape[self.head_pos]
        return char

    def write_char(self, machine_tape, char_to_write):
        machine_tape[self.head_pos] = char_to_write
        return machine_tape

    def go(self, direction):
        if direction == "r":
            self.goRight()
        elif direction == "l":
            self.goLeft()
        elif direction == "s" or direction == "_":
            self.goNoWhere()
        else:
            raise NotImplementedHeadMoveException(f"The {direction} is not supported.\n"
                                                  f"Supported directions:\n"
                                                  f"r - right\n"
                                                  f"l - left\n"
                                                  f"s - stop\n")

    def goNoWhere(self):
        pass

    def goLeft(self):
        if self.head_pos < 0:
            raise OutOfTapeHeadException("Head moved out of tape in left direction.\nCheck given instructions")
        self.head_pos -= 1

    def goRight(self):
        if self.head_pos > self.tape_len:
            raise OutOfTapeHeadException("Head moved out of tape in right direction.\nCheck given instructions")
        self.head_pos += 1


class Machine:
    max_same_state_counter: int = 99999
    model: ExerciseModel
    current_state: str
    next_state: str
    head: Head
    machine_tape: List[str]
    machine_states: list
    same_state_counter: int = 0

    def get_machine_state(self):
        return MachineState(self.current_state, self.head.head_pos, self.machine_tape)

    def __init__(self, model, debug=False):
        self.begin_state = model.begin_state
        self.model = model
        self.debug = debug
        self._init_machine_tape()
        self.current_state = model.begin_state
        self.head = Head(self.get_index_first_not_empty_char(), len(self.machine_tape))
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
        return self.current_state in self.model.end_states

    def prevent_infinite_loop(self, next_state):
        """Count number of same state for every loop"""
        if self.current_state == next_state:
            self.same_state_counter += 1
        else:
            self.same_state_counter = 0
        self.same_state_counter = 0 if self.current_state != next_state else self.same_state_counter + 1

        if self.same_state_counter > self.max_same_state_counter:
            raise InfiniteLoopException("Machine is not able to end state.\n"
                                        "Machine is in same state to long.\n"
                                        "Check given instructions.")

    def solve(self):
        """run run run."""
        is_solved = self.is_in_end_state()
        while not is_solved:
            if self.debug:
                print(self.get_machine_state())

            self.machine_states.append(self.get_machine_state())
            current_char = self.head.read_char(self.machine_tape)
            instruction = self.model.instructions[(self.current_state, current_char)]
            self.machine_tape = self.head.write_char(self.machine_tape, instruction.changeTo)
            self.prevent_infinite_loop(instruction.next_state)
            self.current_state = instruction.next_state
            self.head.go(instruction.move_direction)
            is_solved = self.is_in_end_state()
        if self.debug:
            current_machine_state = self.get_machine_state()
            print(current_machine_state)

    def create_raport(self, raport_path):
        machine_state_first = (self.machine_states[:1] or [None])[0]
        machine_state_second = (self.machine_states[-1:] or [None])[0]
        machine_tape_before = "".join(machine_state_first.machine_tape_state[2:-2])
        machine_tape_after = "".join(machine_state_second.machine_tape_state[2:-2]) \
            if machine_state_second else machine_tape_before

        with open(raport_path, "w") as raport:
            raport.write("Word before: " + machine_tape_before + "\n")
            raport.write("Description: " + self.model.description + "\n")
            raport.write("Word after: " + machine_tape_after + "\n")
