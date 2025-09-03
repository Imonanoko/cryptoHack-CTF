state = [
    [206, 243, 61, 34],
    [171, 11, 93, 31],
    [16, 200, 91, 108],
    [150, 3, 194, 51],
]

round_key = [
    [173, 129, 68, 82],
    [223, 100, 38, 109],
    [32, 189, 53, 8],
    [253, 48, 187, 78],
]


def add_round_key(s, k):
    res = []
    for i in range(0,len(s)):
        res.append([])
        for j in range(0,len(s[0])):
            res[i].append(s[i][j] ^ k[i][j])
    return res
        
def matrix2bytes(matrix):
    """ Converts a 4x4 matrix into a 16-byte array.  """
    text = ''
    for i in range(0,len(matrix)):
        for j in range(0,len(matrix[0])):
            text = text + chr(matrix[i][j])
    return text

print(matrix2bytes(add_round_key(state, round_key)))

