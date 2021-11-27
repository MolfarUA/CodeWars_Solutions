def count_bits(n):
    bit_string = "{0:#b}".format(n)
    one_count = bit_string.count("1")

    return one_count
