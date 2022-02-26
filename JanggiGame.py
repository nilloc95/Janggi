# Name: Collin Gilmore
# Date: 2/11/2021
# Description:  This program contains classes and methods to play the board game Janggi. The game can be created by
#               calling the JanggiGame class. It will initialize 2 team - red and blue. It will create a virtual board
#               with each teams pieces in the correct starting positions. Blue team starts. A player may make a move
#               by calling the make_move() method on the JanggiGame class by entering a starting position and ending
#               position for whichever piece they want to move (horizontal axis = a - i, vertical = 1 - 10). It will
#               validate that the piece chosen is owned by whoever's turn it is, it will also validate that it is a
#               legal move based on that pieces move set, and there are no pieces obstructing its path and does not land
#               on a piece of the same team. a player can pass their turn by moving to the same position they are
#               already in. Each successful move made by a player will check to see if the opposing team has been put in
#               check. If a team is in check they must move to get themselves out of check. If there are no legal moves
#               to remove themselves from check, then they are in checkmate and the opposing team wins, which will be
#               updated in the game-state and make_move() method will no longer work and return False.


class JanggiGame:
    """
    This class represents a board game called Janggi
    """

    def __init__(self):
        """
        This will initialize the game. It sets the initial state to UNFINISHED. It initializes the red and blue team
        by using the Red and Blue classes and their respective get_pieces methods which return each individual piece as
        an object that also have associated methods. It initializes the player turn to be blue to start. It initializes
        an empty board using '-------' as placeholders for empty spots. It also calls update board to set the initial
        placements for each piece
        """
        self._game_state = 'UNFINISHED'
        self._red_pieces = Red().get_red_pieces()
        self._blue_pieces = Blue().get_blue_pieces()
        self._player_turn = 'blue'
        self._board = \
            [
                ['-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------'],
                ['-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------'],
                ['-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------'],
                ['-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------'],
                ['-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------'],
                ['-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------'],
                ['-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------'],
                ['-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------'],
                ['-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------'],
                ['-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------', '-------'],
            ]
        self.update_board()

    def print_board(self):
        """
        This method is used to visualize the board and the pieces in an easy to view way. It starts by calling
        update_board() to ensure it has all piece locations updated
        """
        self.update_board()
        index = 0
        print('_______________________________________________________________________________________________________'
              '_____')
        print('        a          b            c           d          e           f           g            h           '
              'i\n_____________________________________________________________________________________________________'
              '_______')
        length = [10 for i in range(9)]

        for item in self._board:
            if index + 1 != 10:
                print('', str(index + 1) + '|', end='  ')
            else:
                print(str(index + 1) + '|', end='  ')
            for idx in range(len(length)):
                if item[idx] == '-------':
                    name = '-------'
                else:
                    name = item[idx].get_name()
                print(name.ljust(length[idx]), end='  ')
            index += 1
            print()

    def change_player_turn(self):
        """Changes the players turn to red or blue depending on who went last"""
        if self._player_turn == 'blue':
            self._player_turn = 'red'
        else:
            self._player_turn = 'blue'

    def get_item_from_location(self, location):
        """Takes a current location (a1, b6, etc.) and returns the item at that location on the board"""
        location = self.convert_position(location)
        return self._board[location[0]][location[1]]

    def make_move(self, current_location, new_location):
        """
        takes a current location and new location and moves the desired piece if it is a legal move.
        Also, it will check if the games state needs to be updated. It will return False if the move is not legal
        or if one team has already won. It will return True on a successful move and call change_player_turn()
        """
        item_to_move = self.get_item_from_location(current_location)
        if item_to_move == "-------" or item_to_move.get_team() != self._player_turn:
            print("Illegal move, please try again. It's currently " + self._player_turn + "'s turn")
            return False

        if self._game_state != 'UNFINISHED':
            print(self._game_state)
            return False

        current = self.convert_position(current_location)
        new = self.convert_position(new_location)
        if self._player_turn == 'red':
            if self.is_legal(item_to_move, current, new):
                if self._board[new[0]][new[1]] != '-------' and self._board[new[0]][new[1]] != item_to_move:
                    self.remove_piece('blue', new_location)
                item_to_move.set_position(new)
                self._board[current[0]][current[1]] = '-------'
                self.change_player_turn()
                self.update_board()
                if self.is_in_check('blue'):
                    if self.check_mate('blue'):
                        self._game_state = 'RED_WON'
                return True
            else:
                print("Illegal move, please try again. It's currently " + self._player_turn + "'s turn")
                return False
        elif self._player_turn == 'blue':
            if self.is_legal(item_to_move, current, new):
                if self._board[new[0]][new[1]] != '-------' and self._board[new[0]][new[1]] != item_to_move:
                    self.remove_piece('red', new_location)
                item_to_move.set_position(new)
                self._board[current[0]][current[1]] = '-------'
                self.change_player_turn()
                self.update_board()
                if self.is_in_check('red'):
                    if self.check_mate('red'):
                        self._game_state = 'BLUE_WON'
                return True
            else:
                print("Illegal move, please try again. It's currently " + self._player_turn + "'s turn")
                return False

    def update_board(self):
        """
        This method will loop through all the red and blue pieces and check their locations and
        update the board accordingly
        """
        for item in self._red_pieces:
            column = item.get_position()[0]
            row = item.get_position()[1]
            self._board[column][row] = item

        for item in self._blue_pieces:
            column = item.get_position()[0]
            row = item.get_position()[1]
            self._board[column][row] = item

    def is_in_check(self, team):
        """
        This method will check if a team is in check. The "team" parameter must be either 'red' or 'blue'.
        It will check all the opposing teams pieces to see if they have any legal moves that would land them on the
        general of the team passed as a parameter. Returns True if that team is in check and False if not.
        """

        # see if red is in check --> loop through other teams pieces and see if any of them have valid moves to land on
        # the red team's general
        if team == 'red':
            red_general_location = []
            for item in self._red_pieces:
                if item.get_name() == 'rGeneral':
                    red_general_location = item.get_position()
                    break
            for item in self._blue_pieces:
                current = item.get_position()
                if item.check_move(current, red_general_location, self._board):
                    return True
        # see if blue is in check --> loop through other teams pieces and see if any of them have valid moves to land
        # on the blue team's general
        if team == 'blue':
            blue_general_location = []
            for item in self._blue_pieces:
                if item.get_name() == 'bGeneral':
                    blue_general_location = item.get_position()
                    break
            for item in self._red_pieces:
                current = item.get_position()
                if item.check_move(current, blue_general_location, self._board):
                    return True
        return False

    def check_mate(self, team):
        """
        This method will be called if a team is in check. It will loop through all possible player movement options and
        see if there are any legal moves that will take them out of being in check. If they have no moves that can bring
        them out of being in check, they are in check mate and they lose the game. Returns True if they are in
        check mate and False otherwise. It will update the game state to reflect who has won the game.
        """
        if self.is_in_check(team):

            # Check Red Team pieces
            if team == 'red':
                for piece in self._red_pieces:
                    current = piece.get_position()

                    # Loop through every possible location on the board and see if its a valid move, if it is, see if it
                    # will take them out of check
                    new = [0, 0]
                    while new[0] < 10 and new[1] < 9:
                        if piece.check_move(current, new, self._board):
                            piece.set_position(new)
                            if self.is_in_check(team):
                                piece.set_position(current)
                            else:
                                piece.set_position(current)
                                return False
                        if new[1] == 8:
                            new[1] = 0
                            new[0] += 1
                        else:
                            new[1] += 1
            # Check Blue team pieces
            else:
                # Loop through each piece and see if any moves are available to get them out of being in check
                for piece in self._blue_pieces:
                    current = piece.get_position()

                    # Loop through every possible location on the board and see if its a valid move, if it is, see if it
                    # will take them out of check
                    new = [0, 0]
                    while new[0] < 10 and new[1] < 9:
                        if piece.check_move(current, new, self._board):
                            piece.set_position(new)
                            if self.is_in_check(team):
                                piece.set_position(current)
                            else:
                                piece.set_position(current)
                                return False
                        if new[1] == 8:
                            new[1] = 0
                            new[0] += 1
                        else:
                            new[1] += 1
                return True
        else:
            return False

    def is_legal(self, item, current, new):
        """
        This method will check if a move entered into make_move() is a legal move. It will use the same current and
        new location from make_move() to determine this. It will utilize the defined move set of the piece at the
        current location and go through the board to determine if the move is legal.
        """
        current_team = item.get_team()

        if type(self._board[new[0]][new[1]]) is not str:  # check if the location to move to is empty or not
            new_team = self._board[new[0]][new[1]].get_team()  # Says str has no method get_team(), the item it
                                                                # references should never be a string
            if current == new:  # check if they are not moving/ passing
                if self.is_in_check(current_team):
                    return False
                return True
            if current_team == new_team:  # make sure they can't move to their team pieces
                return False
        if item.check_move(current, new, self._board):
            item.set_position(new)
            if self.is_in_check(current_team):
                item.set_position(current)
                return False
            return True
        else:
            return False

    def get_game_state(self):
        """returns the current game state"""
        return self._game_state

    def convert_position(self, position):
        """
        takes a position as a string with a letter and number for columns and rows.
        Converts it to an array used for coordinates. This method is static, but needed to be a class method
        as required in the the documentation
        """
        temp_position = [int(position[1:]) - 1, 0]
        if position[0] == 'a':
            temp_position[1] = 0
        if position[0] == 'b':
            temp_position[1] = 1
        if position[0] == 'c':
            temp_position[1] = 2
        if position[0] == 'd':
            temp_position[1] = 3
        if position[0] == 'e':
            temp_position[1] = 4
        if position[0] == 'f':
            temp_position[1] = 5
        if position[0] == 'g':
            temp_position[1] = 6
        if position[0] == 'h':
            temp_position[1] = 7
        if position[0] == 'i':
            temp_position[1] = 8
        return temp_position

    def remove_piece(self, team, position):
        """removes a piece from the teams list of pieces. Returns True if item is removed, and False otherwise"""
        position = self.convert_position(position)
        piece = self._board[position[0]][position[1]]
        if team == 'blue':
            for item in self._blue_pieces:
                if item == piece:
                    self._blue_pieces.remove(item)
                    self._board[position[0]][position[1]] = '-------'
                    self.update_board()
                    return True
            return False
        else:
            for item in self._red_pieces:
                if item == piece:
                    self._red_pieces.remove(item)
                    self._board[position[0]][position[1]] = '-------'
                    self.update_board()
                    return True
            return False


# The 'Piece' class is the parent to all the individual piece type classes and they all inherit from this class
class Piece:
    """
    Represents a board piece, each piece will inherit this class and build upon it for its own specifications
    """

    def __init__(self, team, position):
        """
        initializes board piece. The team and position will be specified in the Red and Blue classes.
        type, name, and move set will be specified by the class piece that inherits the functionality
        """
        self._team = team
        self._position = position
        self._type = None
        self._name = None
        self._move_set = None
        if team == 'red':
            self._palace = [[0, 3], [0, 4], [0, 5], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5]]
            self._enemy_palace = [[7, 3], [7, 4], [7, 5], [8, 3], [8, 4], [8, 5], [9, 3], [9, 4], [9, 5]]
        else:
            self._palace = [[7, 3], [7, 4], [7, 5], [8, 3], [8, 4], [8, 5], [9, 3], [9, 4], [9, 5]]
            self._enemy_palace = [[0, 3], [0, 4], [0, 5], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5]]

    def get_name(self):
        """returns the name of the board piece"""
        return self._name

    def get_position(self):
        """returns the current position for the board piece"""
        return self._position

    def get_move_set(self):
        """returns self._move_set"""
        return self._move_set

    def set_position(self, new_position):
        """
        takes an array for column and row and updates the current piece's position.
        Should only be used after convert_position has been used to convert the position to an array
        """
        self._position = new_position

    def get_type(self):
        """returns the item type"""
        return self._type

    def get_team(self):
        """returns team name"""
        return self._team

    def get_team_palace(self):
        """returns the palace for the team they are on"""
        return self._palace

    def get_enemy_palace(self):
        """returns the the enemy palace locations"""
        return self._enemy_palace

    def is_in_team_palace(self, current, new):
        """if a piece is in the palace, they can call this function to allow for their additional move set"""
        if new not in self._palace:
            return False
        else:
            if current[0] == new[0]:
                if current[1] + 1 == new[1]:
                    return True
                if current[1] - 1 == new[1]:
                    return True
            if current[1] == new[1]:
                if current[0] + 1 == new[0]:
                    return True
                if current[0] - 1 == new[0]:
                    return True
            if [current[0] + 1, current[1] + 1] == new or [current[0] + 1, current[1] + -1] == new \
                    or [current[0] - 1, current[1] + 1] == new or [current[0] - 1, current[1] - 1] == new:
                return True

    def is_in_enemy_palace(self, current, new):
        """if a piece is in the palace, they can call this function to allow for their additional move set"""
        if new not in self._enemy_palace:
            return False
        else:
            if current[0] == new[0]:
                if current[1] + 1 == new[1]:
                    return True
                if current[1] - 1 == new[1]:
                    return True
            if current[1] == new[1]:
                if current[0] + 1 == new[0]:
                    return True
                if current[0] - 1 == new[0]:
                    return True
            if [current[0] + 1, current[1] + 1] == new or [current[0] + 1, current[1] + -1] == new \
                    or [current[0] - 1, current[1] + 1] == new or [current[0] - 1, current[1] - 1] == new:
                return True


class Chariot(Piece):
    """
    Represents a chariot board piece
    """

    def __init__(self, team, position):
        """Initialises a chariot object with its team+name and move set"""
        super().__init__(team, position)
        self._type = 'Chariot'
        self._name = team[0] + self._type
        self._move_set = None

    def check_move(self, current, new, board):
        """
        This method will check if a move is valid for any chariot piece. It starts by checking if it is in either palace
        for special moves. If its not a palace move, it will check if its moving horizontal or vertical, then which
        direction it is going. If it is a valid move, it will loop through each square between the starting position and
        new position to make sure it's not being blocked. If the move has no issues it will return True, otherwise False
        """
        red_palace_corners_and_center = [[0, 3], [0, 5], [2, 3], [2, 5], [2, 4]]
        blue_palace_corners_and_center = [[9, 3], [9, 5], [7, 3], [7, 5], [8, 4]]

        # moving in the palace
        if current in red_palace_corners_and_center:
            if new in red_palace_corners_and_center:
                return True
        if current in blue_palace_corners_and_center:
            if new in blue_palace_corners_and_center:
                return True

        if current in self.get_enemy_palace():
            if self.is_in_enemy_palace(current, new):
                return True

        if current in self.get_team_palace():
            if self.is_in_team_palace(current, new):
                return True

        # moving horizontally
        if current[0] == new[0] and current[1] != new[1]:
            move_len = new[1] - current[1]
            while move_len > 1:  # Loop from current to new to check for pieces in the way
                if board[current[0]][move_len + current[1] - 1] != "-------":
                    return False
                move_len -= 1
            while move_len < 0:  # same loop as above but for going left on the board
                if board[current[0]][move_len + current[1]] != "-------":
                    return False
                move_len += 1
            return True

        # moving vertically
        if current[0] != new[0] and current[1] == new[1]:
            move_len = new[0] - current[0]

            # Moving down the board
            while move_len > 1:
                if board[move_len + current[0] - 1][current[1]] != "-------":
                    return False
                move_len -= 1

            # Moving up the board
            while move_len < 0:
                if board[move_len + current[0]][current[1]] != "-------":
                    return False
                move_len += 1
            return True
        else:
            return False


class Horse(Piece):
    """
    Represents a chariot board piece
    """

    def __init__(self, team, position):
        """Initialises a Horse object with its team+name and move set"""
        super().__init__(team, position)
        self._type = 'Horse'
        self._name = team[0] + self._type
        self._move_set = None

    def check_move(self, current, new, board):
        """
        validates movement for Horse pieces. First checks the initial vertical/horizontal movement to make sure it is
        empty and not blocked. then it check if the new position is equal to the 8 possible moves a horse can make
        and makes sure they are either empty of doesnt have a teammate in the desired new position
        """

        if current[0] + 2 == new[0]:  # moving down the board as first move
            if board[current[0] + 1][current[1]] != "-------":
                return False
            if current[1] + 1 != new[1] and current[1] - 1 != new[1]:
                return False
        elif current[0] - 2 == new[0]:  # moving up the board as first move
            if board[current[0] - 1][current[1]] != "-------":
                return False
            if current[1] + 1 != new[1] and current[1] - 1 != new[1]:
                return False
        elif current[1] + 2 == new[1]:  # moving to the right for first move
            if board[current[0]][current[1] + 1] != "-------":
                return False
            if current[0] + 1 != new[0] and current[0] - 1 != new[0]:
                return False
        else:  # moving left for first move
            if board[current[0]][current[1] - 1] != "-------":
                return False
            if current[0] + 1 != new[0] and current[0] - 1 != new[0]:
                return False

        # If we get this far its because the first move isn't blocked, now need to make sure the new location is empty/
        # doesn't have a teammate

        if board[new[0]][new[1]] == "-------" or board[new[0]][new[1]].get_team() != self._team:
            return True


class Elephant(Piece):
    """
    Represents a Elephant board piece
    """

    def __init__(self, team, position):
        """Initialises a Elephant object with its team+name and move set"""
        super().__init__(team, position)
        self._type = 'Elephant'
        self._name = team[0] + self._type
        self._move_set = None

    def check_move(self, current, new, board):
        """
        This method will check to make sure the desired move matches the elephant move set and that it is not blocked.
        This method is broken up into 4 sections, all designed for the initial vertical/horizontal move before the
        diagonal moves (up, down, left, right). Takes the current position and new position to move (must be converted
        using convert position method). it also takes the board as a parameter so it can evaluate what items are at the
        new location and the locations along the way so it can check if it can be blocked
        """

        # moving down the board as first move

        if current[0] + 3 == new[0]:
            # check first move before diagonal move
            if board[current[0] + 1][current[1]] != "-------":
                return False
            # Check diagonal move final location is correct
            if [current[0] + 3, current[1] + 2] != new and [current[0] + 3, current[1] - 2] != new:
                return False

            # Check first diagonal move to make sure its not blocked
            if [current[0] + 3, current[1] + 2] == new:
                if board[current[0] + 2][current[1] + 1] != "-------":
                    return False
            else:
                if board[current[0] + 2][current[1] - 1] != "-------":
                    return False

        # moving up the board as first move

        elif current[0] - 3 == new[0]:
            if board[current[0] - 1][current[1]] != "-------":
                return False
            if [current[0] - 3, current[1] + 2] != new and [current[0] - 3, current[1] - 2] != new:
                return False

            # Check first diagonal move to make sure its not blocked
            if [current[0] - 3, current[1] + 2] == new:
                if board[current[0] - 2][current[1] + 1] != "-------":
                    return False
            else:
                if board[current[0] - 2][current[1] - 1] != "-------":
                    return False

        # moving to the right for first move

        elif current[1] + 3 == new[1]:
            if board[current[0]][current[1] + 1] != "-------":
                return False
            if [current[0] + 2, current[1] + 3] != new and [current[0] - 2, current[1] + 3] != new:
                return False

            if [current[0] + 2, current[1] + 3] == new:
                if board[current[0] + 1][current[1] + 2] != "-------":
                    return False
            else:
                if board[current[0] - 1][current[1] + 2] != "-------":
                    return False

        # moving left for first move

        else:
            if board[current[0]][current[1] - 1] != "-------":
                return False
            if [current[0] + 2, current[1] - 3] != new and [current[0] - 2, current[1] - 3] != new:
                return False

            if [current[0] + 2, current[1] - 3] == new:
                if board[current[0] + 1][current[1] - 2] != "-------":
                    return False
            else:
                if board[current[0] - 1][current[1] - 2] != "-------":
                    return False

        # If we get this far its because the first move isn't blocked

        if board[new[0]][new[1]] == "-------" or board[new[0]][new[1]].get_team() != self._team:
            return True


class Guard(Piece):
    """
    Represents a Guard board piece
    """

    def __init__(self, team, position):
        """Initialises a Guard object with its team+name and move set"""
        super().__init__(team, position)
        self._type = 'Guard'
        self._name = team[0] + self._type
        self._move_set = None

    def check_move(self, current, new, board):
        """Checks to ensure the desired move is valid"""
        if self.is_in_team_palace(current, new):
            return True


class General(Piece):
    """
    Represents a General board piece
    """

    def __init__(self, team, position):
        """Initialises a General object with its team+name and move set"""
        super().__init__(team, position)
        self._type = 'General'
        self._name = team[0] + self._type
        self._move_set = None

    def check_move(self, current, new, board):
        """Checks to ensure the desired move is valid"""
        if self.is_in_team_palace(current, new):
            return True


class Cannon(Piece):
    """
    Represents a Cannon board piece
    """

    def __init__(self, team, position):
        """Initialises a Cannon object with its team+name and move set"""
        super().__init__(team, position)
        self._type = 'Cannon'
        self._name = team[0] + self._type
        self._move_set = None

    def check_move(self, current, new, board):
        """
        checks the current location and the new location to verify the desired move is
        valid. If it is, this method returns True. If it is not, it will return False
        """
        jump_counter = 0  # initialize jump counter to 0, if theres a piece to jump over it will increase

        # palace movement, different than the other pieces because of leap mechanic
        if current in [[9, 3], [9, 5], [7, 3], [7, 5]] and new in [[9, 3], [9, 5], [7, 3], [7, 5]] and \
                board[8][4] != '-------':
            if board[8][4].get_type() == 'Cannon':
                return False
            if current == [9, 3] and new == [7, 5]:
                return True
            if current == [7, 3] and new == [9, 5]:
                return True
            if current == [7, 5] and new == [9, 3]:
                return True
            if current == [9, 5] and new == [7, 3]:
                return True

        if current in [[0, 3], [0, 5], [2, 3], [2, 5]] and new in [[0, 3], [0, 5], [2, 3], [2, 5]] and \
                board[1][4] != '-------':
            if board[8][4].get_type() == 'Cannon':
                return False
            if current == [0, 3] and new == [2, 5]:
                return True
            if current == [2, 3] and new == [0, 5]:
                return True
            if current == [0, 5] and new == [2, 3]:
                return True
            if current == [2, 5] and new == [0, 3]:
                return True

        if board[new[0]][new[1]] != '-------':  # if new location has a cannon --> move is invalid
            if board[new[0]][new[1]].get_type() == 'Cannon':
                return False

        # moving horizontally
        if current[0] == new[0] and current[1] != new[1]:
            move_len = new[1] - current[1]

            # Going to the right
            while move_len > 1:  # Loop from current to new to check for pieces in the way
                if board[current[0]][move_len + current[1] - 1] != "-------":
                    if board[current[0]][move_len + current[1] - 1].get_type() == 'Cannon':
                        return False
                    jump_counter += 1
                move_len -= 1

            # same loop as above but for going left on the board
            while move_len < 0:
                if board[current[0]][move_len + current[1] - 1] != "-------":
                    if board[current[0]][move_len + current[1] - 1].get_type() == 'Cannon':
                        return False
                    jump_counter += 1
                move_len += 1
            if jump_counter == 1:
                return True

        # moving vertically
        if current[0] != new[0] and current[1] == new[1]:
            move_len = new[0] - current[0]

            # Moving down the board
            while move_len > 1:
                if board[move_len + current[0] - 1][current[1]] != "-------":
                    if board[move_len + current[0] - 1][current[1]].get_type() == 'Cannon':
                        return False
                    jump_counter += 1
                move_len -= 1

            # Moving up the board
            while move_len < 0:
                if board[move_len + current[0]][current[1]] != "-------":
                    if board[move_len + current[0]][current[1]].get_type() == 'Cannon':
                        return False
                    jump_counter += 1
                move_len += 1
            if jump_counter == 1:
                return True
        else:
            return False


class Soldier(Piece):
    """
    Represents a Soldier board piece
    """

    def __init__(self, team, position):
        """Initialises a Soldier object with its team+name and move set"""
        super().__init__(team, position)
        self._type = 'Soldier'
        self._name = team[0] + self._type
        if team == 'red':
            self._move_set = [[0, 1], [0, -1], [1, 0], [0, 0]]
        else:
            self._move_set = [[0, 1], [0, -1], [-1, 0], [0, 0]]

    def check_move(self, current, new, board):
        """makes sure that the move is in the pieces move_set"""
        move = [new[0] - current[0], new[1] - current[1]]

        if current in self._enemy_palace:
            if self.is_in_enemy_palace(current, new):
                return True

        if move not in self._move_set:
            return False
        else:
            return True


class Red:
    """Represents Red team with all their pieces in a list"""

    def __init__(self):
        """initializes the red class to contain all the pieces, along with their starting positions and team color"""
        self._rChariot1 = Chariot('red', [0, 0])
        self._rChariot2 = Chariot('red', [0, 8])
        self._rElephant1 = Elephant('red', [0, 1])
        self._rElephant2 = Elephant('red', [0, 6])
        self._rHorse1 = Horse('red', [0, 2])
        self._rHorse2 = Horse('red', [0, 7])
        self._rGuard1 = Guard('red', [0, 3])
        self._rGuard2 = Guard('red', [0, 5])
        self._rGeneral = General('red', [1, 4])
        self._rCannon1 = Cannon('red', [2, 1])
        self._rCannon2 = Cannon('red', [2, 7])
        self._rSoldier1 = Soldier('red', [3, 0])
        self._rSoldier2 = Soldier('red', [3, 2])
        self._rSoldier3 = Soldier('red', [3, 4])
        self._rSoldier4 = Soldier('red', [3, 6])
        self._rSoldier5 = Soldier('red', [3, 8])
        self._pieces = [self._rChariot1, self._rElephant1, self._rHorse1, self._rGuard1, self._rGuard2,
                        self._rElephant2, self._rHorse2, self._rChariot2, self._rGeneral, self._rCannon1,
                        self._rCannon2, self._rSoldier1, self._rSoldier2, self._rSoldier3, self._rSoldier4,
                        self._rSoldier5]

    def get_red_pieces(self):
        """returns a list of all the red piece objects"""
        return self._pieces

    def remove_piece(self, piece):
        """removes one of the pieces from the team _pieces list"""
        self._pieces.remove(piece)


class Blue:
    """Represents Red team with all their pieces in a list"""

    def __init__(self):
        """initializes the red class to contain all the pieces, along with their starting positions and team color"""
        self._bChariot1 = Chariot('blue', [9, 0])
        self._bChariot2 = Chariot('blue', [9, 8])
        self._bElephant1 = Elephant('blue', [9, 1])
        self._bElephant2 = Elephant('blue', [9, 6])
        self._bHorse1 = Horse('blue', [9, 2])
        self._bHorse2 = Horse('blue', [9, 7])
        self._bGuard1 = Guard('blue', [9, 3])
        self._bGuard2 = Guard('blue', [9, 5])
        self._bGeneral = General('blue', [8, 4])
        self._bCannon1 = Cannon('blue', [7, 1])
        self._bCannon2 = Cannon('blue', [7, 7])
        self._bSoldier1 = Soldier('blue', [6, 0])
        self._bSoldier2 = Soldier('blue', [6, 2])
        self._bSoldier3 = Soldier('blue', [6, 4])
        self._bSoldier4 = Soldier('blue', [6, 6])
        self._bSoldier5 = Soldier('blue', [6, 8])
        self._pieces = [self._bChariot1, self._bElephant1, self._bHorse1, self._bGuard1, self._bGuard2,
                        self._bElephant2, self._bHorse2, self._bChariot2, self._bGeneral, self._bCannon1,
                        self._bCannon2, self._bSoldier1, self._bSoldier2, self._bSoldier3, self._bSoldier4,
                        self._bSoldier5]
        self._blue_palace = [[]]

    def get_blue_pieces(self):
        """returns a list of all the red piece objects"""
        return self._pieces

    def remove_piece(self, piece):
        """removes one of the pieces from the team _pieces list"""
        self._pieces.remove(piece)


game = JanggiGame()
game.print_board()