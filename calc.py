import csv
import math

def entropy(count, all):
    p = count/float(all)
    if p == 0:
        return 0
    return math.log(p, 2) * -p

def information(values, all):
    sum = 0
    for k in values:
        sum += values[k]['count']/float(all) * values[k]['entropy']
    return sum

def gain_Wrong(ent, info):
    return ent - info

def find_Info_And_Gain(data, length, header):
    # print('***')
    # print(data)
    # print('***')
    yes = 0
    no = 0
    for row in data:
        if row[length] == 'Да':
            yes += 1
        else:
            no += 1
    ent = entropy(yes, len(data)) + entropy(no, len(data))
    if yes == 0:
        print('Лист Нет')
        return []
    elif no == 0:
        print('Лист Да')
        return []
    print('I(T) = {0}/{2} * log2({0}/{2}) + {1}/{2} * log2({1}/{2}) = {3}'.format(yes, no, len(data), ent))
    result = []
    for i in range(1, length):
        # print('[===]')
        unique = {}
        for row in data:
            if row[i] not in unique:
                unique[row[i]] = {'count': 1}
                if row[length] == 'Да':
                    unique[row[i]]['yes'] = 1
                    unique[row[i]]['no'] = 0
                else:
                    unique[row[i]]['no'] = 1
                    unique[row[i]]['yes'] = 0
            else:
                unique[row[i]]['count'] += 1
                if row[length] == 'Да':
                    unique[row[i]]['yes'] += 1
                else:
                    unique[row[i]]['no'] += 1
        
        # print(unique)

        print('-\n' + header[i] + ':')
        counter = 0
        for k in unique:
            print(k + ':')
            counter += 1
            e = entropy(unique[k]['yes'], unique[k]['count']) + entropy(unique[k]['no'], unique[k]['count'])
            unique[k]['entropy'] = e
            print('I(T{4}) = {0}/{2} * log2({0}/{2}) + {1}/{2} * log2({1}/{2}) = {3}'.format(unique[k]['yes'], unique[k]['no'], unique[k]['count'], e, counter))
            # print('{0} | Да: {1} | Нет {2}'.format(k, unique[k]['count'], unique[k]['yes'], unique[k]['no']))
            # print('Энтропия: {0}'.format(e))

        info = information(unique, len(data))
        g = gain(ent, info)

        inf = '\nInfo(X={0}, T) = '.format(header[i])
        for k in unique:
            inf += '{0}/{1} * {2} + '.format(unique[k]['count'], len(data), unique[k]['entropy'])
        inf = inf[:-2]
        inf += '= {0}'.format(info)
        print(inf)
        print('Gain(X={0}, T) = {1} - {2} = {3}'.format(header[i], ent, info, g))
        # print('Info: {0} | Gain: {1}'.format(info, g))

        result.append({'header': header[i], 'info': info, 'gain': g})
    return result

def removeItem(source, idx):
    del source[idx]
    return source

data = []

with open('input.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        data.append(row)
        print(', '.join(row))

header = data[0]
data = data[1:]

def calc(data, length, header, branch):
    # if len(data) == 0 or length == 0 or len(header) == 0:
    #     return
    print('<-----')
    print(' * ' + branch + '\n')
    result = find_info_and_gain(data, length, header)
    result.sort(key=lambda d: d['gain'], reverse=True)
    print('\nРезультат:')
    for r in result:
        print('{0} | {1}'.format(r['header'], r['gain']))
    print('----->\n')

    input()

    for r in result:
        idx = header.index(r['header'])
        unique = {}
        for row in data:
            unique[row[idx]] = True
        for k in unique:
            calc([remove_item(x[:], idx) for x in data if x[idx] == k], length - 1, remove_item(header[:], idx), k)

calc(data[:], len(header) - 1, header, 'Корень')

# result = find_info_and_gain(data[:], len(header) - 1, header)
# result.sort(key=lambda d: d['gain'], reverse=True)
# print('-----')
# for r in result:
#     print('{0} | {1}'.format(r['header'], r['gain']))
# print('-----')

# idx = header.index(result[0]['header'])
# unique = {}
# for row in data:
#     unique[row[idx]] = True

# for k in unique:
#     result = find_info_and_gain([remove_item(x[:], idx) for x in data if x[idx] == k], len(header) - 2, remove_item(header[:], idx))
#     result.sort(key=lambda d: d['gain'], reverse=True)
#     print('-----')
#     print(k)
#     for r in result:
#         print('{0} | {1}'.format(r['header'], r['gain']))
#     print('-----')
