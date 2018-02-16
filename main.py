
from pygame.locals import *

import pygame
import yaml
import sys
import re

import state
import par


class main:

    def __init__(self):

        self.type_conversions = {

            "Boolean" : bool,
            "Integer" : int,
            "String"  : str
        }

        with open("store.yaml") as file:
            self.method_check = yaml.load(file)

        file = par.get_data(par.get_parse_tree("example.code"))

        self.isRunning = True

        self.clock = pygame.time.Clock()

        self.isResizable = 0
        self.isTitleSet = False

        self.examine_init(file)
        self.update_loop(file)


    def internal_method(self, expression):

        if expression[1][0][1:] in state.current_variables.assets:

            if expression[1][1] == "show":

                values = state.asset_show(expression, self.method_check)

                self.screen.blit(values[0], values[1])

        elif expression[1][0][1:] in state.current_variables.variables:
            
            if expression[1][1] == "incr":
                state.var_incr(expression)


    def internal_resizable(self, expression):

        types_available = self.method_check["SCREEN"]["resizable"][1]

        if isinstance(types_available, str):

            type_of = self.type_conversions[types_available]

        elif isinstance(types_available, list):

            temp = (False)

            for i in types_available:

                if isinstance(expression[1][2], self.type_conversions[i]):
                    temp = (True, self.type_conversions[i])

            if temp[0]:
                type_of = temp[1]

            else:

                raise TypeError("Invalid Parameters Given.")

        
        if expression[1][2] and isinstance(expression[1][2], type_of):
            self.isResizable = pygame.RESIZABLE

        else:
            self.isResizable = 0


    def examine_init(self, file):

        for expression in file:

            expr_identifier = expression[0]

            if expr_identifier == "Screen":

                self.WIDTH, self.HEIGHT = state.init_screen(expression)

            elif expr_identifier == "Property":

                if expression[1][1] == "title":
                    self.TITLE = state.init_property(expression, self.method_check)
                    self.isTitleSet = True

                elif expression[1][1] == "resizable":
     
                    self.internal_resizable(expression)


            elif expr_identifier == "Method":

                if expression[1][0][0] == "$" and expression[1][0][1:] == state.current_variables.scr:

                    self.screen = state.init_method(
                        expression, 
                        (self.WIDTH, self.HEIGHT), 
                        self.TITLE, 
                        self.isResizable
                    )

                    if self.isTitleSet:
                        pygame.display.set_caption(self.TITLE)

            elif expr_identifier == "Constant":
                
                state.init_constant(expression)


    def examine_loop(self, file):
        
        for expression in file:

            expr_identifier = expression[0]

            if expr_identifier == "Asset":
                
                state.asset_decl(expression)

            elif expr_identifier == "Variable":

                state.var_decl(expression)

            elif expr_identifier == "Method":

                self.internal_method(expression)


    def update_loop(self, file):

        while self.isRunning:
            self.screen.fill((0, 0, 0))

            mousex,mousey = pygame.mouse.get_pos()
            leftm = pygame.mouse.get_pressed()[0]

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()

                elif event.type == pygame.KEYDOWN:

                    if event.key == K_END:
                        running = False
                        sys.exit()

            self.examine_loop(file)

            pygame.display.update()
            self.clock.tick()


main()
