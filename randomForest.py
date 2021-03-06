import numpy as np
def hasMultipleTargetClasses(data):
    """Computes if the dataset is unpure"""
    # Count the amount of unique target classes that are left in this node/leaf
    # If more than one, the node is still unpure (and would require another split if possible)
    return len(np.unique(data[:,-1])) > 1
def majorityVote(array):
    return np.argmax(np.bincount(array.astype(int)))
def trainRandomForest(traindata, Ntrees, bootstrapsize):
    """Creates a random forest model from the data"""

    # traindata: A matrix of all the data (NxK)
    # Ntrees: the number of trees that make up the forest

    model = [0]*Ntrees #a list of all trees

    for n in range(Ntrees):
        # TODO: This is not bootstrapping right? just a random shuffle of the data and taking the first x elements
        #bootstrap data
        N = traindata.shape[0];
        Nbootstrap = np.floor(bootstrapsize * N);
        
        np.random.shuffle(traindata);
        
        bootStrapData = traindata[0:Nbootstrap,:];
        
        bootStrapData = traindata;
        #set some number of features
        #set some max depth
        tree = trainDecisionTree(bootStrapData) #train
        model[n] = tree
    
    return model

def trainDecisionTree(data, depth=0, tree = [], max_depth = None):
    """Returns the decision tree for some data"""
    #find optimal split
    if max_depth == None:
        max_depth = data.shape[1]

    majority = majorityVote(data[:,-1])

    if depth <= max_depth and hasMultipleTargetClasses(data):
        d = depth
        splitFeature, splitValue = decisionStump(data)
        
        lower = data[data[:,splitFeature]<=splitValue]
        upper = data[data[:,splitFeature]>splitValue]
        
        tree_lower = trainDecisionTree(lower, depth=d+1, tree = tree, max_depth=max_depth)
        tree_upper = trainDecisionTree(upper, depth=d+1, tree = tree, max_depth=max_depth)


        tree = (splitFeature,splitValue,majority,tree_lower,tree_upper)
    else:
        tree = (None,None,majority,None,None)
        #see if child nodes are "pure"
        #for all not pure and depth<max repeat
    
    return tree
def makeRandomForestPrediction(data_point, model):
    predictions = []
    for tree in model:
        predictions.append(makeDecisionTreePrediction(data_point,tree))
    return majorityVote(np.array(predictions))

def makeDecisionTreePrediction(data_point, tree):
    """Makes a prediction with a DT on one datapoint"""
    (splitFeature,splitValue,majority,tree_lower,tree_upper) = tree

    # If this is a leaf, return majority vote
    if splitFeature is None:
        return majority
    # Else, split on split feature and recursively keep going until leaf node
    else:
        if data_point[splitFeature]<=splitValue:
            return makeDecisionTreePrediction(data_point, tree_lower)
        else:
            return makeDecisionTreePrediction(data_point, tree_upper)

def decisionStump(data):
    """Returns the optimal attribute and value for a tree to split on given
    some data matrix"""
    
    #find atrribute and value where entropy of upper and lower are smallest
    entropy = np.inf;
    #for all attrbutes:
    K = data.shape[1];
    for k_temp in range(K-1):
        #sort on values of that attribute
        sort = data[data[:,k_temp].argsort()]
        #for all values
        for value_temp in np.unique(sort[:,k_temp]):
            #calculate entropy of this split (add upper and lower)
            lower = data[data[:,k_temp]<=value_temp]
            upper = data[data[:,k_temp]>value_temp]
            entropylower = calculateEntropy(lower);
            entropyupper = calculateEntropy(upper);
            #if entropy is smaller
            new_entropy = (len(lower)/len(data))*entropylower + (len(upper)/len(data))*entropyupper
            if new_entropy < entropy:
                entropy = new_entropy
                k = k_temp;
                value = value_temp;
                #save this attribute value pair as new optimal
    
    #random split
    #K = data.shape[1]
    #k = np.random.randint(K-1);
    #value = np.mean(data[:,k]);
    return k, value
    
def calculateEntropy(data):
    if len(np.unique(data[:,-1])) <= 1:
        H = 0;
    else:
        histogram,_ = np.histogram(data[:,-1],len(np.unique(data[:,-1])));
        histogram = histogram[histogram != 0]
        H = 0;
        prob = np.double(histogram)/sum(np.double(histogram));
        for p in prob:
            H += -p*np.log2(p);
    return H


# data = np.random.randint(5,size=(20,5))
#
# tree = trainDecisionTree(data)
