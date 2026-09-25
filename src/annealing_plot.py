#!/usr/bin/env python

import plotxvg

def TTT(begin:float, end: float, iter:int, maxiter:int, T0:float):
    return min(T0, max(0.0, T0*(1-(iter-begin*maxiter)/((end-begin)*maxiter))))

def Tlocal(begin:float, end: float, maxgen:int, maxiter:int, T0:float):
    tmpxvg  = "local.xvg"
    with open(tmpxvg, "w") as tmp:
        tmp.write("@xaxis label \"Generation\"\n")
        tmp.write("@yaxis label \"Temperature\"\n")
        for gen in range(maxgen):
            for iter in range(maxiter):
                x = (gen+(1.0*iter)/maxiter)
                if iter < begin*maxiter:
                    y = T0
                elif iter >= end*maxiter:
                    y = 0
                else:
                    y = TTT(begin, end, iter, maxiter, T0)
                tmp.write("%g  %g\n" % ( x, y ) )
    return tmpxvg

def Tmix(begin:float, end: float, maxgen:int, maxiter:int, T0:float):
    tmpxvg  = "mix.xvg"
    with open(tmpxvg, "w") as tmp:
        tmp.write("@xaxis label \"Generation\"\n")
        tmp.write("@yaxis label \"Temperature\"\n")
        for gen in range(maxgen):
            myT0 = (maxgen-gen)*(T0/maxgen)
            for iter in range(maxiter):
                x = (gen+(1.0*iter)/maxiter)
                if iter < begin*maxiter:
                    y = myT0
                elif iter >= end*maxiter:
                    y = 0
                else:
                    y = myT0*(1-(iter-begin*maxiter)/((end-begin)*maxiter))
                tmp.write("%g  %g\n" % ( x, y ) )
    return tmpxvg

def Tmix2(begin:float, end: float, maxgen:int, maxiter:int, T0:float):
    tmpxvg  = "mix2.xvg"
    with open(tmpxvg, "w") as tmp:
        tmp.write("@xaxis label \"Generation\"\n")
        tmp.write("@yaxis label \"Temperature\"\n")
        totiter = maxgen*maxiter
        for gen in range(maxgen):
            myT0 = T0
            if gen > begin*maxgen:
                myT0 = TTT(begin, end, gen, maxgen, T0)
            print(f"gen {gen} myT0 {myT0}")
            for iter in range(maxiter):
                x = (gen+(1.0*iter)/maxiter)
                myiter = gen*maxiter+iter
                if myiter <= begin*totiter:
                    y = myT0
                elif myiter >= end*totiter:
                    y = 0
                else:
                    y = TTT(begin, end, iter, maxiter, myT0)
                tmp.write("%g  %g\n" % ( x, y ) )
    return tmpxvg

def Tglobal(begin:float, end: float, maxgen:int, maxiter:int, T0:float):
    tmpxvg  = "global.xvg"
    with open(tmpxvg, "w") as tmp:
        tmp.write("@xaxis label \"Generation\"\n")
        tmp.write("@yaxis label \"Temperature\"\n")
        totiter = maxgen*maxiter
        for gen in range(maxgen):
            for iter in range(maxiter):
                x = (gen+(1.0*iter)/maxiter)
                myiter = gen*maxiter+iter
                if myiter < begin*totiter:
                    y = T0
                elif myiter >= end*totiter:
                    y = 0
                else:
                    y = T0*(1-(myiter-begin*totiter)/((end-begin)*totiter))
                tmp.write("%g  %g\n" % ( x, y ) )
    return tmpxvg

if __name__ == "__main__":
    maxgen  = 10
    maxiter = 20
    xvgs = [ Tlocal(0.3, 0.8, maxgen, maxiter, 1.0),
             Tmix(0.2, 0.7, maxgen, maxiter, 1.0),
             Tmix2(0.2, 0.7, maxgen, maxiter, 1.0),
             Tglobal(0.3, 0.8, maxgen, maxiter, 1.0) ]
    plotxvg.plot(xvgs, datasetlegends=["Local", "Mix", "Mix2", "Global"],marker=[None,None,None,None],ls=["solid","dashed","dotted","dashdot"],legend_y=0.4)
    
    
