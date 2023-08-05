import random
import sys

import click
from enum import Enum
from time import sleep
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


ascii_ring = """
 ||     __                                                                                                   ||
 ||   __\/__                                                                                                 ||
 ||  //----\\\\                                                                                                ||
 || ||      ||                                                                                               ||
 || ||      ||                                                                                               ||
 ||  \\\\____//                                                                                                ||
 ||    ----                                                                                                  ||
 ||__________________________________________________________________________________________________________||
"""


class Answers(Enum):
    YES = 1
    NO = 0


class Answer:
    def __init__(self, answer: str):
        self.answer = answer.lower()

    def parse(self):
        if self.answer == "y":
            return Answers.YES
        return Answers.NO


def get_years_since_anniversary():
    return (datetime.now() - datetime(2014, 8, 30)).days // 365


def to_std_out(value):
    sys.stdout.write(value)
    sys.stdout.flush()


def write_to_console(value, new_line=True, typing_speed=50):

    count = 0
    for letter in value:
        to_std_out(letter)
        sleep(random.random()*10.0/typing_speed)
        count += 1
        if count >= 100 and letter == " ":
            to_std_out(" "*(104 - count) + " || ")
            print()
            to_std_out(" || ")
            count = 0

    if count < 100:
        to_std_out(" "*(104 - count))

    if new_line:
        print()


def print_and_sleep(to_print: str, sleep_time: int = 0.5, new_line=True):
    to_std_out(" || ")
    write_to_console(to_print, False)
    to_std_out(" || ")
    if new_line:
        print()
    sleep(sleep_time)


def start_fun():
    print(" " + "+"*110)
    print_and_sleep("Hey butts")
    print_and_sleep("Its Matt")
    print(" ||                                                                                                         "
          " ||")
    print_and_sleep(f"We've been dating for {get_years_since_anniversary()} years")
    print_and_sleep("When we met at anime expo in 2014 I never would have thought we would then bond later over a "
                    "silly over dub of a show that would lead us to spending nights talking over messenger.")
    print_and_sleep("I remember talking to my mom later about this girl that I've been talking too and how I've never "
                    "really connected before with anyone on that kind of level so quickly.")
    print_and_sleep("With you, I never felt the need to be someone I'm not. I can always be myself and nerd out (like "
                    "I'm doing now) or just talk at length about some anime or book I'm reading. When I do I usually "
                    "look back and see a big smile on your face.")
    print_and_sleep("I live for those moments.")
    print_and_sleep("Even if my day was going poorly or I was struggling I always knew if I could make you smile that "
                    "none of the other stuff or struggles would matter.")
    print_and_sleep("I want nothing more than to make you smile.")
    print_and_sleep("I wish I could be there with you in person to give you the real thing, "
                    "but at the moment this is the best I can do.", new_line=False)
    sleep(2)
    print(ascii_ring)
    return Answer(input("Will you marry me?"))



def stop_fun():
    pass


def is_denise(answer: Answer):
    if answer.parse():
        return start_fun()
    return stop_fun()


@click.command()
def love():
    answer = Answer(input("Is your name Denise? [y]/n ") or "Y")
    is_denise(answer)


def start():
    love()
