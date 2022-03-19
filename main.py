import pygame

pygame.font.init()

WINNER_FONT = pygame.font.SysFont("comicsans", 100)

WIDTH = 500
HEIGHT = 500
FPS = 60
X_O_SIZE = (160, 160)

BOARD_IMG = pygame.transform.scale(
    pygame.image.load("Assets/board.png"), (WIDTH, HEIGHT)
)
X_IMG = pygame.transform.scale(pygame.image.load("Assets/x.png"), X_O_SIZE)
O_IMG = pygame.transform.scale(pygame.image.load("Assets/o.png"), X_O_SIZE)


class Board:
    def __init__(self):
        self.width = 9
        self.board = [0 for _ in range(self.width)]
        self.turn = "O"

    def change_turn(self) -> str:
        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"
        return self.turn

    def check_winner(self, board: list):
        self.board = board
        hori = self.horizontal_win(self.board)
        vert = self.vertical_win(self.board)
        diag = self.diagonal_win(self.board)
        if hori:
            return hori
        elif vert:
            return vert
        elif diag:
            return diag
        return False

    def horizontal_win(self, board):
        for i in range(3):
            if board[i] == board[i + 3] == board[i + 6]:
                return board[i]
        return False

    def vertical_win(self, board):
        for i in range(9):
            if (
                board[(i + 1) // 3]
                == board[(i + 1) // 3 + 1]
                == board[(i + 1) // 3 + 2]
            ):
                return board[(i + 1) // 3]
        return False

    def diagonal_win(self, board):
        if board[0] == board[4] == board[8]:
            return board[0]
        if board[2] == board[4] == board[6]:
            return board[2]
        return False


class TicTacToe:
    def __init__(self) -> None:
        self.boardc = Board()
        self.COORDS = {
            1: (0, 0),
            2: (170, 0),
            3: (340, 0),
            4: (0, 170),
            5: (170, 170),
            6: (340, 170),
            7: (0, 340),
            8: (170, 340),
            9: (340, 340),
        }
        self.REVERSE_COORDS = {value: key for key, value in self.COORDS.items()}
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")
        self.clock = pygame.time.Clock()
        self.board = self.boardc.board
        self.board_rects = []
        self.run()

    def draw_window(self):
        self.screen.blit(BOARD_IMG, (0, 0))
        for index in range(len(self.board)):
            if self.board[index] == "X":
                self.screen.blit(X_IMG, self.COORDS[index + 1])
            elif self.board[index] == "O":
                self.screen.blit(O_IMG, self.COORDS[index + 1])
            self.board_rects.append(
                pygame.Rect(self.COORDS[index + 1], O_IMG.get_size())
            )
        board = [i for i in self.boardc.board if i != 0]

        if self.boardc.check_winner(self.board):
            winnertext = WINNER_FONT.render(
                f"Winner: {self.boardc.check_winner(self.board)}",
                1,
                (255, 165, 0),
            )
            self.screen.blit(
                winnertext, (WIDTH / 2 - winnertext.get_width() / 2, HEIGHT / 2)
            )
            pygame.time.delay(5000)
            self.running = False
        elif len(board) == 9:
            winnertext = WINNER_FONT.render("Draw", 1, (255, 165, 0))
            self.screen.blit(
                winnertext, (WIDTH / 2 - winnertext.get_width() / 2, HEIGHT / 2)
            )
            pygame.time.delay(5000)
            self.running = False
        pygame.display.update()

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.running = False
                    case pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        for rect in self.board_rects:
                            if rect.collidepoint(x, y):

                                self.board[
                                    self.REVERSE_COORDS[(rect.x, rect.y)] - 1
                                ] = self.boardc.change_turn()

                                self.draw_window()
                                break

            self.draw_window()


TicTacToe()
