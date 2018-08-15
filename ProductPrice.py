rn_option = {
    0: 0, 1: 3914, 2: 4283, 3: 3130, 4: 3277,
    5: 3261, 6: 3312, 7: 3357, 8: 3892, 9: 0
}
# x = stitches
# y = rn_option
company = {
    "gd": lambda x,y: (10000 if x < 2500 else x * 4, x * 3)[x > 10000],
    "rn": lambda x,y: (2.5, 3)[y == 0] * (2500, x - rn_option[y])[x - rn_option[y] > 2500],
    "sw": lambda x,y: (10000, round(x,-2) * 4)[x > 2500],
    "normal": lambda x,y: (10000, x * 4)[x > 2500]
}
def price(x,z,y=0):
    if z=='ex!@':
        return " "
    if z!='gd' and z!='rn' and z!='sw':
        z='normal'
    return str(int(company[z](int(x),y)))
def modified_stitches(x,y=0):
    print(x)
    return str(int(x)-rn_option[y])

