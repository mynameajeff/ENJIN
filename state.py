
import pygame
import re

class current_variables:

    # labels = {}
    assets = {}
    variables = {}
    constants = {}

    # collecting_label = False
    # current_label = None

def asset_decl(expression):
    current_variables.assets[str(expression[1][0])] = \
        pygame.image.load(expression[1][1])


def asset_show(expression, method_check):

    if expression[1][2][0][1:] == current_variables.scr and len(expression[1][2]) == method_check["ASSET"]["show"][0]:

        if not re.match("[^$A-Za-z_-][0-9]*", expression[1][2][1]):

            peram_0 = current_variables.variables[expression[1][2][1][1:]]

        else:
            peram_0 = expression[1][2][1]

        if not re.match("[^$A-Za-z_-][0-9]*", expression[1][2][2]):

            peram_1 = current_variables.variables[expression[1][2][2][1:]]

        else:
            peram_1 = expression[1][2][2]

        return (current_variables.assets[expression[1][0][1:]], (float(peram_0), float(peram_1)))

    else:
        raise TypeError("Invalid Parameters Given.")


def var_decl(expression):

    current_variables.variables[str(expression[1][0])] = expression[1][1]


def var_incr(expression, loop = False):

    loc = expression[1][0][1:]

    if loc in current_variables.variables:

        var = current_variables.variables[loc]

        try:
            var = float(var)

        except ValueError:

            raise ValueError(
                ".incr property could not be issued on Variable \"{0:s}\", with value {1:s}."
                .format(loc, current_variables.variables[loc])
            )

        current_variables.variables[loc] = float(var) + 1


def label_begin(expression):

    current_variables.collecting_label = True
    current_variables.current_label = str(expression[1])

    current_variables.labels[str(expression[1])] = []


def label_end():

    current_variables.collecting_label = False


def init_screen(expression):

    current_variables.scr = expression[1][0]

    parameter = []

    for i in range(2):

        if not re.match("[0-9]", expression[1][1][i]):

            parameter.append(float(current_variables.constants[
                str(expression[1][1][i][1:])
            ]))

        else:
            parameter.append(float(expression[1][1][i]))

    return tuple(parameter)


def init_property(expression, method_check):

    if expression[1][0][1:] == current_variables.scr:
    
        if expression[1][1] in method_check["SCREEN"]:

            method = method_check["SCREEN"][expression[1][1]]

            if isinstance(expression[1][2], str) and expression[1][2][0] == "$":
                
                return current_variables.constants[
                    str(expression[1][2][1:])
                ]

            else:
                return expression[1][2]


def init_method(expression, screen_dimensions, title, isResizable):

    screen_dimensions = [int(x) for x in list(screen_dimensions)]

    if expression[1][1] == "create":

        return pygame.display.set_mode(
            screen_dimensions,
            isResizable
        )


def init_constant(expression):

    current_variables.constants[str(expression[1][0])] = expression[1][1]
