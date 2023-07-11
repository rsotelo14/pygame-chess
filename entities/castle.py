from entities.move import Move

class Castle(Move):
    def __init__(self, start_square_num, target_square_num, piece, is_short_castle):
        super().__init__(start_square_num,target_square_num,piece)
        self.is_short_castle = is_short_castle