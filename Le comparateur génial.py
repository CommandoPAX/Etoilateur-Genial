f1 = open("inlist_project", "r")
f2 = open("inlist_project2", "r")

for i in range(100) :
    l1 = f1.readline()
    l2 = f2.readline()

    if l1 != l2 : print(i, l1, l2)
