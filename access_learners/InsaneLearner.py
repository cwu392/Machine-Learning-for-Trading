import LinRegLearner as lrl
import BagLearner as bl
import numpy as np
class InsaneLearner(bl.BagLearner):
    def __init__(self, verbose = False):
        #pass # move along, these aren't the drones you're looking for
        self.learners=[bl.BagLearner(learner=lrl.LinRegLearner, bags=20) for i in range(20)]
        self.bags=20
        #for i in range(self.bags):
        # 	self.learners.append({learner:lrl.LinRegLearner})

    # def author(self):
    #     return 'cwu392' # replace tb34 with your Georgia Tech username

    # def addEvidence(self,trainX,trainY):
    # 	for learner in self.learners:
    # 		index = np.random.randint(trainX.shape[0], size=trainX.shape[0])
    # 		learner.addEvidence(trainX[index],trainY[index])

    # def query(self,points):
    #     output=0
    #     for learner in self.learners:
    #     	output=learner.query(points)
    #     return output/self.bags

# if __name__=="__main__":
#     #print "the secret clue is 'zzyzx'"
#     import pandas as pd
#     data=pd.DataFrame()
#     data=pd.read_csv('/home/chiamin/GaTech/ml4t/ML4T_2017Fall-master/assess_learners/Data/simple.csv')

#     #np.random.shuffle(data)
#     train_rows = int(0.6* data.shape[0])
#     test_rows = data.shape[0] - train_rows

#     trainX = data.ix[:train_rows,0:-1]
#     trainY = data.ix[:train_rows,-1]
#     testX = data.ix[train_rows:,0:-1]
#     testY = data.ix[train_rows:,-1]

#     # separate out training and testing data
#     import InsaneLearner as il
#     learner = il.InsaneLearner(verbose = False) # constructor
#     learner.addEvidence(trainX, trainY) # training step
#     predY = learner.query(testX) # query