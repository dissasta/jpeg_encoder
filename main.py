import os, binascii, math
global blk_size, width, height

input = "d:\\jpeg-test.tga"
output = "d:\\out.jpg"
width = 128
height = 128
blk_size = 8

Y_qM = ([16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99],)

def dct(channel, downsample=1):
        result = [[[] for x in range(blk_size)] for i in range(int(width/downsample*height/downsample/(blk_size**2)))]
        for blk in range(len(channel)):
            norm_u = 1/math.sqrt(2)

            for u in range(blk_size):
                if u != 0:
                     norm_u = 1

                for v in range(blk_size):
                    sum = 0.0

                    if v != 0:
                        norm_v = 1
                    else:
                        norm_v = 1/math.sqrt(2)

                    for y in range(blk_size):
                        for (x, val) in enumerate(channel[blk][y]):
                            sum += val * math.cos(((2*y+1)*u*math.pi)/16)*math.cos(((2*x+1)*v*math.pi)/16)

                    result[blk][u].append(round(norm_u*norm_v*sum/4, 2))

        return result

def main():
    with open(input, 'rb') as file:
        file.seek(18)
        pxlData = [byte for byte in file.read()]
        pxlArray = [[pxlData[i:i+3] for i in range(x, x + width * 4, 4)] for x in range(0, height * width * 4, width * 4)]

        #converting pixel array into three separate luminance(Y) and chrominance(U,V) channels
        Y = [[int(0.299 * i[2] + 0.587 * i[1] + 0.114 * i[0]) for i in x] for x in pxlArray]
        U = [[int(-0.1687 * i[2] - 0.3313 * i[1] + 0.5 * i[0] + 128) for i in x] for x in pxlArray]
        V = [[int(0.5 * i[2] - 0.4187 * i[1] - 0.0813 * i[0] + 128) for i in x] for x in pxlArray]

        #downsampling chrominance down to 4:2:0 by reducing vertical and horizontal resolution by a factor of 2
        d_U = [[x[i] for i in range(width) if not i % 2] for x in [U[y] for y in range(height) if not y % 2]]
        d_V = [[x[i] for i in range(width) if not i % 2] for x in [V[y] for y in range(height) if not y % 2]]

        #transforming each channel into 8x8 8bit sub-images
        n_Y = [[[x[i] for i in range(h, h + blk_size)] for x in [Y[y] for y in range(v, v + blk_size)]] for v in range(0, height, blk_size) for h in range(0, width,blk_size)]
        n_dU = [[[x[i] for i in range(h, h + blk_size)] for x in [d_U[y] for y in range(v, v + blk_size)]] for v in range(0, int(height / 2), blk_size) for h in range(0, int(width / 2), blk_size)]
        n_dV = [[[x[i] for i in range(h, h + blk_size)] for x in [d_V[y] for y in range(v, v + blk_size)]] for v in range(0, int(height / 2), blk_size) for h in range(0, int(width / 2), blk_size)]

        #shifting values from positive range to ones centered on zero by subtracting 128 from each value in each specific 8x8 sub-image
        for x in range(len(n_Y)):
            for y in range(len(n_Y[x])):
                for z in range(len(n_Y[x][y])):
                    n_Y[x][y][z] -= 128

        for x in range(len(n_dU)):
            for y in range(len(n_dU[x])):
                for z in range(len(n_dU[x][y])):
                    n_dU[x][y][z] -= 128

        for x in range(len(n_dV)):
            for y in range(len(n_dV[x])):
                for z in range(len(n_dV[x][y])):
                    n_dV[x][y][z] -= 128
        n_Y[0][0][0] = -76
        n_Y[0][0][1] = -73
        n_Y[0][0][2] = -67
        n_Y[0][0][3] = -62
        n_Y[0][0][4] = -58
        n_Y[0][0][5] = -67
        n_Y[0][0][6] = -64
        n_Y[0][0][7] = -55
        n_Y[0][1][0] = -65
        n_Y[0][1][1] = -69
        n_Y[0][1][2] = -73
        n_Y[0][1][3] = -38
        n_Y[0][1][4] = -19
        n_Y[0][1][5] = -43
        n_Y[0][1][6] = -59
        n_Y[0][1][7] = -56
        n_Y[0][2][0] = -66
        n_Y[0][2][1] = -69
        n_Y[0][2][2] = -60
        n_Y[0][2][3] = -15
        n_Y[0][2][4] = 16
        n_Y[0][2][5] = -24
        n_Y[0][2][6] = -62
        n_Y[0][2][7] = -55
        n_Y[0][3][0] = -65
        n_Y[0][3][1] = -70
        n_Y[0][3][2] = -57
        n_Y[0][3][3] = -6
        n_Y[0][3][4] = 26
        n_Y[0][3][5] = -22
        n_Y[0][3][6] = -58
        n_Y[0][3][7] = -59
        n_Y[0][4][0] = -61
        n_Y[0][4][1] = -67
        n_Y[0][4][2] = -60
        n_Y[0][4][3] = -24
        n_Y[0][4][4] = -2
        n_Y[0][4][5] = -40
        n_Y[0][4][6] = -60
        n_Y[0][4][7] = -58
        n_Y[0][5][0] = -49
        n_Y[0][5][1] = -63
        n_Y[0][5][2] = -68
        n_Y[0][5][3] = -58
        n_Y[0][5][4] = -51
        n_Y[0][5][5] = -60
        n_Y[0][5][6] = -70
        n_Y[0][5][7] = -53
        n_Y[0][6][0] = -43
        n_Y[0][6][1] = -57
        n_Y[0][6][2] = -64
        n_Y[0][6][3] = -69
        n_Y[0][6][4] = -73
        n_Y[0][6][5] = -67
        n_Y[0][6][6] = -63
        n_Y[0][6][7] = -45
        n_Y[0][7][0] = -41
        n_Y[0][7][1] = -49
        n_Y[0][7][2] = -59
        n_Y[0][7][3] = -60
        n_Y[0][7][4] = -63
        n_Y[0][7][5] = -52
        n_Y[0][7][6] = -50
        n_Y[0][7][7] = -34

        dct_Y = dct(n_Y)
        dct_dU = dct(n_dU,2)
        dct_dV = dct(n_dV,2)
        elo = [x for map(lambda x, y: x/y, dct_Y[0][0], Y_qM[0])
        print(next(elo))

if __name__ == "__main__":
    main()