#!/usr/bin/env python3

import math

def do_one(model:str, bondlength:float, angle: float, dM: float):
    vsite3a = dM/(2*bondlength*math.cos(math.pi*angle/(180*2)))
    print(f"{model} bondlength {bondlength} angle {angle} dM {dM} vsite3a {vsite3a}")

if __name__ == "__main__":
    do_one("COS/G2", 0.09572, 104.52, 0.022)
    do_one("COS/G3", 0.1, 109.47, 0.015)
