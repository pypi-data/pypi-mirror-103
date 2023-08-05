# od - Original data,sd - shuffle data, iv - independent varaible, dwiv - data without iv, ldwiv list of dwiv, cd - combined data.
# "C:\\Users\\prav\\PycharmProjects\\SVM\\SVM\\Iris.csv"

import pandas as pd
import random
import numpy as np
class linearclassifier():
    def linearreg(a,b,drop,independent):
        od = pd.read_csv(a)


        for i in drop:

            od = od.drop([i],axis=1)

        sd = od.sample(frac=1)

        Y = []
        iv = sd[independent]

        for val in iv:
            if (val == 'Iris-setosa'):
                Y.append(0)
            else:
                Y.append(1)


        dwiv = sd.drop([independent],axis=1)
        ldwiv = dwiv.values.tolist()

        X=ldwiv

        x_train = []
        y_train = []
        x_test = []
        y_test = []

        sep =int(b*(len(X)))
        rem= int(len(X)-sep)
        x_train = X[0:sep]
        x_test= X[sep:]
        y_train = Y[0:sep]
        y_test= Y[sep:]

        x_train = np.array(x_train)
        y_train = np.array(y_train)
        x_test = np.array(x_test)
        y_test = np.array(y_test)

        xs={}
        for i in range(len(od.columns)-1):
            xs["x_"+ str(i+1)]=x_train[:,i]
        for i in range(len(od.columns)-1):
            xs["x_"+ str(i+1)]=np.array(xs["x_"+ str(i+1)])
        for i in range(len(od.columns)-1):
            xs["x_"+ str(i+1)]=xs["x_"+ str(i+1)].reshape(sep, 1)



        y_train = y_train.reshape(sep,1)


        def sigmoid(x):
            return (1 / (1 + np.exp(-x)))


        m = sep
        alpha = 0.0001
        th={}
        for i in range(len(od.columns)):
            th["theta_"+ str(i)]=np.zeros((m, 1))
        print (th.keys())



        epochs = 0
        cost_func = []


        while (epochs < 10000):
            y = 0
            y += th["theta_0"]
            for i in range (len(od.columns)-1):
                y+=th["theta_"+str(i+1)]*xs["x_"+str(i+1)]
            y=y.reshape(sep,1)


            y = sigmoid(y)


            cost = (- np.dot(np.transpose(y_train), np.log(y)) - np.dot(np.transpose(1 - y_train), np.log(1 - y))) / m


            thg={}
            thg["thetag_0"] = np.dot(np.ones((1, m)), y - y_train) / m
            for i in range(len(od.columns)-1):
                thg["thetag_"+str(i+1)] = np.dot(np.transpose(xs["x_"+str(i+1)]), y - y_train) / m
            for i in range(len(od.columns)):
                th["theta_" + str(i)] = th["theta_" + str(i)]- alpha*thg["thetag_"+str(i)]



            cost_func.append(cost)
            epochs += 1


        from sklearn.metrics import accuracy_score
        test={}
        for i in range(len(od.columns)-1):
            test["test_"+str(i+1)]=x_test[:, i]


        for i in range(len(od.columns)-1):
            test["test_" + str(i+1)] = np.array(test["test_"+str(i+1)])
        for i in range(len(od.columns)-1):
            test["test_" + str(i+1)] = test["test_"+str(i+1)].reshape(rem, 1)




        index = list(range(rem, sep))
        for i in range(len(od.columns)):
            th["theta_"+ str(i)]=np.delete(th["theta_"+str(i)], index)
        for i in range(len(od.columns)):
            th["theta_"+ str(i)]=th["theta_"+str(i)].reshape(rem, 1)


        print (th.keys())

        y_pred = 0
        y_pred += th["theta_0"]
        for i in range (len(od.columns)-1):
            y_pred+=th["theta_"+str(i+1)]*test["test_"+str(i+1)]

        y_pred = sigmoid(y_pred)


        new_y_pred = []
        for val in y_pred:
            if (val >= 0.5):
                new_y_pred.append(1)
            else:
                new_y_pred.append(0)


        print(accuracy_score(y_test, new_y_pred))

