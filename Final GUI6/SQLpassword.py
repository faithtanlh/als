with open('SQLpassword.txt') as f:
    lines = f.readlines()

my_password = lines[0]

def get_password():
    return my_password