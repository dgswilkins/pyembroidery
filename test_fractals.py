import math
import pyembroidery.EmbPattern as EmbPattern


def evaluate_lsystem(symbol, rules, depth):
    if depth <= 0 or symbol not in rules:
        symbol()
    else:
        for produced_symbol in rules[symbol]:
            evaluate_lsystem(produced_symbol, rules, depth - 1)


class Turtle:
    def __init__(self, pattern):
        self.pattern = pattern
        self.angle = 0
        self.x = 0
        self.y = 0
        import math
        self.turn_amount = math.pi / 3

    def forward(self, distance):
        self.x += distance * math.cos(self.angle)
        self.y += distance * math.sin(self.angle)
        self.pattern.add_stitch_absolute(self.x, self.y, EmbPattern.STITCH)

    def turn(self, angle):
        self.angle += angle

    def move(self, distance):
        self.x += distance * math.cos(self.angle)
        self.y += distance * math.sin(self.angle)


    def add_gosper(self):
        a = lambda: self.forward(20)
        b = lambda: self.forward(20)
        l = lambda: self.turn(self.turn_amount)
        r = lambda: self.turn(-self.turn_amount)
        initial = lambda: None
        rules = {
            initial: [a],
            a: [a, l, b, l, l, b, r, a, r, r, a, a, r, b, l],
            b: [r, a, l, b, b, l, l, b, l, a, r, r, a, r, b]
        }
        evaluate_lsystem(initial, rules, 5)
        self.pattern.add_stitch_relative(0, 0, EmbPattern.BREAK_COLOR)

    def add_serp(self):
        a = lambda: self.forward(20)
        b = lambda: self.forward(20)
        l = lambda: self.turn(self.turn_amount)
        r = lambda: self.turn(-self.turn_amount)
        initial = lambda: None
        rules = {
            initial: [a],
            a: [b, l, a, l, b],
            b: [a, r, b, r, a]
        }
        evaluate_lsystem(initial, rules, 6)
        self.pattern.add_stitch_relative(0, 0, EmbPattern.BREAK_COLOR)


def generate(pattern):
    turtle = Turtle(pattern);
    turtle.add_gosper()
    turtle.move(500)
    turtle.add_serp()
    turtle.move(500)
    turtle.add_gosper()
    pattern.add_stitch_absolute(0, 0, EmbPattern.END)
