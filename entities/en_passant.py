from entities.move import Move

class EnPassant(Move):
    def __init__(self, start_square_num, target_square_num, piece):
        super().__init__(start_square_num,target_square_num,piece)
