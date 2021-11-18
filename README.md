# TurningMachine

Przykładowe użycie w main. Wystarczy podać odpowiednie ścieżki.

W folderze tests w pliku tests.py można znaleźć odpowiednie testy jednostkowe. 

        def test_zad8_false(self):
        path = "D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine\\" \
               "tests\\example_zad8_false.txt"
        handler = InputHandler(path)
        model = ExerciseModel(handler.readFile())
        machine = Machine(model, debug=True)
        machine.solve()
        self.assertEqual("F", machine.current_state)

    def test_ilosc_jedynek_zer(self):
        """Test mający na celu sprawdzić czy
         maszyna poradzi sobie z zadaniem określającym tą
          samą ilość zer i jedynek."""

        path = "D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine\\" \
               "tests\\example_taka_sama_ilosc_zer_jedynek.txt"
        _, handler, model, machine = get_test_tuple(path)
        machine.debug = True
        machine.solve()
        machine.create_raport("raport_zad8.txt")

    def test_zad3(self):
        """nastepnik w alfabecie binarnym"""

        path = "D:\\Szymon\\STUDIA\\Algorytmika\\TurningMachine\\" \
               "tests\\example.zad3.txt"
        _, handler, model, machine = get_test_tuple(path)
        machine.debug = True
        machine.solve()
        machine.create_raport("raport_zad8.txt")


Powyższy kod pokazuje zastosowanie dla trzech wybranych zadań. 