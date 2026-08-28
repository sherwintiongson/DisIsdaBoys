def test_dictionary():
    start = 33319
    end = 30093
    lut = {"-50C": start,
           "-25C": 33199,
           "0C": 32923,
           "25C": 31893,
           "50C": 31643,
           "75C": 30613,
           "100": end}
    for x in lut:
        print(lut[x])
    lut["105C"] = 40000
    for x in lut:
        print(lut[x])

