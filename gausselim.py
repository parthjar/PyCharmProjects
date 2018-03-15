def answer(pegs):
    if len(pegs)<=1: return [-1,-1]  # can't achieve double RPM if there is only 1 peg
    d = []  # this is going to be the distance matrix, it will have values for distance betweeen pegs
    for i in range(len(pegs)-1):
        d.append(pegs[i+1]-pegs[i])  # calculate distance between pegs and append to d
        # print(d)
    r = identity(len(pegs)-1)  # start to build the set of simultaneous equations, start with identity matrix
    # print(r)
    for i,row in enumerate(r):
        if i == (len(r)-1):
            r[i][0]=1/2  # for last row/equation: set first gear should have half radius of last gear
            # print(r)
        else:
            r[i][i+1] = 1  # for all other rows/equation: set requirement that distance should be sum of radius of gears
            # print(r)
        row.append(d[i])  # add distance column to r
    # print(r)
    S = my_gauss_elim(r)  # perform gauss elimination to find solution
    # print(S)
    Sq=[]  # pre-define Sq, will be S matrix without the last column
    for row in S:
        if row[-1] < 1:  # all gears should have radius of 1 or more, if not, return [-1,-1]
            return [-1,-1]
        Sq.append(row[:-1])
    # print(Sq)
    if Sq != identity(len(Sq)):  # check is Sq is an identity matrix, if not, a solution doesn't exisit
        return [-1,-1]

    ans = S[0][-1]  # if code reaches here, the solution exists
    # print(ans)
    from decimal import Decimal
    from fractions import Fraction
    # dec = Decimal(ans)
    # ans_frac = Fraction(dec).limit_denominator()
    ans_list = [ans.numerator,ans.denominator] #return numerator and denominator as a list
    return ans_list  # return solution


def identity(size):
    # this function returns a square identity matrix of length size
    ans = []
    for row in range(0, size):
        ans.append([])
        for col in range(0, size):
            if row == col:
                ans[row].append(1)
            else:
                ans[row].append(0)
    return ans


def my_gauss_elim(x):
    # this function performs gaussian elimination of the provided matrix and
    # returns a new matrix in reduced row echelon form
    # this function does operations in fraction form
    import copy
    from fractions import Fraction
    M = copy.deepcopy(x)
    if not M: return M  # return nothing if M is empty
    lead = 0  # set column index
    rowCount = len(M)  # number of rows
    columnCount = len(M[0])  # number of columns
    for r in range(rowCount):
        if lead >= columnCount:
            return M
        i = r
        while M[i][lead] == 0:
            i += 1
            if i == rowCount:
                i = r
                lead += 1
                if columnCount == lead:
                    return M
        M[i],M[r] = M[r],M[i]
        lv = M[r][lead]
        M[r] = [Fraction(mrx) / Fraction(lv) for mrx in M[r]]
        for i in range(rowCount):
            if i != r:
                lv = M[i][lead]
                M[i] = [Fraction(iv) - Fraction(lv)*Fraction(rv) for rv,iv in zip(M[r],M[i])]
        lead += 1
    return M

# mtx = [ [ 1, 2, -1, -4],
#         [ 2, 3, -1, -11],
#         [-2, 0, -3, 22],]

# mtx = [ [ 1, 0, -3, -5],
#         [ 0, 1, 2, 4],
#         [0, 0, 0, 0],]
#
# ans = my_gauss_elim(mtx)
# print(ans)
# print(mtx)
#
# for rw in ans:
#   print(', '.join( (str(rv) for rv in rw) ))

ans = answer([5,20,30,40,50,60,70,80,100,120,150,181])
# ans = answer([4,30,50])
print(type(ans[1]))
print(ans)