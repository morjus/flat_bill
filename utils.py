import sys
from typing import Type


def input_handler(text: str, return_type: Type[float] | Type[int] = None):
    var = input(text)
    if return_type:
        while True:
            try:
                var = return_type(var)
                break
            except ValueError:
                if var in ("q", "Q"):
                    sys.exit()
                print("Not correct value! Try again! Or type 'Q' for exit")
                var = input(text)
                continue
    return var
