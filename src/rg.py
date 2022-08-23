import pandas as pd
import time

def basic_set(df):
    basic = {}
    for i in df.drop_duplicates().values.tolist():
        basic[str(i)] = []
        for j, k in enumerate(df.values.tolist()):
            if k == i:
                basic[str(i)].append(j)

    return basic

def rough_set(data):
    data = data.dropna(axis=0, how='any')
    x_data = data.drop(['judge'], axis=1)
    y_data = data.loc[:, 'judge']

    y_basic_set = sorted([v for k, v in basic_set(y_data).items()])

    x_basic_set = sorted([v for k, v in basic_set(x_data).items()])
    pos = []
    for i in x_basic_set:
        for j in y_basic_set:
            if set(i).issubset(j):
                pos.append(i)
    pos.sort()
    print("x_basic_set",x_basic_set)
    print("y_basic_set",y_basic_set)
    print ('y的x正域Pos_x(y): ',pos)
    r_x_y = len([k for i in pos for k in i]) / (len(data))

    u = locals()
    pos_va = locals()
    r = locals()
    columns_num = list(range(len(x_data.columns)))

    imp_core = []

    imp_attr = []
    for i in columns_num:
        c = columns_num.copy()
        c.remove(i)
        u = data.iloc[:, c]
        u = sorted([v for k, v in basic_set(u).items()])
        pos_va = []
        for k in u:
            for j in y_basic_set:
                if set(k).issubset(j):
                    pos_va.append(k)
        if sorted(pos_va) != pos:
            imp_core.append(i)
        r = len(sorted(pos_va)) / len(data)
        r_diff = round(r_x_y - r, 4)

        imp_attr.append(r_diff)

    dict_imp = {}
    for o, p in enumerate(imp_attr):
        dict_imp[data.columns[o]] = p

    result = dict_imp
    sorted_dict_imp = sorted(dict_imp, key=lambda x: dict_imp[x], reverse=True)
    sorted_dict_imp = list(map(lambda x: {x: dict_imp[x]}, sorted_dict_imp))
    imp_core = [data.columns[i] for i in imp_core]

    print('Attribute importance is:', sorted_dict_imp)
    # print('Core attribute is：', imp_core)

    return result

def deal(data):

    len = data.iloc[:,0].size

    if len%500 != 0:
        if len > 500:
            num = len//500+1
        else:
            num = 1
    else:
        if len > 500:
            num = int(len/500)
        else:
            num = 1
    arr = [[]]*num

    count = 0
    for i in arr:

        if num == 1:
            arr[count] = data.iloc[0:len]
        elif count == num - 1:
            arr[count] = data.iloc[500 * count:len]
        else:
            arr[count] = data.iloc[500 * count:(count + 1) * 500]
        count = count + 1
    sorted_dict_imp = [[]]*num
    total = [0]*27
    title = ['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','C14','C15','C16','C17','C18','C19','C20','C21','C22','C23','C24','C25','C26','C27']

    count = 0
    for i in arr:
        print('--------------------------------------------------'%(count+1))
        sorted_dict_imp[count] = rough_set(i)
        count = count + 1
    count1 = 0

    for i in sorted_dict_imp:
        count = 0
        if count1 == 0:
            for j in title:
                total[count] = i.get(j)
                count = count + 1
        else:
            for z in title:
                total[count] = i.get(z) + total[count]
                count = count + 1
        count1 = count1 + 1

    count = 0
    for i in title:
        print(i,':',round(total[count],4))
        count = count + 1


def main():
    time1 = time.time()

    data = pd.read_csv(filepath_or_buffer='/data1.csv')
    deal(data)
    time2 = time.time()
    print(time2-time1)


if __name__ == '__main__':
    main()