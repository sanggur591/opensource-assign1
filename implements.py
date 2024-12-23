import math
import random
import time

import config

import pygame
from pygame.locals import Rect, K_LEFT, K_RIGHT



class Basic:
    def __init__(self, color: tuple, speed: int = 0, pos: tuple = (0, 0), size: tuple = (0, 0)):
        self.color = color
        self.rect = Rect(pos[0], pos[1], size[0], size[1])
        self.center = (self.rect.centerx, self.rect.centery)
        self.speed = speed
        self.start_time = time.time()
        self.dir = 270

    def move(self):
        dx = math.cos(math.radians(self.dir)) * self.speed
        dy = -math.sin(math.radians(self.dir)) * self.speed
        self.rect.move_ip(dx, dy)
        self.center = (self.rect.centerx, self.rect.centery)


class Block(Basic):
    def __init__(self, color: tuple, pos: tuple = (0, 0), layer: int = 0, alive=True):
        """
        color: 블록의 초기 색상
        pos: 블록의 위치
        layer: 블록의 층 (회색은 0, 나머지는 1 이상)
        """
        super().__init__(color, 0, pos, config.block_size)
        self.layer = layer  # 층 정보
        self.alive = alive
        self.collision_count = 0  # 회색 블록의 충돌 횟수

    def draw(self, surface) -> None:
        if self.alive:
            pygame.draw.rect(surface, self.color, self.rect)

    def collide(self):
        deleted = False
        if not self.alive:
            return 

        if self.layer == 0:  # 회색 블록
            self.collision_count += 1
            if self.collision_count <= config.collision_limit:
            
                self.color = config.colors[self.collision_count]
            else:
                self.alive = False
                self.rect.width = 0
                self.rect.height = 0
                deleted = True
                
             
        else:  # 나머지블록
            self.alive = False
            self.rect.width = 0
            self.rect.height = 0
            deleted = True
        
        return deleted
            


class Paddle(Basic):
    def __init__(self):
        super().__init__(config.paddle_color, 0, config.paddle_pos, config.paddle_size)
        self.start_pos = config.paddle_pos
        self.speed = config.paddle_speed
        self.cur_size = config.paddle_size

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move_paddle(self, event: pygame.event.Event):
        if event.key == K_LEFT and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        elif event.key == K_RIGHT and self.rect.right < config.display_dimension[0]:
            self.rect.move_ip(self.speed, 0)


class Ball(Basic):
    def __init__(self, pos: tuple = config.ball_pos, color: tuple = config.ball_color):
        super().__init__(color, config.ball_speed, pos, config.ball_size)
        self.power = 1
        self.dir = 90 + random.randint(-45, 45)

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def draw_item(self, surface, pos: tuple, color: tuple):
        temp_rect = self.rect.copy() 
        temp_rect.topleft = pos 
        pygame.draw.ellipse(surface, color, temp_rect)

    def collide_block(self, blocks: list):
        # ============================================
        # TODO: Implement an event when the ball hits a block
        for block in blocks:
            collided = False
            if self.rect.colliderect(block.rect[0], block.rect[1], block.rect.width, 1):
                self.dir = 360 - self.dir + random.randint(-5, 5)
                collided = True
                
            elif self.rect.colliderect(block.rect[0], block.rect[1] + block.rect.height - 1, block.rect.width, 1):
                self.dir = 360 - self.dir + random.randint(-5, 5)
                collided = True
                

            elif self.rect.colliderect(block.rect[0], block.rect[1], 1, block.rect.height):
                self.dir = 180 - self.dir + random.randint(-5, 5)
                collided = True
            
            elif self.rect.colliderect(block.rect[0] + block.rect.width - 1 , block.rect[1], 1, block.rect.height):
                self.dir = 180 - self.dir + random.randint(-5, 5)
                collided = True


            if collided == True and block.collide() == True:
                pos = ((block.rect[0]+config.block_size[0]/2),(block.rect[1]+config.block_size[1]/2))
                color = config.ball_red if block.layer == 0 else config.ball_blue
                item = Ball(pos = pos, color = color)
                return item

                


    def collide_paddle(self, paddle: Paddle) -> None:
        if self.rect.colliderect(paddle.rect):
            self.dir = 360 - self.dir + random.randint(-5, 5)

    def hit_wall(self):
        # ============================================
        # TODO: Implement a service that bounces off when the ball hits the wall
        pass
        # 좌우 벽 충돌
        if self.rect.colliderect(Rect((0,0),(config.wall_width, config.display_dimension[1]))) :
            self.dir = 180 - self.dir
        
        if self.rect.colliderect(Rect((config.display_dimension[0] - config.wall_width ,0),(config.wall_width, config.display_dimension[1]))) :
            self.dir = 180 - self.dir
        
        # 상단 벽 충돌
        if self.rect.colliderect(Rect(0, 0, config.display_dimension[0], config.wall_width)) :
            self.dir = 360 - self.dir
    
    def alive(self):
        # ============================================
        # TODO: Implement a service that returns whether the ball is alive or not
        if self.center[1] > config.display_dimension[1] :
            return False
        else :
            return True
        
