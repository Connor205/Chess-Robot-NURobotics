def test_imports():
    import pytest
    import stockfish
    import tkinter
    import time
    import threading
    import serial


# Test stockfish.py
def test_stockfish():
    from stockfish import Stockfish
    stockfish = Stockfish()
    assert stockfish.is_move_correct('a2a3') == True
    stockfish.set_fen_position(
        "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
    assert stockfish.get_best_move() == 'd2d4'
    assert stockfish.does_current_engine_version_have_wdl_option()
    assert stockfish.get_stockfish_major_version() == 14
    assert not stockfish.is_development_build_of_engine()