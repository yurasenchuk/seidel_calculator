def check_float(x):
    try:
        x = float(x)
        if abs(x) > 0.:
            return True
    except ValueError:
        pass
    return False


def validate_matrix(matrix):
    check = True
    for i in matrix:
        for j in i:
            check = check and check_float(j)
    return check


def validate_vector(vector):
    check = True
    for i in vector:
        check = check and check_float(i)
    return check
