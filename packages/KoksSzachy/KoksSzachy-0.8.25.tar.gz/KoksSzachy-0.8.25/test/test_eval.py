#!/usr/bin/env python3

import unittest
import chess
from koksszachy.engine import KoksSzachy


class TestEval():
  def test_eval():
    v = KoksSzachy("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    print(v.evaluate())


if __name__=="__main__":
#  unittest.main()
  TestEval.test_eval()
