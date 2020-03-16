from random import randint
import math

def main():
    u = [[randint(0,1) for i in range(x, x + 32)] for x in range(0, 32 * 32, 32)]
    for i in u:
        print(i)

    nu = [[[x[i] for i in range(h, h + 8)] for x in [u[y] for y in range(v, v + 8)]] for v in range(0, 32, 8) for h in range(0, 32, 8)]


if __name__ == "__main__":
    main()