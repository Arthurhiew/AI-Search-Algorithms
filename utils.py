def readFile(filename):
    f = open(filename, "r")
    print("Parsing file...: ", filename)
    leftbank = [int(i) for i in f.readline().split(",")]
    rightbank = [int(i) for i in f.readline().split(",")]
    f.close()
    state = {"leftBank": leftbank,
             "rightBank": rightbank
             }
    print("Done.")
    return state


def outputSolutionToFile(filename, path,  expandedCount):
    f = open(filename, "w")
    print("Writing to file:", filename)
    # for i in enumerate
    f.write("Number of Nodes Expanded: %d\n" % (expandedCount))
    for i, item in enumerate(path):
        f.write("%d.\t Left Bank: %d chickens, %d wolves, %d boat\t\tRight Bank: , %d chickens, %d wolves, %d boat\n" %
                (i+1, item[0][0], item[0][1], item[0][2], item[1][0], item[1][1], item[1][2]))
        print(i+1, ".\tLeft Bank: ", item[0][0], "chickens, ", item[0][1],  "wolves, ", item[0][2],
              "boat\t Right Bank: ", item[1][0], "chickens, ", item[1][1], "wolves, ", item[1][2], "boat")
    f.close()
    print("Done.")
