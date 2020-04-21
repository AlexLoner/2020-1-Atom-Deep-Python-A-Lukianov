def mtx():
    n = 6
    first =  [[i + 1 for i in range(6)] for j in range(n)]
    second = [[i + 1 for i in range(6)] for j in range(n)]
    third =  [[0 for i in range(6)] for j in range(n)]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                third[i][j] += first[i][k] * second[k][j]
    print(third)