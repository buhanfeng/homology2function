import datetime
import pandas as pd
import numpy as np


def getFromJson(url):
    pass


def getFromXml(xml):
    pass


def getDateStr():
    x = datetime.datetime.now()
    return str(x)


def consoleLog(*mes):
    print(' '.join(mes))


def getDfIndexByValue(df, col, values):
    m = max(df.index)
    ret = []
    for e in values:
        r = df.loc[df[col] == e]
        if r is not None:
            ret.append(list(r.index))
        else:
            ret.append(m)
            m += 1
    return ret


def updateTable(left, right, left_on, right_on, updateKey):
    left = left.merge(right, how='left', left_on=left_on, right_on=right_on)
    print(left.dtypes)
    if updateKey:
        # left.apply(func=anonymous, axis=1, arg=updateKey)
        for k, v in updateKey.items():
            # left[k] = np.where(pd.notna(left[k]) & pd.notna(left[v] & (left[v] not in left[k])), left[k] + ' # ' + left[v], left[k])
            left[k] = np.where(pd.isna(left[k]) & pd.notna(left[v]), left[v], left[k])
        for k, v in updateKey.items():
            del left[v]
    del left[right_on]
    return left


def anonymous(a, arg):
    for k, v in arg.items():
        if pd.isna(a[v]):
            continue
        elif pd.isna(a[k]):
            a.loc[k] = a[v]
        else:
            a.loc[k] = a[k] + ' # ' + a[v]
    return a
