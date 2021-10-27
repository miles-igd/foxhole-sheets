import cv2
import sys, string

def get_input():
    in_ = []
    while True:
        k = cv2.waitKey()
        if k==27 or k==13:
            break
        elif k==8:
            try:
                in_.pop()
                sys.stdout.write("\b \b")
                sys.stdout.flush()
            except IndexError:
                continue
        else:
            char = chr(k)
            if char not in string.printable:
                continue
            print(chr(k), end='', flush=True)
            in_.append(chr(k))
    print("")

    return "".join(in_)

def ident_item(im, output="", save=True):
    cv2.imshow("Identify this:", im)

    identity = get_input()
    if save:
        cv2.imwrite(output+identity+".png", im)
    return identity

def ident_num(im):
    cv2.imshow("Identify this:", im)

    identity = get_input()

    return identity
