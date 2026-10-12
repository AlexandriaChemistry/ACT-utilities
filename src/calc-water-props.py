#!/usr/bin/env python3

import math

def do_one4(model:str, bondlength:float, angle: float, dM: float):
    vsite3a = dM/(2*bondlength*math.cos(math.pi*angle/(180*2)))
    print(f"{model} bondlength {bondlength} angle {angle} dM {dM} vsite3a {vsite3a}")
    
def do_one5(model:str, bondlength:float, angleHOH: float, rOL: float, angleLOL:float):
    # The position of the virtual sites in TIP5P is computed as follows:
    #
    # The distance from OW to L is 0.07 nm, the geometry is tetrahedral
    # (109.47 deg)
    # Therefore, a = b = 0.07 * cos (109.47/2) / | xOH1 + xOH2 |
    #            c = 0.07 * sin (109.47/2) / | xOH1 X xOH2 |
    #
    # Using | xOH1 X xOH2 | = | xOH1 | | xOH2 | sin (H1-O-H2)
    #       | xOH1 + xOH2 | = 2 | xOH1 | cos (H1-O-H2)
    # Vsite pos x4 = x1 + a*x21 + b*x31 + c*(x21 X x31)
    # In general
    # a = b = rOL * cos(angle/2)/ (2 bondlength)
    # c = rOL * sin(angle/2) / ( xOH1 X xOH2 )
    ang_hoh = math.pi*angleHOH/180
    ang_lol = math.pi*angleLOL/180
    a = rOL * math.cos(ang_lol/2) / (2 * bondlength * math.cos(ang_hoh/2))
    c = rOL * math.sin(ang_lol/2) / (bondlength**2 * math.sin(ang_hoh))
    print(f"{model}: bondlength {bondlength} angleHOH {angleHOH} angleLOL {angleLOL} rOL {rOL} a {a} c {c}")

def calc_alpha(model:str, qshell:float, kshell:float):
    ONE_4PI_EPS0 = 138.93545758
    alpha = 1000*ONE_4PI_EPS0*qshell**2/(kshell)
    print(f"{model}: qshell {qshell} kshell {kshell} alpha {alpha}")
    
if __name__ == "__main__":
    do_one4("TIP4P", 0.09572, 104.52, 0.015)
    do_one4("COS/G2", 0.09572, 104.52, 0.022)
    do_one4("COS/G3", 0.1, 109.47, 0.015)
    do_one4("SWM6", 0.09572, 104.52, 0.0247)

    do_one5("TIP5P", 0.09572, 104.52, 0.07, 109.47)
    do_one5("SWM6", 0.09572, 104.52, 0.0315, 101.098)
    calc_alpha("SWM6", 1.62789, 418400)
    calc_alpha("SWM3", 1.3828, 418400)
    
