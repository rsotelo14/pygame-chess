import vars
class Piece:
    def __init__(self, is_white, value):
        self.is_white = is_white
        self.value = value
        self.img = None
        
        #Deciding type of piece
        # 10 -> King
        # 9 -> Queen
        # 5 -> Rook
        # 4 -> Bishop
        # 3 -> Knight
        # 1 -> Pawn
        if self.value == 10 and self.is_white:
            self.img = vars.WHITE_KING
        elif self.value == 10 and not self.is_white:
            self.img = vars.BLACK_KING
        elif self.value == 9 and self.is_white:
            self.img = vars.WHITE_QUEEN
        elif self.value == 9 and not self.is_white:
            self.img = vars.BLACK_QUEEN
        elif self.value == 5 and self.is_white:
            self.img = vars.WHITE_ROOK
        elif self.value == 5 and not self.is_white:
            self.img = vars.BLACK_ROOK
        elif self.value == 4 and self.is_white:
            self.img = vars.WHITE_BISHOP
        elif self.value == 4 and not self.is_white:
            self.img = vars.BLACK_BISHOP
        elif self.value == 3 and self.is_white:
            self.img = vars.WHITE_KNIGHT
        elif self.value == 3 and not self.is_white:
            self.img = vars.BLACK_KNIGHT
        elif self.value == 1 and self.is_white:
            self.img = vars.WHITE_PAWN
        elif self.value == 1 and not self.is_white:
            self.img = vars.BLACK_PAWN