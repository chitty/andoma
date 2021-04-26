import sys
import chess
import argparse
from movegeneration import next_move
from transposition_table import TranspositionTable


def talk():
    """
    The main input/output loop.
    This implements a slice of the UCI protocol.
    """
    board = chess.Board()
    depth = get_depth()
    transposition_table = TranspositionTable()

    while True:
        msg = input()
        print(f">>> {msg}", file=sys.stderr)
        command(depth, board, msg, transposition_table)


def command(
    depth: int,
    board: chess.Board,
    msg: str,
    transposition_table: TranspositionTable = None,
):
    """
    Accept UCI commands and respond.
    The board state is also updated.
    """
    if msg == "quit":
        sys.exit()

    if msg == "uci":
        print("id name Andoma")  # Andrew/Roma -> And/oma
        print("id author Andrew Healey & Roma Parramore")
        print("uciok")
        return

    if msg == "isready":
        print("readyok")
        return

    if msg == "ucinewgame":
        return

    if "position startpos moves" in msg:
        moves = msg.split(" ")[3:]
        board.clear()
        board.set_fen(chess.STARTING_FEN)
        for move in moves:
            board.push(chess.Move.from_uci(move))
        return

    if "position fen" in msg:
        fen = " ".join(msg.split(" ")[2:])
        board.set_fen(fen)
        return

    if msg[0:2] == "go":
        _move = next_move(depth, board, transposition_table)
        print(f"bestmove {_move}")
        return


def get_depth() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", default=3, help="provide an integer (default: 3)")
    args = parser.parse_args()
    return max([1, int(args.depth)])
