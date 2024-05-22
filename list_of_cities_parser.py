with open("list_of_cities.txt") as file:
    data1 = [
        (i.split()[2:4], int(i.split()[-1])) if i.split()[1].isdigit() or i.split()[1] == "—" else (i.split()[1:3], int(i.split()[-1]))
        for i in file.readlines()
    ]
    data2 = [(i[0][0], i[1]) if i[0][1].isdigit() or i[0][1] == "—" else (i[0][0] + " " + i[0][1], i[1]) for i in data1]
    data3 = [(i[0][:-3], i[1]) if "[" in i[0] else (i[0], i[1]) for i in data2]
    data4 = [(i[0][:-3], i[1]) if "[" in i[0] else (i[0], i[1]) for i in data3]
    data5 = [(i[0][:-3], i[1]) if "[" in i[0] else (i[0], i[1]) for i in data4]
    print(*data5, sep=",\n")
