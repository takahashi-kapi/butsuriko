import math
import random

BLACK = 1
WHITE = 2

board = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0],
    [0, 0, 2, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

def can_place_x_y(board, stone, x, y):
    """
    石を置けるかどうかを調べる関数。
    board: 2次元配列のオセロボード
    x, y: 石を置きたい座標 (0-indexed)
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    return: 置けるなら True, 置けないなら False
    """
    if board[y][x] != 0:
        return False  # 既に石がある場合は置けない

    opponent = 3 - stone  # 相手の石 (1なら2、2なら1)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True  # 石を置ける条件を満たす

    return False

def can_place(board, stone):
    """
    石を置ける場所を調べる関数。
    board: 2次元配列のオセロボード
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    """
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                return True
    return False

def smart_place(board, stone):
    """
    石を賢く置く関数（改良版）。
    board: 2次元配列のオセロボード
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    return: (x, y) 次に置く座標
    """
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def evaluate(board, stone):
        """
        簡単な評価関数。角を優先し、全体の石数も考慮。
        """
        corner_positions = [(0, 0), (0, len(board[0]) - 1), (len(board) - 1, 0), (len(board) - 1, len(board[0]) - 1)]
        score = 0

        # 石の数をカウント
        score += sum(row.count(stone) for row in board)

        # 角を評価
        for x, y in corner_positions:
            if board[y][x] == stone:
                score += 10  # 角の価値を高く設定

        return score

    def simulate_move(board, stone, x, y):
        """
        指定された座標に石を置いた後の盤面を返す。
        """
        new_board = [row[:] for row in board]
        opponent = 3 - stone
        new_board[y][x] = stone

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            flips = []

            while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and new_board[ny][nx] == opponent:
                flips.append((nx, ny))
                nx += dx
                ny += dy

            if flips and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and new_board[ny][nx] == stone:
                for fx, fy in flips:
                    new_board[fy][fx] = stone

        return new_board

    # 全ての有効な手を探索
    valid_moves = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                valid_moves.append((x, y))

    if not valid_moves:
        return None  # 置ける場所がない場合

    # 最良の手を見つける
    best_move = None
    best_score = -math.inf

    for x, y in valid_moves:
        new_board = simulate_move(board, stone, x, y)
        score = evaluate(new_board, stone)
        if score > best_score:
            best_score = score
            best_move = (x, y)

    return best_move

class ButsurikoAI(object):

    def face(self):
        return "🐰"

    def place(self, board, stone):
        x, y = smart_place(board, stone)  # 賢い配置を使用
        return x, y



