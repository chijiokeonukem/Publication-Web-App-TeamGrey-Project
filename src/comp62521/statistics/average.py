
def mean(X):
    n = len(X)
    if n > 0:
        return float(sum(X)) / float(len(X))
    return 0


def median(X):
    n = len(X)
    if n == 0:
        return 0
    L = sorted(X)
    if n % 2:
        return L[n / 2]
    return mean(L[(n / 2) - 1:(n / 2) + 1])

def mode(X):
    n = len(X)
    if n == 0:
        return []

    d = {}
    for item in X:
        if d.has_key(item):
            d[item] += 1
        else:
            d[item] = 1

    m = (0, 0)
    for key in d.keys():
        if d[key] > m[1]:
            m = (key, d[key])

    largest = d[max(d, key=d.get)]              # Get the largest occurrance
    m = [x for x in d.keys() if d[x]==largest]	# Calculate the mode by finding the values that occurred 'largest' number of times

    return m
