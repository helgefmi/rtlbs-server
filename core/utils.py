from decimal import Decimal


def delta_frames(a, b):
    d = int(a) - int(b)
    f = int((a - int(a)) * 100) - int((b - int(b)) * 100)
    if f < 0:
        d -= 1
        f += 60
    if f < 10:
        f = '0{}'.format(f)
    return Decimal('{}.{}'.format(d, f))
