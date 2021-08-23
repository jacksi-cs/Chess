import chess

piece_value = {
    'P' : 1,
    'N' : 3,
    'B' : 3,
    'R' : 5,
    'Q' : 9,
    'K' : 0.5, # Kings will always be on the board
    'p' : -1,
    'n' : -3,
    'b' : -3,
    'r' : -5,
    'q' : -9,
    'k' : -0.5
}

piece_type_list = [chess.PAWN, chess.ROOK, chess.BISHOP, chess.KNIGHT, chess.QUEEN, chess.KING]

def eval(cboard):
    white_count = 0
    black_count = 0

    if cboard.is_checkmate():
        if cboard.turn == chess.WHITE:
            return -1000
        elif cboard.turn == chess.BLACK:
            return 1000
    if cboard.is_stalemate():
        return 0

    board_fen = cboard.board_fen()
    for char in board_fen:
        if char.isupper():
            white_count += piece_value[char]
        elif char.islower():
            black_count += piece_value[char]

    material_balance = white_count + black_count

def eval2(cboard):

    # Determining whether or not checkmate or stalemate
    check = 0
    if cboard.is_checkmate():
        if cboard.turn == chess.WHITE:
            return -100
        elif cboard.turn == chess.BLACK:
            return 100
    if cboard.is_stalemate():
        return 0

    # Small incentive to check the opponent
    if cboard.is_check():
        if cboard.turn == chess.WHITE:
            check = -5
        elif cboard.turn == chess.BLACK:
            check = 5

    bb_white_pieces = chess.SquareSet(chess.BB_ALL)
    for piece_type in piece_type_list:
        bb_white_pieces = bb_white_pieces | cboard.pieces(piece_type, chess.WHITE)

    bb_black_pieces = chess.SquareSet(chess.BB_ALL)
    for piece_type in piece_type_list:
        bb_black_pieces = bb_black_pieces | cboard.pieces(piece_type, chess.BLACK)
    
    ally_multiplier = 1.2
    opponent_multiplier = 1.1

    value = 0

    row = 56
    column = 0
    for char in cboard.board_fen():
        if char != '/':
            if char.isdigit():
                column += int(char)
            else:
                if char.isupper():
                    value += ally_multiplier * (piece_value[char] * (len(cboard.attacks(row+column) | bb_white_pieces)))
                    value += opponent_multiplier * (piece_value[char] * (len(cboard.attacks(row+column) | bb_black_pieces)))
                elif char.islower():
                    value += ally_multiplier * (piece_value[char] * (len(cboard.attacks(row+column) | bb_black_pieces)))
                    value += opponent_multiplier * (piece_value[char] * (len(cboard.attacks(row+column) | bb_white_pieces)))

                value += (piece_value[char] * (len(cboard.attacks(row+column) | (~bb_white_pieces & ~bb_black_pieces))))
                column += 1
        else:
            row -= 8
            column = 0

    return value + check

board = chess.Board("2b1k1nr/3q1p1p/r2p1b2/pp2p1p1/1Pnp4/PN1QPPPP/1B1K2B1/1R4NR w k - 0 20")

print(eval2(board))