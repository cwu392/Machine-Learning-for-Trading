import numpy as np
from collections import Counter
class BagLearner():
    def __init__(self, learner, kwargs = {}, bags = 20, boost = False, verbose = False):
        #pass # move along, these aren't the drones you're looking for
        self.learners=[]
        self.bags=bags
        for i in range(self.bags):
        	self.learners.append(learner(**kwargs))
        self.boost=boost
        self.verbose=verbose

    def author(self):
        return 'cwu392' # replace tb34 with your Georgia Tech username

    def addEvidence(self,trainX,trainY):
    	for learner in self.learners:
    		index = np.random.randint(trainX.shape[0], size=trainX.shape[0])
    		learner.addEvidence(trainX[index],trainY[index])

    def query(self,points):
        res=[]
        for learner in self.learners:
        	res.append(learner.query(points))
            
        res = np.transpose(res)
        ret = [max(Counter(x).iteritems(), key = lambda x : x[1])[0] for x in res]
        return np.array(ret)

if __name__=="__main__":

    import pandas as pd
    import matplotlib.pyplot as plt
    import BagLearner as bl
    import QLearner as ql
    import math
    dt_test_rmses = []
    bag_test_rmses = []
    bag_train_rmses = []
    data=pd.DataFrame()
    data=pd.read_csv('/home/chiamin/GaTech/ml4t/ML4T_2017Fall-master/assess_learners/Data/Istanbul_NEW.csv')
    data=np.array(data)
    #np.random.shuffle(data)
    train_rows = int(0.6* data.shape[0])
    test_rows = data.shape[0] - train_rows

    trainX = data[:train_rows,0:-1]
    trainY = data[:train_rows,-1]
    testX = data[train_rows:,0:-1]
    testY = data[train_rows:,-1]

    for bag in [3, 10, 20, 40]:
        bag_test_rmses = []
        bag_train_rmses = []
        for leaf_size in range(1, 31,1):

            bag_learner = bl.BagLearner(learner=ql.QLearner, bags=bag, kwargs={"num_states":100, "num_actions":4, "alpha": 0.2,"gamma": 0.9,"rar": 0.5, "radr": 0.99,"dyna": 1,"verbose": False})
            bag_learner.addEvidence(trainX, trainY)

            # bag test
            predY = bag_learner.query(testX)
            rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
            bag_test_rmses.append(rmse)

            # bag train
            predY = bag_learner.query(trainX)
            rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
            bag_train_rmses.append(rmse)

        fig = plt.figure()
        plt.xticks(range(30), range(1, 31))
        plt.xlabel('leaf size')
        plt.ylabel('RMSE')
        bag_train, = plt.plot(bag_train_rmses, label=str(bag) + ' bag training')
        bag_test, = plt.plot(bag_test_rmses, label=str(bag) + ' bag testing')
        dt_test, = plt.plot(dt_test_rmses, label='DT testing')
        plt.legend(handles=[bag_train, bag_test, dt_test])
        plt.show()

    #bag_learner = bl.BagLearner(learner=lrl.LinRegLearner, bags=5)
    # for bag in [3, 5,10]:
    #     for leaf_size in range(1, 31):
    #         bag_learner = bl.BagLearner(learner=dt.DTLearner, bags=bag, kwargs={"leaf_size":leaf_size})
    #         bag_learner.addEvidence(trainX, trainY)

    #         # bag test
    #         predY = bag_learner.query(testX)
    #         rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
    #         bag_test_rmses.append(rmse)
    #         #fig = plt.figure()
    #     fig = plt.figure()
    #     #plt.xticks(range(30), range(1, 31))
    #     plt.xlabel('leaf size')
    #     plt.ylabel('RMSE')
    #     bag_train, = plt.plot(bag_train_rmses, label=str(bag) + ' bag training')
    #     bag_test, = plt.plot(bag_test_rmses, label=str(bag) + ' bag testing')
    #     dt_test, = plt.plot(dt_test_rmses, label='DT testing')
    #     plt.legend(handles=[bag_train, bag_test, dt_test])
    #     plt.show()

    # bag_test, = plt.plot(bag_test_rmses, label='BagLearner testing')
    # # rt_test, = plt.plot(rt_test_rmses, label='RTLearner testing')
    # plt.xticks(range(30), range(1, 31))
    # plt.xlabel('leaf size')
    # plt.ylabel('RMSE')
    # #plt.legend(handles=[dt_test, rt_test])
    # plt.legend(handles=[bag_test])
    # plt.show()


        # fig = plt.figure()
        # plt.xticks(range(30), range(1, 31))
        # plt.xlabel('leaf size')
        # plt.ylabel('RMSE')
        # bag_train, = plt.plot(bag_train_rmses, label=str(bag) + ' bag training')
        # bag_test, = plt.plot(bag_test_rmses, label=str(bag) + ' bag testing')
        # dt_test, = plt.plot(dt_test_rmses, label='DT testing')
        # plt.legend(handles=[bag_train, bag_test, dt_test])
        # plt.show()