import time
import threading
import os
import random
import copy
import re

class Color:
    def black(self, text):
        return f'\033[100m{text}\033[0m'
    
    def white(self, text):
        return f'\033[7m{text}\033[0m'
    
    def green(self, text):
        return f'\033[37;1;42m{text}\033[0m'
    
    def blue(self, text):
        return f'\033[37;3;104m{text}\033[0m'
    
    def grey(self, text):
        return f'\033[0;2;206m{text}\033[0m'

    def red(self, text):
        return f'\033[31m{text}\033[0m'
    
    def yellow(self, text):
        return f'\033[33m{text}\033[0m'
    
    def custom(self, text, color):
        return f'\033[{color}{text}\033[0m'
    
    
class Widget:
    def __init__(self):
        self.color = Color()
        self.message = ''
        
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def _len(self,text):
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        return len(ansi_escape.sub('', text))
    
    def showmenu(self):
        chess_board = [
        ['♜ ', '♞ ', '♝ ', '♛ ', '♚ ', '♝ ', '♞ ', '♜ '],  # 8
        ['♟ ', '♟ ', '♟ ', '♟ ', '♟ ', '♟ ', '♟ ', '♟ '],  # 7
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],  # 6
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],  # 5
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],  # 4
        ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],  # 3
        ['♙ ', '♙ ', '♙ ', '♙ ', '♙ ', '♙ ', '♙ ', '♙ '],  # 2
        ['♖ ', '♘ ', '♗ ', '♕ ', '♔ ', '♗ ', '♘ ', '♖ ']   # 1
        ]
        sub_menu = ('\033[104m1.\033[0m Main 1 VS 1 dengan teman', 
                    '\033[104m2.\033[0m Bermain dengan \033[5;33mAI\033[0m (Beginner)', 
                    '\033[104m3.\033[0m Tentang Program', 
                    '\033[104m4.\033[0m Keluar')
        line_length = 61
        print(f"┌{'─'*line_length}┐")
        print("│    a b c d e f g h       ░█▀▀░█░█░█▀▀░█▀▀░█▀▀░░░█▀▄░█░█░█▀▀ │")
        print("│   ┌────────────────┐   │ ░█░░░█▀█░█▀▀░▀▀█░▀▀█░░░█▀▄░█░█░█░█ │")
        for row in range(8):
            boxes=""
            print(f'│ {8-row} │', end='')
            for col in range(8):        
                boxes += f'\033[7m{chess_board[row][col]}\033[0m' if (row+col) % 2 == 0 else f'\033[100m{chess_board[row][col]}\033[0m'
            if row == 0:
                print(boxes, end='')
                print(f"│ {8-row} │ ░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░░░▀▀░░▀▀▀░▀▀▀ │")
            elif row >= 2 :
                length = 34 - (self._len(sub_menu[row-2]) if (row-2) <= len(sub_menu)-1 else 0)
                print(boxes, end='')
                print(f"│ {8-row} │ {(sub_menu[row-2] + ' ' * length) if (row-2) <= len(sub_menu)-1 else '':<34} │")
            else:
                print(boxes, end='')
                print(f"│ {8-row} │ {' ':<34} │")
                
        print(f"│   └────────────────┘   │ {self.message:<34} │")
        print(f"│    a b c d e f g h       {' ':<34} │")
        print(f"└{'─'*line_length}┘")
        
        
    def header_display(self, player_name, timer):
        line_length = 24
        abcd = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        padding = 3
        print(f"┌{'─'*line_length}┐")
        heading = ''.join(f'{ch.center(2)}' for ch in abcd)
        print(f"│{' '*padding} {heading} {' '*padding}│{'':<3}👤 {player_name:<10} {timer} ")
        print(f"│{' '*padding}┌{('─'*16)}┐{' '*padding}│")
        
    def middle_display (self, row, captured_pieces, message=''):
        white_captured = []
        black_captured = []
        for item in captured_pieces:
            if item.is_white:
                white_captured.append(item.icon)
            else:
                black_captured.append(item.icon)
        text=""        
        row +=1
        if row == 1:
            text +='(' + ','.join(white_captured) + ')'
        elif row == 4:
            text +=self.color.yellow(message)
        elif row == 8:
            text +='(' + ','.join(black_captured) + ')'
        return text 
        
    def bodyBoard_display(self, chess_board, captured_pieces):
        for row in range(len(chess_board)):
            box =""
            for col in range(len(chess_board[row])):
                piece = chess_board[row][col]
                color_exist = piece.color if isinstance(piece, ChessPiece) else False
                icon = piece.icon
                if not color_exist:
                    color_func = self.color.white if (row + col) % 2 == 0 else self.color.black
                    box += color_func(f"{icon} ")
                else:
                    color_func = self.color.custom
                    box += color_func(f"{icon} ", piece.color)
                    
            print(f"│ {8-row} │{box}│ {8-row} │{'':<3}{self.middle_display(row, captured_pieces, board.message)}")
            
    def footer_display(self, player_name, timer):
        line_length = 24
        abjad = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        padding = 3
        print(f"│{' '*padding}└{('─'*16)}┘{' '*padding}│")
        footer = ''.join(f'{ch.center(2)}' for ch in abjad)
        print(f"│{' '*padding} {footer} {' '*padding}│{'':<3}👤 {player_name:<10} {timer} ")
        print(f"└{'─'*line_length}┘")
        
    def showmessage(self, text):
        length_msg = len(text) + 2
        print(f"╭{'─'*length_msg}╮")
        print(f"│ {text} │")
        print(f"╰{'─'*length_msg}╯")
    
    def chip(self, items, split):
        top = middle = bottom = ""
        for i in range(len(items)):
            length = len(items[i])+2
            top += f"╭{'─' * length}╮"
            middle += f"│ {items[i]} │"
            bottom += f"╰{'─' * length}╯"
            if (i+1) % split == 0:
                print(top)
                print(middle)
                print(bottom)
                top = middle = bottom = ""
        
class GameStatus:
    def __init__(self, board):
        self.board = board    
        
    def is_check(self, is_white, board=None):
        board = board if board else self.board
        king_pos = board.find_king(is_white)
        for row in range(8):
            for col in range(8):
                piece = board.chess_board[row][col]
                if piece.icon != ' ' and piece.is_white != is_white:
                    if king_pos in piece.get_valid_move(row, col, check_check=False):
                        board.chess_board[king_pos[0]][king_pos[1]].setColor('41m')
                        return True
        return False

    
    def has_escape_moves(self, is_white):
        original_board = self.board.chess_board
        for row in range(8):
            for col in range(8):
                piece = original_board[row][col]
                if piece.icon != ' ' and piece.is_white == is_white:
                    valid_moves = piece.get_valid_move(row, col)
                    if self.has_legal_move(row, col, valid_moves, original_board, is_white):
                        return True
        return False

    
    def has_legal_move(self, row, col, valid_moves, original_board, is_white):
        for to_row, to_col in valid_moves:
            board = copy.deepcopy(original_board)
            test_piece = board[row][col]
            board[to_row][to_col] = test_piece
            board[row][col] = ChessPiece()
            
            temp_board_wrapper = copy.deepcopy(self.board)
            temp_board_wrapper.chess_board = board
            
            if not self.is_check(is_white, temp_board_wrapper):
                return True
        return False

    
    
    def is_checkemate(self, is_white):
        return self.is_check(is_white) and not self.has_escape_moves(is_white)
    
    def is_stalemate(self, is_white):
        return not self.is_check(is_white) and not self.has_escape_moves(is_white)

class Board:
    def __init__(self):
        self.widget = Widget()
        self.chess_board = []
        self.caputured_pieces = []
        self.last_moves = None
        self.message = ''
        
    def create_newBoard(self):
        size = 8
        self.chess_board = [[ChessPiece() for _ in range(size)] for _ in range(size)]
    
    def setup_default_board(self):
        board = self
        white_pieces = (Rook('♖',True, board), Horse('♘',True, board), Bishop('♗',True, board), Queen('♕',True, board), 
         King('♔',True, board), Bishop('♗',True, board), Horse('♘',True, board), Rook('♖',True, board))
        black_pieces = (Rook('♜',False, board), Horse('♞',False, board), Bishop('♝',False, board), Queen('♛',False, board), 
         King('♚',False, board), Bishop('♝',False, board), Horse('♞',False, board), Rook('♜',False, board))
        for i in range(8):
        #white
            board.chess_board[6][i] = Pawn('♙', True, board)
            board.chess_board[7][i] = white_pieces[i]
        # black
            board.chess_board[1][i] = Pawn('♟', False, board)
            board.chess_board[0][i] = black_pieces[i]
    
    def insert_chess_piece(self, piece, row, col):
        self.chess_board[row][col] = piece
    
    def find_king(self, is_white):
        for row in range(8):
            for col in range(8):
                piece = self.chess_board[row][col]
                if isinstance(piece, King) and piece.is_white == is_white:
                    return row, col
        return None
    
    def add_capture_piece(self, piece):
        if piece.icon !=' ':
            self.caputured_pieces.append(piece)
    
    def display(self, player_name_white, player_name_black, white_timer, black_timer):
        self.widget.header_display(player_name_white, black_timer)
        self.widget.bodyBoard_display(self.chess_board, self.caputured_pieces)
        self.widget.footer_display(player_name_black, white_timer)
    
    def setMessage(self, message):
        self.message = message
        
    def highlight_box(self, valid_moves):
        try:
            board = self.chess_board
            for count, (i, j) in enumerate(valid_moves, start=1):
                color = '43m' if count % 2 == 0 else '103m'
                board[i][j].setColor(color)
        except AttributeError as e:
            print(f'Error: {e}')
    
    def resetColor(self):
        try:
            for row in self.chess_board:
                for piece in row:
                    piece.color = None
        except AttributeError as e:
            print(f'Error: {e}')
        
        
class ChessPiece:
    def __init__(self, icon=' ', is_white=None, board=None):
        self.icon = icon
        self.board = board
        self.is_white = is_white
        self.color = None
        self.has_moved = False
        self.status = GameStatus(board)
    
    def move(self, from_row, from_col, to_row, to_col):
        if (to_row, to_col) in self.get_valid_move(from_row, from_col) and self.board:
            board = self.board.chess_board
            #capture piece
            target_piece = board[to_row][to_col]
            self.board.add_capture_piece(target_piece)
            
            board[to_row][to_col] = board[from_row][from_col]
            self.remove_old_box(from_row, from_col)
            self.has_moved = True
        else:
            print("Invalid Move!")
            self.board.setMessage('Invalid Move!')
                
    def setColor(self, color):
        self.color = color
        
    def remove_old_box(self, row, col):
        try:
            board = self.board.chess_board
            board[row][col] = ChessPiece()
        except AttributeError as e:
            print(f'Error: {e}')
    
    def get_valid_move(self, row, col):
        pass
    
    def is_move_safe(self, from_row, from_col, to_row, to_col):
        board_copy = copy.deepcopy(self.board)
        status_copy = GameStatus(board_copy)
        
        piece = board_copy.chess_board[from_row][from_col]
        board_copy.chess_board[to_row][to_col] = piece
        board_copy.chess_board[from_row][from_col] = ChessPiece()
        
        return not status_copy.is_check(self.is_white)


class King(ChessPiece):
    def __init__(self, icon, is_white, board):
        super().__init__(icon, is_white,board)
    #special move    
    def castling(self,to_row, to_col, valid_moves):
        row = 7 if self.is_white else 0
        board = self.board.chess_board
        if to_col == 2 and (to_row, to_col) in valid_moves: #castling left
            rook = board[row][0]
            rook.move(row,0,row, 3)
            board[row][2] = self
            self.remove_old_box(row, 4)
            
        elif to_col == 6 and (to_row, to_col) in valid_moves: #castling right
            rook = board[row][7]
            rook.move(row,7,row, 5)
            board[row][6] = self
            self.remove_old_box(row, 4)
            
            
    def is_rook_left_valid(self):
        rook = self.board.chess_board[7][0] if self.is_white else self.board.chess_board[0][0]
        piece = self.board.chess_board[7] if self.is_white else self.board.chess_board[0]
        return (isinstance(rook, Rook)
                and not rook.has_moved 
                and piece[1].icon ==' '
                and piece[2].icon ==' '
                and piece[3].icon ==' ')
           
    def is_rook_right_valid(self):
        rook = self.board.chess_board[7][7] if self.is_white else self.board.chess_board[0][7]
        piece = self.board.chess_board[7] if self.is_white else self.board.chess_board[0]
        return (isinstance(rook, Rook)
                and not rook.has_moved 
                and piece[5].icon ==' '
                and piece[6].icon ==' ')
    
    def get_valid_move(self, row, col, check_check=True):
        try:
            valid_moves = []
            board = self.board.chess_board
            king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

            for row_offset, col_offset in king_moves:
                new_row = row + row_offset
                new_col = col + col_offset
                if not (0 <= new_row < 8 and 0 <= new_col <8):
                    continue
                piece = board[new_row][new_col]
                if piece.icon == ' ' or piece.is_white != self.is_white:
                    if not check_check or self.is_move_safe(row, col, new_row, new_col):
                        valid_moves.append((new_row, new_col))
                                    
            if not self.has_moved and (not check_check or not game_status.is_check(self.is_white)):
                if self.is_rook_left_valid() and (not check_check or self.is_move_safe(row, col, row, new_col-2)):
                        valid_moves.append((row, col-2))
                if self.is_rook_right_valid() and (not check_check or self.is_move_safe(row, col, row, new_col+2)):
                        valid_moves.append((row, col+2))
                        
            return valid_moves
        except AttributeError as e:
            print(f'Error: {e}')
    
    def is_castling_move(self, to_row, to_col, valid_moves):
        #castling bisa jalan kalo raja tidak skak, raja berad di kolom 2/6 raja belum bergerak dan castling ada di valid moves
        return to_col in [2, 6] and not self.has_moved and (to_row, to_col) in valid_moves
    
    def move(self, from_row, from_col, to_row, to_col):
        try:
            board = self.board.chess_board
            valid_moves = self.get_valid_move(from_row, from_col)
            if self.is_castling_move(to_row, to_col, valid_moves):
                self.castling(to_row,to_col,valid_moves)
            elif (to_row, to_col) in valid_moves and self.board:
                #capture piece
                target_piece = board[to_row][to_col]
                self.board.add_capture_piece(target_piece)
                
                board[to_row][to_col] = board[from_row][from_col]
                self.remove_old_box(from_row, from_col)
                self.has_moved = True
            else:
                print("Invalid Move!")
                self.board.message = 'Invalid Move!'
        except AttributeError as e:
            print(f'Error: {e}')
        
    
class Queen(ChessPiece):
    def __init__(self, icon, is_white, board):
        super().__init__(icon, is_white, board)
    def get_valid_move(self, row, col, check_check=True):
        try:
            valid_moves = []
            board = self.board.chess_board
            queen_moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (-1, -1), (1, 1), (1, -1)]
            
            for row_offset, col_offset in queen_moves:
                new_row, new_col = row + row_offset, col + col_offset 
                while 0 <= new_row < 8 and 0 <= new_col < 8:
                    piece = board[new_row][new_col]
                    is_opponent = piece.is_white != self.is_white
                    if piece.icon == ' ':
                        if not check_check or self.is_move_safe(row, col, new_row, new_col):
                            valid_moves.append((new_row, new_col))
                    elif is_opponent:
                        if not check_check or self.is_move_safe(row, col, new_row, new_col):
                            valid_moves.append((new_row, new_col))
                        break
                    else:
                        break
                    new_row += row_offset
                    new_col += col_offset
                    
            return valid_moves
        except AttributeError as e:
            print(f'Error: {e}')

class Pawn(ChessPiece):
    def __init__(self, icon, is_white, board):
        super().__init__(icon, is_white, board)
        
        
    def get_valid_move(self, row, col, check_check=True):
        try:
            valid_moves = []
            direction = -1 if self.is_white else 1
            board = self.board.chess_board
            #jika bisa maju 1 langkah
            if 0 <= row + direction < 8 and board[row + direction][col].icon == ' ':
                if not check_check or self.is_move_safe(row, col, row + direction, col):
                    valid_moves.append((row + direction, col))
            
            #jika bisa maju 2 langkah
            if ((self.is_white and row == 6) or (not self.is_white and row == 1)) and board[row + direction*2][col].icon == ' ':
                if not check_check or self.is_move_safe(row, col, row + direction*2, col):
                    valid_moves.append((row + direction*2, col))
            
            #enpassant    
            if self.board.last_moves:
                (from_row, from_col), (to_row, to_col), is_white = self.board.last_moves
                if (is_white != self.is_white
                    and abs(from_row - to_row) == 2
                    and abs(to_col-col) == 1 
                    and board[row+direction][to_col].icon ==' '
                    and to_row == row):
                    if not check_check or self.is_move_safe(row, col, row + direction, col):
                        valid_moves.append((row + direction, to_col))
                    
            
            #serangan diagonal
            for target in (-1, 1):
                new_col = col + target
                if 0 <= row + direction < 8 and 0 <= new_col < 8:
                    piece = board[row + direction][new_col]
                    if piece and piece.icon != " " and piece.is_white != self.is_white:
                        if not check_check or self.is_move_safe(row, col, row + direction, col):
                            valid_moves.append((row + direction, new_col))
                        
            return valid_moves
        except AttributeError as e:
            print(f'Error: {e}')
            
    def promotion(self, row, col, board):
        promote_item = '1. ♕ Queen', '2. ♖ Rook', '3. ♗ Bishop', '4. ♘ Horse'
        white_pieces = (Queen('♕',True, board), Rook('♖',True, board), Bishop('♗',True, board), Horse('♘',True, board))
        black_pieces = (Queen('♛',False, board), Rook('♜',False, board), Bishop('♝',False, board), Horse('♞',False, board))
        widget.chip(promote_item, len(promote_item))
        while True:
            try:
                choose = int(input('Pilih promosi 1-4: '))-1
                if self.is_white:
                    self.board.chess_board[row][col] = white_pieces[choose]
                else:
                    self.board.chess_board[row][col] = black_pieces[choose]
                break
            except ValueError:
                continue
            except IndexError:
                continue
        board.setMessage('Pion Dipromosikan')
                
    
    def is_en_passant(self, from_row, from_col, to_row, to_col):
        try:
            board = self.board.chess_board
            return (abs(from_col-to_col) == 1 
                    and board[to_row][to_col].icon ==' ' 
                    and (to_row, to_col) 
                    in self.get_valid_move(from_row, from_col))
        except AttributeError as e:
            print(f'Error: {e}')
    
    def move(self, from_row, from_col, to_row, to_col):
        try:
            board = self.board.chess_board
            #enpassant
            if self.is_en_passant(from_row, from_col, to_row, to_col):
                #capture piece
                target_piece = board[from_row][to_col]
                self.board.add_capture_piece(target_piece)
                
                board[to_row][to_col] = board[from_row][from_col]
                self.remove_old_box(from_row, from_col)
                board[from_row][to_col] = ChessPiece()
                self.has_moved = True
            elif (to_row, to_col) in self.get_valid_move(from_row, from_col) and self.board:
                #capture piece
                target_piece = board[to_row][to_col]
                self.board.add_capture_piece(target_piece)
                
                board[to_row][to_col] = board[from_row][from_col]
                self.remove_old_box(from_row, from_col)
                self.has_moved = True
            else:
                print("Invalid Move!")
                self.board.message = 'Invalid Move!'
            #cek apakah layak di promosikan
            if (self.is_white and to_row==0) or (not self.is_white and to_row==7):
                self.promotion(to_row, to_col, self.board)
            
            self.board.last_moves = ((from_row, from_col), (to_row, to_col), self.is_white)
        except AttributeError as e:
            print(f'Error: {e}')
    
class Rook(ChessPiece):
    def __init__(self, icon, is_white, board):
        super().__init__(icon, is_white, board)
    def get_valid_move(self, row, col, check_check=True):
        try:
            valid_moves = []
            board = self.board.chess_board
            rook_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            
            for row_offset, col_offset in rook_moves:
                new_row, new_col = row + row_offset, col + col_offset 
                while 0 <= new_row < 8 and 0 <= new_col < 8:
                    piece = board[new_row][new_col]
                    is_opponent = piece.is_white != self.is_white
                    if piece.icon == ' ':
                        if not check_check or self.is_move_safe(row, col, new_row, new_col):
                            valid_moves.append((new_row, new_col))
                    elif is_opponent:
                        if not check_check or self.is_move_safe(row, col, new_row, new_col):
                            valid_moves.append((new_row, new_col))
                        break
                    else:
                        break
                    new_row += row_offset
                    new_col += col_offset
                    
            return valid_moves
        except AttributeError as e:
            print(f'Error: {e}')

class Bishop(ChessPiece):
    def __init__(self, icon, is_white, board):
        super().__init__(icon, is_white, board)
    def get_valid_move(self, row, col, check_check=True):
        try:
            valid_moves = []
            board = self.board.chess_board
            bishop_moves = [(-1, 1), (-1, -1), (1, 1), (1, -1)]
            
            for row_offset, col_offset in bishop_moves:
                new_row, new_col = row + row_offset, col + col_offset
                while 0<= new_row < 8 and 0<= new_col < 8:
                    piece = board[new_row][new_col]
                    is_opponent = piece.is_white != self.is_white
                    if piece.icon == ' ':
                        if not check_check or self.is_move_safe(row, col, new_row, new_col):
                            valid_moves.append((new_row, new_col))
                    elif is_opponent:
                        if not check_check or self.is_move_safe(row, col, new_row, new_col):
                            valid_moves.append((new_row, new_col))
                        break
                    else:
                        break
                    new_row +=row_offset
                    new_col +=col_offset
            
            return valid_moves
        except AttributeError as e:
            print(f'Error: {e}')
    
class Horse(ChessPiece):
    def __init__(self, icon, is_white, board):
        super().__init__(icon, is_white, board)
    def get_valid_move(self, row, col, check_check=True):
        try:
            valid_moves = []
            board = self.board.chess_board
            horse_moves = [
            (-2, 1), # Langkah L ke atas Kanan
            (-2, -1), # Langkah L ke atas Kiri
            (2, 1), # Langkah L ke bawah Kanan
            (2, -1), # Langkah L ke bawah Kiri
            (-1, 2), # Langkah L ke atas Kanan 2
            (-1,-2), # Langkah L ke atas Kiri 2
            (1, 2), # Langkah L ke bawah Kanan 2
            (1,-2) # Langkah L ke bawah Kiri
            ]
            
            for row_offset, col_offset in horse_moves:
                new_row, new_col = row + row_offset, col + col_offset
                if not (0 <= new_row < 8 and 0 <= new_col <8):
                    continue
                piece = board[new_row][new_col]
                if piece and piece.icon == ' ' or piece.is_white != self.is_white:
                    if not check_check or self.is_move_safe(row, col, new_row, new_col):
                        valid_moves.append((new_row, new_col))
                                
            return valid_moves
        except AttributeError as e:
            print(f'Error: {e}')
            
class ChessCoordinate:
    def __init__(self):
        self.dict_col = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        
    def CoordinateConverter(self, pos):
        try:
            col , row = pos
            col = col.lower()
            row = int(row)
            return self.dict_col.get(col), 8-row
        except (ValueError, TypeError, KeyError) as ex:
            print(f'Error: {ex}')

class AI:
    def __init__(self, board, is_white):
        self.board = board
        self.is_white = is_white
        
    def make_ai_move(self):
        all_legal_moves = []
        board = self.board.chess_board
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece.is_white == self.is_white:
                    valid_moves = piece.get_valid_move(row, col)
                    for valid_move in valid_moves:
                        all_legal_moves.append(((row, col), valid_move))
        choosen_moves = random.choice(all_legal_moves)
        return choosen_moves

    def set_team(self, is_white):
        self.is_white = is_white
            
class TimerChess:
    def __init__(self, minutes=1):
        self.color = Color()
        self.set_duration(minutes * 60)
        self.running = False

    def set_duration(self, seconds):
        self.timer = seconds

    def start(self):
        if self.timer <= 0:
            return
        self.running = True
        timerthread = threading.Thread(target=self.run)
        timerthread.daemon = True
        timerthread.start()

    def stop(self):
        self.running = False

    def run(self):
        while self.running and self.timer > 0:
            time.sleep(1)
            self.timer -= 1
            if self.timer <= 0:
                self.running = False
                
    def isTimeout(self):
        return self.timer <= 0
    
    def display(self):
        minutes, seconds = divmod(self.timer, 60)
        if self.timer == 0:
            return self.color.grey("00:00")
        if self.running:
            return self.color.green(f"{minutes:02d}:{seconds:02d}")
        else:
            return self.color.grey(f"{minutes:02d}:{seconds:02d}")

class NoTimer:
    def __init__(self):
        self.color = Color()
        self.timer = 1
        self.running = False
    def start(self):
        self.running = True
    def stop(self):
        self.running = False
    def set_duration(self, seconds=0):
        pass
    def isTimeout(self):
        return False
    def display(self):
        if self.running:
            return self.color.green(' ∞ ')
        return self.color.grey(' ∞ ')

class Player:
    def __init__(self, name, team):
        self.name = name
        self.team = team
        self.timer = None

class Manage_Player:
    def __init__(self):
        self.players = []

    def add_player(self, name, team, is_timer=True, timer_duration=60):
        player = Player(name, team)
        player.timer = TimerChess(timer_duration // 60 if timer_duration else 0) if is_timer else NoTimer()
        self.players.append(player)
        return player

    def clear_players(self):
        self.players.clear()      
                
board = Board()
players = Manage_Player()
game_status = GameStatus(board)
widget = Widget()
pos = ChessCoordinate().CoordinateConverter
ai_beginner = AI(board, False)
color = Color()

def initial_game(timer_duration=0, vs_ai=False):
    board.create_newBoard()
    board.setup_default_board()
    players.clear_players()
    
    if vs_ai:
        while True:
            user_team = input("Pilih tim kamu (White/Black): ").strip().lower()
            if user_team in ['white', 'black']:
                is_white_user = user_team == 'white'
                break
            else:
                print("Input tidak valid. Masukkan 'White' atau 'Black'.")
        
        name = input(f'Masukkan nama kamu ({user_team.capitalize()}): ')
        if user_team == 'white':
            players.add_player(name, is_white_user, False)
            players.add_player('AI (Pemula)', not is_white_user, False)
            ai_beginner.set_team(not is_white_user)
        else:
            players.add_player('AI (Pemula)', not is_white_user, False)
            ai_beginner.set_team(not is_white_user)
            players.add_player(name, is_white_user, False)

    else:
        for is_white in (True, False):
            team = 'White' if is_white else 'Black'
            name = input(f'Masukkan nama pemain ({team}): ')
            if timer_duration == 0:
                players.add_player(name, is_white, False)
            else:
                players.add_player(name, is_white,timer_duration=timer_duration)


def display():
    widget.clear()
    player_white, player_black = players.players
    white_timer, black_timer = player_white.timer.display(), player_black.timer.display()
    board.display(player_black.name, player_white.name, white_timer, black_timer)
    print(f"{color.blue('q: quit')} {color.blue('r: resign')}")

def select_piece(player):
    while True:
        try:
            team = 'White' if player.team else 'Black'
            pick = input(f'Pilih bidak ({team}): ').strip().lower()

            if pick == 'q':
                return 'quit'
            elif pick == 'r':
                return 'resign'

            from_col, from_row = pos(pick)
            piece = board.chess_board[from_row][from_col]
            if piece.icon == ' ':
                board.setMessage("Tidak ada bidak di kotak tersebut.")
            elif piece.is_white != player.team:
                board.setMessage("Itu bukan bidak milikmu.")
            elif not piece.get_valid_move(from_row, from_col):
                board.setMessage(f'{piece.icon} tidak punya langkah legal.')
            else:
                return from_row, from_col
        except Exception:
            board.setMessage("Input tidak valid.")
        display()

def select_target(valid_moves):
    while True:
        try:
            target = input('Pilih target: ').strip().lower()
            if target == 'q':
                return 'quit'
            elif target == 'r':
                return 'resign'

            to_col, to_row = pos(target)
            if (to_row, to_col) in valid_moves:
                return to_row, to_col
            else:
                board.setMessage("Gerakan tidak valid!")
        except Exception:
            board.setMessage("Input tidak valid")
        display()

def do_turn(player, is_ai=False):
    player.timer.start()
    if is_ai:
        time.sleep(1)
        (from_row, from_col), (to_row, to_col) = ai_beginner.make_ai_move()
        piece = board.chess_board[from_row][from_col]
        board.setMessage(f"AI memilih {piece.icon}")
        display()
        board.resetColor()
        time.sleep(1)
        piece.move(from_row, from_col, to_row, to_col)
        board.highlight_box([(from_row, from_col), (to_row, to_col)])
        board.setMessage(f"{piece.icon} bergerak ke {to_row, to_col}")
        display()
        
    else:
        display()
        move = select_piece(player)
        if move == 'quit':
            return 'quit'
        if move == 'resign':
            return 'resign'
        from_row, from_col = move
        piece = board.chess_board[from_row][from_col]
        valid_moves = piece.get_valid_move(from_row, from_col)
        board.resetColor()
        board.highlight_box(valid_moves)
        board.setMessage(f"{player.name} memilih {piece.icon}")
        display()
        target = select_target(valid_moves)
        if target == 'quit':
            return 'quit'
        if target == 'resign':
            return 'resign'
        board.resetColor()
        to_row, to_col = target
        piece.move(from_row, from_col, to_row, to_col)
        board.highlight_box([(from_row, from_col), (to_row, to_col)])
        board.setMessage(f"{piece.icon} bergerak ke {to_row, to_col}")

    display()
    player.timer.stop()
    return None


def game_play(ai=False):
    checkmate = False
    display()
    while not checkmate:
        for player in players.players:
            is_ai = (player.name == 'AI (Pemula)') if ai else False
            white_player, black_player = players.players
            opponent = white_player if not player.team else black_player
            result = do_turn(player, is_ai)
            if result == 'quit':
                checkmate = True
                board.setMessage("Keluar ke menu utama...")
                display()
                break
            elif result == 'resign':
                checkmate = True
                board.setMessage(f"{opponent.name} menang karena lawan menyerah!")
                display()
                break
            
            if game_status.is_checkemate(True) or game_status.is_checkemate(False):
                checkmate = True
                board.setMessage(f'{player.name} menang dengan skakmat!')
                display()
                break
            
            if game_status.is_stalemate(True) or game_status.is_stalemate(False):
                checkmate = True
                board.setMessage(f'Pertandingan seri!')
                display()
                break
            
            if game_status.is_check(True):
                board.setMessage("White sedang skak!")
                display()
            if game_status.is_check(False):
                board.setMessage("Black sedang skak!")
                display()
            
            if player.timer.isTimeout():
                checkmate = True
                board.setMessage(f'{opponent.name} menang dengan waktu!')
                display()
                break

    input('> Tekan enter untuk kembali ke menu ')

                
def show_time_menu():
    widget.chip(("1. Tanpa Batas", "2. 10 Menit"), 2)
    widget.chip(("3. 5 Menit", "4. 3 Menit", "5. 1 Menit"), 3)

    while True:
        try:
            choice = int(input("Pilih opsi waktu (1-5): "))
            durations = {1: 0, 2: 600, 3: 300, 4: 180, 5: 60}
            return durations.get(choice, 0)
        except:
            print("Input tidak valid.")


def main_menu():
    while True:
        widget.clear()
        widget.showmenu()
        try:
            option = int(input("Masukkan pilihanmu: "))
            if option == 1:
                duration = show_time_menu()
                initial_game(timer_duration=duration)
                game_play()
            elif option == 2:
                initial_game(timer_duration=0, vs_ai=True)
                game_play(ai=True)
            elif option == 3:
                print('-'*30)
                print('Game catur berbasi terminal oleh kelompok JackFruit')
                print("Nama anggota kelompok:")
                widget.chip(('Georgina', 'Dhesy', 'Renaia', 'Anugerah'), 4)
                print('-'*30)
                input()
            elif option == 4:
                widget.message = "Terima kasih telah bermain."
                break
            else:
                widget.message = ("Pilihan tidak dikenal.")
        except ValueError:
            widget.message = ("Masukkan angka yang valid.")
            

main_menu()