class BoardSquare:
    def __init__(self, x_start, y_start, width_height, is_white, piece = None):
        self.x_start = x_start
        self.y_start = y_start
        self.width_height= width_height
        self.is_white = is_white
        self.piece = piece
