def solution(size):
    if size == 1:
        return [[1]]
    spiral = []
    # Fill top row with '1's and rest with '0's
    for i in range(size):
        spiral.append([1 if i == 0 else 0] * size)
    # Locations and directions
    row, col = 0, size-1
    hor, ver = 0, 1
    # Loop for the length of the spiral's arm
    for n in range(size-1, 0, -2):
        # Loop for the number of arms of this length
        for m in range(min(2, n)):
            # Loop for each '1' in this arm
            for i in range(n):
                row += ver
                col += hor
                spiral[row][col] = 1
            # Change direction
            hor, ver = -ver, hor
    return spiral

for size in range(5,10):
    test.assert_equals(spiralize(size), solution(size), "Failed for size %i" % size)

for size in range(11,50):
    test.expect(spiralize(size) == solution(size), "Failed for size %i" % size)

test.expect(spiralize(100) == solution(100), "Failed for size 100")
