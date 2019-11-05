
def main():
    f = open("test_file.txt", "r")
    a = []
    f1 = f.readline()
    while f1:
        for x in f1:
            if x == ':' or x == ';':
                a.append(f1)
        f1 = f.readline()
    f.close()
    # print(a)
    temp = []
    for each in a:
        b = each[:-1]
        temp.append(b)
        # if each.__contains__('\n'):
        #     temp.append()
    print(temp)


    # print(f.read())


if __name__ == '__main__':
    main()

