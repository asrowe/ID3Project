import math


def entropy(aClass):
    trace = False

    classcount = {}
    for c in aClass:
            if c in classcount:
                classcount[c] = classcount[c] + 1
            else:
                classcount[c] = 1.0
    if trace :
        print "Class values: " + str(classcount)

    classprob = {k : v/len(aClass) for k, v in classcount.iteritems()}
    temp = map(lambda x: -1 * x * math.log(x,2), classprob.itervalues())

    if trace:
        print "Class Probabilites: " + str(classprob)
        print "Class entropies" + str(temp)

    
    _entropy = reduce(lambda x, y: x+y, temp)

    if trace:
        print "Entropy: " + str(_entropy)

    return _entropy


def gain(data, class_idx, cv_idx): #cv  is covariate
    trace = False
    
    covars = set([x[cv_idx] for x in data])

    if trace:
        print covars

    subsets = {}
    for cv in covars:
        
        subset = []
        for i in range(len(data)):
            if (data[i][cv_idx] == cv):
                subset.append(data[i][class_idx])
        subsets[cv] = subset

    if trace:
        print subsets
        print {k : entropy(v) for k, v in subsets.iteritems()}

    weighted_entropys = {k : float(len(v))/float(len(data))* entropy(v) for k, v in subsets.iteritems()}

    if trace:
        print weighted_entropys

    _gain = entropy([x[class_idx] for x in data]) - reduce(lambda x, y: x+y, weighted_entropys.itervalues())
    
    return _gain

def getMax(gains):
    max_v = 0
    max_h = ""
    
    for k, v in gains.iteritems():
        if v > max_v:
            max_h = k
            max_v = v

    return max_h
        



def id3Learn(headings, data, class_name): # learns a decision tree based on the ID3 algorithm
    class_idx = headings.index(class_name)
    print "Index of " + class_name + " is " + str(class_idx)
    aClass = [x[class_idx] for x in data]

    predictors = []
    for i in range(len(headings)):
        if i != class_idx:
            predictors.append(i)

    infoGain = {headings[i] : gain(data,class_idx, i) for i in predictors}
        
    print "Gain: " + str(infoGain)
    node =  getMax(infoGain)

    if node == "":# pure population
        return None
    else:
        node_idx = headings.index(node)
        node_options = set([x[node_idx] for x in data])
        print node_options
        return (node, node_options)

def cutData(headings, data, cut_attribute, cut_value):
    cut_idx = headings.index(cut_attribute)
    filtered_dataset = []
    for row in data:
        if row[cut_idx] == cut_value:
            filtered_dataset.append(row)
    return filtered_dataset

def recurseID3(headings, data, class_name, tree):
    node, node_options = id3Learn(headings, data, class_name)
    tree.append(node)
    if node_options != None:
        for o in node_options:
            part_data = cutData(headings, data, node, o)
            recurseID3(headings, part_data, class_name, tree)
    return tree

    


# main script
# open  and read ball file

f = open('C:/Users/arowe4/Dropbox/data/ball.txt', 'r')
ball = f.readlines()

isFirst = True
headings = []
records = []

for day in ball:
    values = day.split('\t')[0:7]
    values = [i.strip("\n") for i in values]

    if isFirst:
        headings = values
        isFirst = False
    else:
        records.append(values)

print "Headings: " + str(headings)
print "Sample record: " + str(records[0])

#dtree = id3Learn((headings, records, "Play ball")
#print dtree

print recurseID3(headings, records, "Play ball", [])
