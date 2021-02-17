import sys

import pygame
import random
import math
import snake_object
import colors


class Snake:
    pygame.init()
    DIS = pygame.display.set_mode((800, 600))
    FOOD_ROW = 0
    FOOD_COL = 0

    def __init__(self, snakeList):

        self.dis_H = 800
        self.dis_W = 600
        self.snakeBlock = 10
        self.score1 = 0
        self.score2 = 0
        self.start = True
        self.is_eaten = False
        self.font = pygame.font.SysFont(None, 25, 3)
        self.snakeList = snakeList
        self.game_over = False
        self.player_failed = False
        self.is_a_star_mode = False
        self.all_snake_positions = set()
        self.eaten_self = False

        pygame.display.update()
        pygame.display.set_caption('Snake by Guy')

    def message(self, msg, color, i):
        """
        this method is responsible for displaying msgs to the players on the screen.
        :param msg:
        :param color:
        :param i:
        :return:
        """
        if msg == "Loser!!!":
            Snake.DIS.fill(colors.PURPLE)
            player_lost = "Player " + str(i + 1) + " is the loser!!!"
            mesg = self.font.render(player_lost, True, color)
            mesg2 = self.font.render("Would you like to play another game?", True, color)
            mesg3 = self.font.render("Press Y \ N", True, color)
            Snake.DIS.blit(mesg, [self.dis_W / 2 - 20, self.dis_H / 2 - 150])
            Snake.DIS.blit(mesg2, [self.dis_W / 2 - 80, self.dis_H / 2 - 100])
            Snake.DIS.blit(mesg3, [self.dis_W / 2 + 30, self.dis_H / 2 - 50])

        elif msg == "Score: ":
            if not self.is_a_star_mode:
                mesg = self.font.render("For A* madness press the 'h' key", True, colors.BLUE)
                Snake.DIS.blit(mesg, [self.dis_W / 2 - 50, self.dis_H / 2 - 380])
            else:
                pygame.draw.rect(self.DIS, colors.BLACK, [self.dis_W / 2 - 50, self.dis_H / 2 - 380, 560, 50])
                mesg = self.font.render("To quit A* madness press the 'q' key", True, colors.BLUE)
                Snake.DIS.blit(mesg, [self.dis_W / 2 - 50, self.dis_H / 2 - 380])

            color1 = self.snakeList[0].getColor()
            mesg = self.font.render("Player1 " + msg + str(self.score1), True, color1)
            pygame.draw.rect(self.DIS, colors.BLACK, [self.dis_W / 2 - 190, self.dis_H / 2 - 390, 90, 50])
            Snake.DIS.blit(mesg, [self.dis_W / 2 - 290, self.dis_H / 2 - 380])

            if len(self.snakeList) == 2:
                color2 = self.snakeList[1].getColor()
                mesg = self.font.render("Player2 " + msg + str(self.score2), True, color2)
                pygame.draw.rect(self.DIS, colors.BLACK, [self.dis_W + 120, self.dis_H / 2 - 390, 90, 50])
                Snake.DIS.blit(mesg, [self.dis_W + 20, self.dis_H / 2 - 380])
        pygame.display.update()

    def game_loop(self):
        """
        Runs the game "forever" and catches keyboard events.
        responsible for drawing the 2 snakes each clock tick.
        :return:
        """
        game_begin = True
        Snake.DIS.fill(colors.BLACK)
        row = 50
        col = 50

        while not self.game_over:
            if game_begin:
                for i in range(len(self.snakeList)):
                    node = snake_object.MyNode(row, col)
                    self.snakeList[i].enqueue(node)
                    pygame.draw.rect(Snake.DIS, self.snakeList[i].getColor(),
                                     [self.snakeList[i].getHead().getRow(), self.snakeList[i].getHead().getCol(), 10,
                                      10])
                    pygame.display.update()
                    col += 10
                game_begin = False

            while self.player_failed:
                # self.message("Loser!!!", self.yellow, i)
                for eve in pygame.event.get():
                    if eve.type == pygame.KEYDOWN:
                        if eve.key == pygame.K_y:
                            self.player_failed = False
                            self.game_restart()
                        elif eve.key == pygame.K_n:
                            self.player_failed = False
                            self.game_over = True
                            break

            if self.is_a_star_mode:
                self.a_star_madness()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Snake.game_over = True
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q and self.is_a_star_mode:
                        self.player_failed = False
                        self.snakeList[1].setColor((0, 255, 255))
                        self.game_restart()

                    self.move_player(event, 0)
                    self.move_player(event, 1)

            for i in range(len(self.snakeList)):

                self.snakeList[i].setOldRow(self.snakeList[i].getTail().getRow())
                self.snakeList[i].setOldCol(self.snakeList[i].getTail().getCol())
                oldHeadRow = self.snakeList[i].getHead().getRow()
                oldHeadCol = self.snakeList[i].getHead().getCol()
                self.snakeList[i].tail_to_head()
                pos = self.snakeList[i].getPosList()
                self.snakeList[i].getHead().setRow(oldHeadRow + pos[0])
                self.snakeList[i].getHead().setCol(oldHeadCol + pos[1])

                pygame.draw.rect(Snake.DIS, self.snakeList[i].getColor(),
                                 [self.snakeList[i].getHead().getRow(),
                                  self.snakeList[i].getHead().getCol(), 10, 10])

                self.check_position(i)
                if self.player_failed is True:
                    break

                if self.snakeList[i].getPlayerMoved():
                    pygame.draw.rect(Snake.DIS, colors.BLACK,
                                     [self.snakeList[i].getOldRow(), self.snakeList[i].getOldCol(), 10, 10])

                    # if self.eaten_self:
                    #     pygame.draw.rect(Snake.DIS, self.snakeList[0].getColor(),
                    #                      [self.snakeList[i].getOldRow(), self.snakeList[i].getOldCol(), 10, 10])
                    #     self.eaten_self = False
                    pygame.display.update()

            self.snakeList[0].getClock().tick(self.snakeList[0].getTime())

            self.message("Score: ", colors.NAVY, 0)
            self.random_food()

        pygame.quit()
        quit()

    def a_star_madness(self):
        pygame.draw.rect(Snake.DIS, colors.BLACK,
                         [self.snakeList[1].getHead().getRow(),
                          self.snakeList[1].getHead().getCol(), 10, 10])
        pygame.display.update()
        self.snakeList[1].setColor(colors.BLACK)

        player = self.snakeList[0]
        possible_moves = {"u": [0, self.snakeBlock, "d"], "d": [0, - self.snakeBlock, "u"],
                          "r": [- self.snakeBlock, 0, "l"],
                          "l": [self.snakeBlock, 0, "r"]}  # up, down, right, left

        heuristic_value = sys.maxsize
        for heading, move in possible_moves.items():
            new_position = (player.getHead().getRow() + move[0], player.getHead().getCol() + move[1])
            temp_heuristic = abs(Snake.FOOD_ROW * 10 - new_position[0]) + \
                             abs(Snake.FOOD_COL * 10 - new_position[1])  # manhattan distance heuristic

            if temp_heuristic < heuristic_value and move[2] != player.getHeading:
                heuristic_value = temp_heuristic
                player.setPosList(move)
                player.setHeading(heading)

        self.snakeList[0].setPlayerMoved(True)
        self.check_position(0)

    def move_player(self, event, i):
        """
        catches arrow keys events and by that, sets the heading of each snake.
        :param event:
        :param i:
        :return:
        """

        player = self.snakeList[i]

        if event.key == pygame.K_h:
            self.is_a_star_mode = True

        # player 1
        if i == 0:
            if event.key == pygame.K_DOWN and player.getHeading() is not "u":
                player.setPosList([0, self.snakeBlock])
                player.setHeading("d")
                self.snakeList[0].setPlayerMoved(True)

            elif event.key == pygame.K_UP and player.getHeading() is not "d":
                player.setPosList([0, - self.snakeBlock])
                player.setHeading("u")
                self.snakeList[0].setPlayerMoved(True)

            elif event.key == pygame.K_LEFT and player.getHeading() is not "r":
                player.setPosList([- self.snakeBlock, 0])
                player.setHeading("l")
                self.snakeList[0].setPlayerMoved(True)

            elif event.key == pygame.K_RIGHT and player.getHeading() is not "l":
                player.setPosList([self.snakeBlock, 0])
                player.setHeading("r")
                self.snakeList[0].setPlayerMoved(True)

        # player 2
        else:
            if event.key == pygame.K_s and player.getHeading() is not "u":
                player.setPosList([0, self.snakeBlock])
                player.setHeading("d")
                self.snakeList[1].setPlayerMoved(True)

            elif event.key == pygame.K_w and player.getHeading() is not "d":
                player.setPosList([0, - self.snakeBlock])
                player.setHeading("u")
                self.snakeList[1].setPlayerMoved(True)

            elif event.key == pygame.K_a and player.getHeading() is not "r":
                player.setPosList([- self.snakeBlock, 0])
                player.setHeading("l")
                self.snakeList[1].setPlayerMoved(True)

            elif event.key == pygame.K_d and player.getHeading() is not "l":
                player.setPosList([self.snakeBlock, 0])
                player.setHeading("r")
                self.snakeList[1].setPlayerMoved(True)

    def random_food(self):
        """
        Each time a snake consumes a piece of food, a new piece is drawn on the screen in a random place.
        :return:
        """
        if not self.is_eaten:
            Snake.FOOD_ROW = random.randint(10, 69)
            Snake.FOOD_COL = random.randint(10, 49)
            pygame.draw.rect(Snake.DIS, colors.GREEN, [Snake.FOOD_ROW * 10, Snake.FOOD_COL * 10, 10, 10])
            pygame.display.update()
            self.is_eaten = True

    def check_position(self, i):
        """
        whenever a snake head is located at a piece of food location, the player's score is increased,
        the food is marked as eaten, and the ticks of the clock become more frequent (represented as a log function) .
        Also checks whether the 2 snakes collided and determines the responsible snake for that collision.
        :param i:
        :return:
        """
        if self.FOOD_ROW * 10 == self.snakeList[i].getHead().getRow() and Snake.FOOD_COL * 10 == \
                self.snakeList[i].getHead().getCol():
            pygame.draw.rect(Snake.DIS, colors.BLACK, [self.FOOD_ROW, Snake.FOOD_COL, 10, 10])
            if i == 0:
                self.score1 += 1
            else:
                self.score2 += 1
            myTime = self.snakeList[i].getTime()
            inc = math.log(myTime, 15)  # clock ticks become more frequent.
            self.snakeList[i].setTime(myTime + inc)
            self.is_eaten = False

            node = snake_object.MyNode(self.snakeList[i].getTail().getRow(), self.snakeList[i].getTail().getCol())
            self.snakeList[i].enqueue(node)

        if self.snakeList[i].getHead().getRow() > self.dis_H or self.snakeList[i].getHead().getRow() < 0 or \
                self.snakeList[i].getHead().getCol() > self.dis_W or self.snakeList[i].getHead().getCol() < 0:
            self.side_to_side(i)
            # self.message("Loser!!!", self.yellow, i)

        temp = self.snakeList[i].getTail()
        head = self.snakeList[i].getHead()
        while temp is not head and self.snakeList[i].getSize() > 2:
            if (head.getRow() == temp.getRow()) and (head.getCol() == temp.getCol()) and not self.is_a_star_mode:
                # if self.is_a_star_mode:
                #     self.is_eaten = True
                self.player_failed = True
                self.message("Loser!!!", colors.YELLOW, i)
                break
            temp = temp.getNext()

        otherTemp = self.snakeList[1 - i].getTail()
        otherHead = self.snakeList[1 - i].getHead()
        while otherTemp is not otherHead and self.snakeList[1 - i].getSize() > 2 and not self.is_a_star_mode:
            if (head.getRow() == otherTemp.getRow()) and (head.getCol() == otherTemp.getCol()):
                self.player_failed = True
                self.message("Loser!!!", colors.YELLOW, i)
                break
            otherTemp = otherTemp.getNext()

    def game_restart(self):
        """
        If the players decided to play another game, new snakes are created instead of the previous ones.
        :return:
        """
        snakeLst = []
        self.is_a_star_mode = False
        for i in range(len(self.snakeList)):
            color = self.snakeList[i].getColor()
            snake_to_add = snake_object.SnakeQ(color)
            snakeLst.append(snake_to_add)
        new_snake = Snake(snakeLst)
        new_snake.game_loop()

    def side_to_side(self, i):
        """
        Enables the snakes to move from side to side of the screen when hit the the frame. left to right, top to bottom,
        and vise versa.
        :param i:
        :return:
        """

        pygame.draw.rect(Snake.DIS, colors.BLACK,
                         [self.snakeList[i].getOldRow(), self.snakeList[i].getOldCol(), self.snakeBlock,
                          self.snakeBlock])
        self.snakeList[i].setOldRow(self.snakeList[i].getTail().getRow())
        self.snakeList[i].setOldCol(self.snakeList[i].getTail().getCol())
        oldHeadRow = self.snakeList[i].getHead().getRow()
        oldHeadCol = self.snakeList[i].getHead().getCol()
        self.snakeList[i].tail_to_head()

        if oldHeadRow >= self.dis_H:
            self.snakeList[i].getHead().setRow(oldHeadRow - self.dis_H)

        elif oldHeadRow <= 0:
            self.snakeList[i].getHead().setRow(oldHeadRow + self.dis_H)

        elif oldHeadCol >= self.dis_W:
            self.snakeList[i].getHead().setCol(oldHeadCol - self.dis_W)

        elif oldHeadCol <= 0:
            self.snakeList[i].getHead().setCol(oldHeadCol + self.dis_W)

        pygame.draw.rect(Snake.DIS, self.snakeList[i].getColor(),
                         [self.snakeList[i].getHead().getRow(),
                          self.snakeList[i].getHead().getCol(), self.snakeBlock, self.snakeBlock])
        pygame.display.update()


if __name__ == "__main__":
    snake1 = snake_object.SnakeQ(colors.RED)
    snake2 = snake_object.SnakeQ((0, 255, 255))
    snake_lst = [snake1, snake2]
    snake = Snake(snake_lst)
    snake.game_loop()
