from typing import Tuple, List


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self,
            start: Tuple[int, int],
            end: Tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.desks = self.get_decks(start, end)
        self.is_drowned = is_drowned

    def get_decks(self,
                  start: Tuple[int, int],
                  end: Tuple[int, int]
                  ) -> List[Deck]:
        decks = []
        if start[0] < end[0]:
            for deck in range(start[0], end[0] + 1):
                decks.append(Deck(deck, end[1] + 1))
        elif start[1] < end[1]:
            for deck in range(start[1], end[1] + 1):
                decks.append(Deck(start[0], deck))
        else:
            decks.append(Deck(start[0], start[1]))
        return decks

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.desks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        desk = self.get_deck(row, column)
        if desk and desk.is_alive:
            desk.is_alive = False
            decks = [not desk.is_alive for desk in self.desks]
            if all(decks):
                return "Sunk!"
            else:
                return "Hit!"
        return "Miss!"


class Battleship:
    def __init__(self, ships: Tuple[int, int]) -> None:
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = {}
        self.populate_field()
        self.validate_field()

    def populate_field(self) -> None:
        for ship in self.ships:
            for deck in ship.desks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        if location in self.field:
            ship = self.field[location]
            result = ship.fire(location[0], location[1])
            if result == "Sunk!":
                for deck in ship.desks:
                    self.field[(deck.row, deck.column)].is_drownred = True
            return result
        return "Miss!"

    def print_field(self) -> None:
        field = [["~"] * 10 for _ in range(10)]
        for (row, column), ship in self.field.items():
            if ship.is_drowned:
                field[row][column] = "x"
            elif ship.get_deck(row, column).is_alive:
                field[row][column] = "\u25A1"
            else:
                field[row][column] = "*"
        for row in field:
            print(" ".join(row))

    def validate_field(self) -> None:
        ship_sizes = [len(ship.desks) for ship in self.ships]
        if len(ship_sizes) != 10:
            raise ValueError("There should be exactly 10 ships.")
        if ship_sizes.count(1) != 4:
            raise ValueError("There should be exactly 4 single-deck ships.")
        if ship_sizes.count(2) != 3:
            raise ValueError("There should be exactly 3 double-deck ships.")
        if ship_sizes.count(3) != 2:
            raise ValueError("There should be exactly 2 three-deck ships.")
        if ship_sizes.count(4) != 1:
            raise ValueError("There should be exactly 1 four-deck ship.")


# battle_ship = Battleship(
#     ships=[
#         ((0, 0), (0, 3)),
#         ((0, 5), (0, 6)),
#         ((0, 8), (0, 9)),
#         ((2, 0), (4, 0)),
#         ((2, 4), (2, 6)),
#         ((2, 8), (2, 9)),
#         ((9, 9), (9, 9)),
#         ((7, 7), (7, 7)),
#         ((7, 9), (7, 9)),
#         ((9, 7), (9, 7)),
#     ]
# )
#
# battle_ship.print_field()
