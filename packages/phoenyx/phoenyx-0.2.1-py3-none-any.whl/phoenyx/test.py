# type: ignore
from phoenyx import *

import math as m
import numpy as np
import random as rd

from renderer import *
from menu import *
from slider import *
from button import *
from sandbox import *
from body import *

renderer: Renderer = Renderer(600, 600, "collision")
sandbox: SandBox = SandBox(renderer, 290, 290)

b1: Body
b2: Body
b3: Body


def reset() -> None:
    global b1, b2, b3
    b1.reset()
    b2.reset()
    b3.reset()


def setup() -> None:
    global b1, b2, b3
    renderer.create_menu("options", background=False, color=255, text_color=255, reset=reset)

    b1 = sandbox.new_body(300, 100, 1, 10)
    b2 = sandbox.new_body(290, 80, 1, 10)
    b3 = sandbox.new_body(310, 60, 1, 10)
    sandbox.set_gravity(y=.5)

    renderer.text_size = 15
    renderer.text_color = 255

    renderer.set_background(51)


def draw() -> None:
    global b1, b2, b3
    # renderer.background(51)

    sandbox.update()
    sandbox.show()
    renderer.text(10, 10, f"fps : {round(renderer.fps)}")


if __name__ == "__main__":
    renderer.run(draw, setup=setup)
