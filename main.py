from src.inputHandler import InputHandler
from src.machine import Machine
from src.model import ExerciseModel

if __name__ == '__main__':
    #lot's of examples in tests directory.

    path = ...
    handler = InputHandler(path)
    model = ExerciseModel(handler.readFile())
    ##debug = True output of process to std.

    machine = Machine(model, debug=True)
    machine.solve()
    #optional.
    machine.create_raport(raport_path=...)
