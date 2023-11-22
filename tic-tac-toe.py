import sys
import pygame
import random
import copy
import numpy as np
WIDTH=700
HEIGHT=700
ROW=3
COL=3
SQSIZE=WIDTH//COL
lWIDTH=15
LINE_WIDTH=15
CIRC_WIDTH=15
CROSS_WIDTH=20
RADIUS=SQSIZE//4
OFFSET=50
bg=(255,255,255)
lc=(0,0,0)
CIRC_COLOR=(250,0,0)
CROSS_COLOR=(135,206,250)

pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('TIC-TAC-TOE')
screen.fill(bg)

class Board():

    def __init__(self):
        self.square= np.zeros((ROW,COL))
        self.empty_sqrs=self.square
        self.marked_sqrs=0
    
    def final_state(self,show=False):
        for col in range(COL):
            if self.square[0][col]==self.square[1][col]==self.square[2][col]!=0:
                if show:
                    color=CIRC_COLOR if self.square[0][col]==2 else CROSS_COLOR
                    iPos=(col*SQSIZE+SQSIZE//2,20)
                    fPos=(col*SQSIZE+SQSIZE//2,HEIGHT-20)
                    pygame.draw.line(screen,color,iPos,fPos,LINE_WIDTH)
                return self.square[0][col]
        for row in range(ROW):
            if self.square[row][0]==self.square[row][1]==self.square[row][2]!=0:
                if show:
                    color=CIRC_COLOR if self.square[row][0]==2 else CROSS_COLOR
                    iPos=(20,row*SQSIZE+SQSIZE//2)
                    fPos=(WIDTH-20,row*SQSIZE+SQSIZE//2)
                    pygame.draw.line(screen,color,iPos,fPos,LINE_WIDTH)
                return self.square[row][0]
        
        if self.square[0][0]==self.square[1][1]==self.square[2][2]!=0:
            if show:   
                color=CIRC_COLOR if self.square[1][1]==2 else CROSS_COLOR
                iPos=(20,20)
                fPos=(WIDTH-20,HEIGHT-20)
                pygame.draw.line(screen,color,iPos,fPos,CROSS_WIDTH)
            return self.square[1][1]
        
        if self.square[2][0]==self.square[1][1]==self.square[0][2]!=0:
            if show:
               color=CIRC_COLOR if self.square[1][1]==2 else CROSS_COLOR
               iPos=(20,HEIGHT-20)
               fPos=(WIDTH-20,20)
               pygame.draw.line(screen,color,iPos,fPos,CROSS_WIDTH)
            return self.square[1][1 ]
        return 0
        
    
    def mark_sqr(self,row,col,player):
        self.square[row][col]=player
        self.marked_sqrs+=1
    
    def empty_sqr(self,row,col):
        return self.square[row][col]==0
    def get_empty_sqrs(self):
        empty_sqrs=[]
        for row in range(ROW):
            for col in range(COL):
                if self.empty_sqr(row,col):
                    empty_sqrs.append((row,col))
        return empty_sqrs
    
    def isfull(self):
        return self.marked_sqrs==9
    
    def isempty(self):
        return self.marked_sqrs==0

class AI():

    def __init__(self,level=0,player=2):
        self.level=level
        self.player=player

    def rnd(self,board):
        empty_sqrs=board.get_empty_sqrs()
        idx=random.randrange(0,len(empty_sqrs))

        return empty_sqrs[idx]
    
    def minmax(self,board,maximizing):
        case=board.final_state()

        if case==1:
            return 1,None
        if case==2:
            return -1,None
        
        elif board.isfull():
            return 0,None
        
        if maximizing:
            max_eval=-100
            best_move=None
            empty_sqrs=board.get_empty_sqrs()
            for (row,col) in empty_sqrs:
                temp_board=copy.deepcopy(board)
                temp_board.mark_sqr(row,col,1)
                eval=self.minmax(temp_board,False)[0]
                if eval > max_eval:
                    max_eval=eval
                    best_move=(row,col)
            
            return max_eval,best_move
        
        elif not maximizing:
            min_eval=100
            best_move=None
            empty_sqrs=board.get_empty_sqrs()
            for (row,col) in empty_sqrs:
                temp_board=copy.deepcopy(board)
                temp_board.mark_sqr(row,col,self.player)
                eval=self.minmax(temp_board,True)[0]
                if eval<min_eval:
                    min_eval=eval
                    best_move=(row,col)
            
            return min_eval,best_move
            

    def eval(self,main_board):
        if self.level==0:
            eval, move=self.minmax(main_board,False)
        print(f'Ai as chosen to mark the square in pos {move}with an eval of:{eval}')

        return move

class Game:
    def __init__(self):
        self.board=Board()
        self.ai=AI()
        self.player=1
        self.gamemode='ai'
        self.runining=True
        self.show_lines()

    def make_move(self,row,col):
        self.board.mark_sqr(row,col,self.player)
        self.draw_fig(row,col)
        self.next_turn()


    def show_lines(self):
        pygame.draw.line(screen,lc,(SQSIZE,0),(SQSIZE,HEIGHT),lWIDTH)
        pygame.draw.line(screen,lc,(WIDTH-SQSIZE,0),(WIDTH-SQSIZE,HEIGHT),lWIDTH)

        pygame.draw.line(screen,lc,(0,SQSIZE),(WIDTH,SQSIZE),lWIDTH)
        pygame.draw.line(screen,lc,(0,HEIGHT-SQSIZE),(WIDTH,HEIGHT-SQSIZE),lWIDTH)
     
    def draw_fig(self,row,col):
        if self.player==1:
            start_desc=(col * SQSIZE + OFFSET,row * SQSIZE + SQSIZE -OFFSET)
            end_desc=(col * SQSIZE + SQSIZE - OFFSET,row * SQSIZE + OFFSET)
            pygame.draw.line(screen,CROSS_COLOR,start_desc,end_desc,CROSS_WIDTH)
            start_asc=(col * SQSIZE + OFFSET,row * SQSIZE + OFFSET)
            end_asc=(col * SQSIZE + SQSIZE - OFFSET,row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen,CROSS_COLOR,start_asc,end_asc,CROSS_WIDTH)
        elif self.player==2:
            center=(col * SQSIZE + SQSIZE // 2,row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen,CIRC_COLOR,center,RADIUS,CIRC_WIDTH)

    def next_turn(self):
        self.player=self.player % 2 + 1
    
    def isover(self):
        return self.board.final_state(show=True)!=0 or self.board.isfull()

def main():
    game=Game()
    board=game.board
    ai=game.ai
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=event.pos
                row=pos[1]//SQSIZE
                col=pos[0]//SQSIZE
            
                if board.empty_sqr(row,col) and game.runining:
                    game.make_move(row,col)
                    if game.isover():
                        game.runining=False

        if game.gamemode=='ai' and game.player==ai.player and game.runining:
            pygame.display.update()
            row,col=ai.eval(board)
            game.make_move(row,col)
            if game.isover():
                game.runining=False
           
        pygame.display.update()

main()