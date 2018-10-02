"""
A simple wrapper for linear regression.  (c) 2015 Tucker Balch
"""
import resource, sys
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)

import numpy as np
from numpy import corrcoef
import math
class DTLearner():

    def __init__(self,leaf_size=1, verbose = False):
        #pass # move along, these aren't the drones you're looking for
        self.leaf_size=leaf_size
        self.tree=[]
        self.leaf=-1
        self.NA=-1

    def author(self):
        return 'cwu392' # replace tb34 with your Georgia Tech username

    def addEvidence(self,trainX,trainY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """

        # slap on 1s column so linear regression finds a constant term
        newdataX = np.array(trainX)
        print "Input TrainX.shape[0]"+str(trainX.shape[0])
        newdataY = np.array(trainY)
        print "Input TrainY.shape[0]"+str(trainY.shape[0])
        data=np.column_stack([trainX,trainY])
        #data=np.hstack((newdataX,newdataY))
        tree=self.build_tree(data,self.leaf_size)
        self.tree=tree

    def build_tree(self, data,leaf_size=1):
        max_cof=0
        i_key=-1
        dataX=data[:,0:-1]
        dataY=data[:,-1]
        if dataX.shape[0]<=self.leaf_size:
            return np.array([[self.leaf,dataY.mean(),self.NA,self.NA]])
        else:
            #Determine best feature i to split on# i_key,cof_key
            for i in range(0,len(dataX[0,:])): #Ignore date#
                cof=(np.corrcoef(dataX[:,i],dataY)[1,0])
                if abs(cof)>abs(max_cof):
                    i_key=int(i);
                    cof_key=abs(cof)
            SplitVal=np.median(dataX[:,i_key])
            left_data=data[data[:,i_key]<=SplitVal]
            right_data=data[data[:,i_key]>SplitVal]
            if right_data.shape[0]==0:
                return np.array([[self.leaf,dataY.mean(),self.NA,self.NA]])
            lefttree=self.build_tree(left_data)
            righttree=self.build_tree(right_data)
            root=np.array([[i_key,SplitVal,1,lefttree.shape[0]+1]])
            root=np.concatenate((root,lefttree,righttree))
            return root

    def query(self,points):
        result=[]
        #print "Tree:"+str(self.tree)
        #print "Points"+str(points)
        for point in points:
            i=0
            while True:
                key=int(self.tree[i][0])
                if self.tree[i][0]!=self.leaf:
                    if point[key]<=self.tree[i][1]:
                        i+=int(self.tree[i][2])
                    elif point[key]>self.tree[i][1]:
                        i+=int(self.tree[i][3])
                else:
                    result.append(self.tree[i][1])
                    break
        return np.array(result)


# if __name__=="__main__":
#     #print "the secret clue is 'zzyzx'"
#     import pandas as pd
#     import matplotlib.pyplot as plt
#     data=pd.DataFrame()
#     data=pd.read_csv('/home/chiamin/GaTech/ml4t/ML4T_2017Fall-master/assess_learners/Data/Istanbul_NEW.csv')
#     data=np.array(data)
#     #np.random.shuffle(data)
#     train_rows = int(0.6* data.shape[0])
#     test_rows = data.shape[0] - train_rows

#     trainX = data[:train_rows,0:-1]
#     trainY = data[:train_rows,-1]
#     testX = data[train_rows:,0:-1]
#     testY = data[train_rows:,-1]
#     # separate out training and testing data
#     import DTLearner as dt
#     # learner = dt.DTLearner(leaf_size = 1, verbose = False) # constructor
#     # learner.addEvidence(trainX, trainY) # training step
#     # predY1 = learner.query(testX) # query
#     # rmse1 = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
    
#     dt_test_rmses = []
#     dt_train_rmses=[]
#     # rt_test_rmses = []
#     for leaf_size in range(1, 31):
#         dt_learner = dt.DTLearner(leaf_size=leaf_size)
#         # rt_learner = rt.RTLearner(leaf_size=leaf_size)
    
#         dt_learner.addEvidence(trainX, trainY)
#         # rt_learner.addEvidence(trainX, trainY)
        
#         predY = dt_learner.query(testX)
#         rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
#         dt_test_rmses.append(rmse)
#         trainY_a = dt_learner.query(trainX)
#         rmse_t = math.sqrt(((trainY - trainY_a) ** 2).sum()/testY.shape[0])
#         dt_train_rmses.append(rmse_t)
#         # predY = rt_learner.query(testX)
#         # rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
#         # rt_test_rmses.append(rmse)
#     fig = plt.figure()
#     dt_test, = plt.plot(dt_test_rmses, label='DTLearner testing')
#     dt_train, = plt.plot(dt_train_rmses, label='DTLearner training')
#     # rt_test, = plt.plot(rt_test_rmses, label='RTLearner testing')
#     plt.xticks(range(30), range(1, 31))
#     plt.xlabel('leaf size')
#     plt.ylabel('RMSE')
#     #plt.legend(handles=[dt_test, rt_test])
#     plt.legend(handles=[dt_test,dt_train])
#     plt.show()
#     #fig.savefig(sys.argv[1].split('/')[1].split('.')[0] + '_' +'dt_rt_compare_no_bag.png')
