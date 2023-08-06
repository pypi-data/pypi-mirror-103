from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import SelectPercentile
import sklearn.metrics as sm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import time

class AutoML():
    def __init__(self,X, y, test_size=0.3, auto=True, score_type='weighted'):
        self.X = X
        self.y = y
        self.X_train = pd.DataFrame()
        self.X_test = pd.DataFrame()
        self.y_train = pd.DataFrame()
        self.y_test = pd.DataFrame()
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.20, random_state=1)
        self.auto = auto
        self.acc = pd.DataFrame()
        self.score_type = score_type
        self.setting = str() 
        if self.score_type == 'binary':
            self.setting = 'binary'
        else:
            self.score_type = 'weighted'

        self.model = {}
        self.model['knnclf'] = KNeighborsClassifier()
        self.model['lrclf'] = LogisticRegression()
        self.model['gnbclf'] = GaussianNB()
        self.model['svcclf'] = SVC()
        self.model['sgdclf'] = SGDClassifier()
        self.model['dtclf'] = DecisionTreeClassifier()
        self.model['rfclf'] = RandomForestClassifier()

        self.cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)

        self.parameters = {}
        self.parameters['gbclf'] = {}
        self.parameters['gbclf']['n_estimators'] = [10, 100, 1000]
        self.parameters['gbclf']['learning_rate'] = [0.001, 0.01, 0.1]
        self.parameters['gbclf']['subsample'] = [0.5, 0.7, 1.0]
        self.parameters['gbclf']['max_depth'] = [3, 7, 9]
        self.parameters['gbclf']['max_features'] = ['sqrt', 'log2']

        self.parameters['rfclf'] = {}
        self.parameters['rfclf']['n_estimators'] = [10, 100, 1000]
        self.parameters['rfclf']['criterion'] = ['gini', 'entropy']
        self.parameters['rfclf']['max_features'] = ['sqrt', 'log2']

        self.parameters['svcclf'] = {}
        self.parameters['svcclf']['kernel'] = ['poly', 'rbf', 'sigmoid']
        self.parameters['svcclf']['C'] = [50, 10, 1.0, 0.1, 0.01]
        self.parameters['svcclf']['gamma'] = ['scale']

        self.parameters['knnclf'] = {}
        self.parameters['knnclf']['n_neighbors'] = range(1, 21, 2)
        self.parameters['knnclf']['weights'] = ['uniform', 'distance']
        self.parameters['knnclf']['metric'] = ['euclidean', 'manhattan', 'minkowski']

        self.parameters['lrclf'] = {}
        self.parameters['lrclf']['solver'] = ['newton-cg', 'lbfgs', 'liblinear']
        self.parameters['lrclf']['penalty'] = ['l1', 'l2', 'elasticnet']
        self.parameters['lrclf']['C'] = [100, 10, 1.1, 0.1, 0.01]

        self.parameters['sgdclf'] = {}
        self.parameters['sgdclf']['n_iter'] = [1, 5, 10]
        self.parameters['sgdclf']['alpha'] = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100]
        self.parameters['sgdclf']['penalty'] = ["none", "l1", "l2"]

        self.parameters['gnbclf'] = {}
        self.parameters['gnbclf']['var_smoothing'] = np.logspace(0,-9, num=100)

        self.parameters['dtclf'] = {}
        self.parameters['dtclf']['min_samples_split'] = range(1,10)
        self.parameters['dtclf']['min_samples_leaf'] = range(1,5)
        self.parameters['dtclf']['max_depth'] = range(1,10)
        self.parameters['dtclf']['criterion'] = ['gini', 'entropy']

# feature selection

    def variance(self):
        var_thres=VarianceThreshold(threshold=0)
        var_thres.fit(self.X_test)
        constant_columns = [column for column in self.X.columns
                    if column not in self.X.columns[var_thres.get_support()]]
        print(len(constant_columns))
        print(constant_columns)
        # for feature in constant_columns:
        #     print(feature)
        # return self.X_train.columns[var_thres.get_support()], self.X_train.drop(constant_columns,axis=1)
        return self.X_train.drop(constant_columns,axis=1,inplace=True), self.X_test.drop(constant_columns,axis=1,inplace=True)

    def correlation(self, threshold=0.5):
        col_corr = set()  # Set of all the names of correlated columns
        corr_matrix = self.X_train.corr()
        for i in range(len(corr_matrix.columns)):
            for j in range(i):
                if (corr_matrix.iloc[i, j]) > threshold: # we are interested in absolute coeff value
                    colname = corr_matrix.columns[i]  # getting the name of column
                    col_corr.add(colname)
        print('total drop columns ,',len(col_corr))
        print('We drop this columns because they highly +ve correlated \n ',col_corr)
        # self.X_train.drop(col_corr,axis=1)
        # self.X_test.drop(col_corr,axis=1)
        return self.X_train.drop(col_corr,axis=1,inplace=True), self.X_test.drop(col_corr,axis=1,inplace=True)

    def info_gain(self):
        mutual_info = mutual_info_classif(self.X_train, self.y_train)
        mutual_info = pd.Series(mutual_info)
        mutual_info.index = self.X_train.columns
        mutual_info.sort_values(ascending=False)
        inde = mutual_info[mutual_info.values > 0.005].sort_values(ascending=False).index
        return self.X_train[inde], self.X_test[inde]

    def feature_selection_all(self):
        self.variance()
        self.correlation()
        self.info_gain()
        return self.X_train, self.X_test

# train all models

    def knn(self):
        neigh = KNeighborsClassifier(n_neighbors=3)
        start = time.time()
        neigh.fit(self.X_train, self.y_train)
        end = time.time()
        print('KNN')
        y_pred = neigh.predict(self.X_test)
        
        data = {'Algorithm': 'KNN','Accuracy': sm.accuracy_score(self.y_test,y_pred), 'Precision score': sm.precision_score(self.y_test,y_pred,average=self.score_type) \
                ,'Recall score': sm.recall_score(self.y_test,y_pred,average=self.score_type), 'Precision score': sm.precision_score(self.y_test,y_pred,average=self.score_type), \
                'F1 score': sm.f1_score(self.y_test,y_pred,average=self.score_type),'time(sec)':end-start} 
        new = pd.Series(data)
        self.acc = self.acc.append(new, ignore_index=True)
        return neigh

    def logisticreg(self):
        lr_model = LogisticRegression()
        start = time.time()
        lr_model.fit(self.X_train, self.y_train)
        end = time.time()
        print('Logisitc Regression')
        y_pred = lr_model.predict(self.X_test)

        data = {'Algorithm': 'Logisitc Regression','Accuracy': sm.accuracy_score(self.y_test,y_pred), 'Precision score': sm.precision_score(self.y_test,y_pred,average=self.score_type) \
                ,'Recall score': sm.recall_score(self.y_test,y_pred,average=self.score_type), 'Precision score': sm.precision_score(self.y_test,y_pred,average=self.score_type), \
                'F1 score': sm.f1_score(self.y_test,y_pred,average=self.score_type),'time(sec)':end-start} 
        new = pd.Series(data)
        self.acc = self.acc.append(new, ignore_index=True)
        return lr_model

    def gaussiannb(self):
        gnb = GaussianNB()
        start = time.time()
        gnb.fit(self.X_train, self.y_train)
        end = time.time()
        print('Gaussian NavieBayes')
        y_pred = gnb.predict(self.X_test)

        data = {'Algorithm': 'Gaussian NavieBayes','Accuracy': sm.accuracy_score(self.y_test,y_pred), 'Precision score': sm.precision_score(self.y_test,y_pred,average=self.score_type) \
                ,'Recall score': sm.recall_score(self.y_test,y_pred,average=self.score_type), 'Precision score': sm.precision_score(self.y_test,y_pred,average=self.score_type), \
                'F1 score': sm.f1_score(self.y_test,y_pred,average=self.score_type),'time(sec)':end-start} 
        new = pd.Series(data)
        self.acc = self.acc.append(new, ignore_index=True)
        return gnb

    def decisiontree(self):
        clf_entropy = DecisionTreeClassifier()
        start = time.time()
        clf_entropy.fit(self.X_train, self.y_train)
        end = time.time()
        print('Decision Tree Classifier')
        y_pred = clf_entropy.predict(self.X_test)

        data = {'Algorithm': 'Decision Tree Classifier','Accuracy': sm.accuracy_score(self.y_test,y_pred), 'Precision score': sm.precision_score(self.y_test,y_pred,average=self.score_type) \
                ,'Recall score': sm.recall_score(self.y_test,y_pred,average=self.score_type), 'Precision score': sm.precision_score(self.y_test,y_pred,average=self.score_type), \
                'F1 score': sm.f1_score(self.y_test,y_pred,average=self.score_type),'time(sec)':end-start} 
        new = pd.Series(data)
        self.acc = self.acc.append(new, ignore_index=True)
        return clf_entropy

    def svm(self):
        svc_model = SVC()
        start = time.time()
        svc_model.fit(self.X_train, self.y_train)
        end = time.time()
        print('Support vector machine')
        y_pred = svc_model.predict(self.X_test)

        data = {'Algorithm': 'Support vector machine','Accuracy': sm.accuracy_score(self.y_test,y_pred), 'Precision score': sm.precision_score(self.y_test,y_pred,average=self.score_type) \
                ,'Recall score': sm.recall_score(self.y_test,y_pred,average=self.score_type), 'Precision score': sm.precision_score(self.y_test,y_pred,average=self.score_type), \
                'F1 score': sm.f1_score(self.y_test,y_pred,average=self.score_type),'time(sec)':end-start} 
        new = pd.Series(data)
        self.acc = self.acc.append(new, ignore_index=True)
        return svc_model

    def randomforest(self):
        Rclf = RandomForestClassifier(random_state=0)
        start = time.time()
        Rclf.fit(self.X_train, self.y_train)
        end = time.time()
        print('Random Forest Classifier')
        y_pred = Rclf.predict(self.X_test)

        data = {'Algorithm': 'Random Forest Classifier','Accuracy': sm.accuracy_score(self.y_test,y_pred), 'Precision score': sm.precision_score(self.y_test,y_pred,average=self.score_type) \
                ,'Recall score': sm.recall_score(self.y_test,y_pred,average=self.score_type), 'Precision score': sm.precision_score(self.y_test,y_pred,average=self.score_type), \
                'F1 score': sm.f1_score(self.y_test,y_pred,average=self.score_type),'time(sec)':end-start} 
        new = pd.Series(data)
        self.acc = self.acc.append(new, ignore_index=True)
        return Rclf

    def sgdclassifier(self):
        sgdclf = SGDClassifier()
        start = time.time()
        sgdclf.fit(self.X_train, self.y_train)
        end = time.time()
        print('SGD Classifier')
        y_pred = sgdclf.predict(self.X_test)

        data = {'Algorithm': 'SGD Classifier','Accuracy': sm.accuracy_score(self.y_test,y_pred), 'Precision score': sm.precision_score(self.y_test,y_pred,average=self.score_type) \
                ,'Recall score': sm.recall_score(self.y_test,y_pred,average=self.score_type), 'Precision score': sm.precision_score(self.y_test,y_pred,average=self.score_type), \
                'F1 score': sm.f1_score(self.y_test,y_pred,average=self.score_type),'time(sec)':end-start} 
        new = pd.Series(data)
        self.acc = self.acc.append(new, ignore_index=True)
        return sgdclf

    def fit(self):
        if self.auto==True:
            self.knn()
            self.logisticreg()
            self.gaussiannb()
            self.decisiontree()
            self.svm()
            self.randomforest()
            self.sgdclassifier()
        return self.acc

# hypertune

    def hypertune_grid(self,model_name):
        start = time.time()
        self.model[model_name].fit(self.X_train, self.y_train)
        end = time.time()
        model_time = end-start

        sum = 1
        for model, para in self.parameters[model_name].items():
            sum = sum * len(para)
        print('Estimate time = ',np.round((sum*model_time*3)/60,3))
        
        grid_search = GridSearchCV(estimator=self.model[model_name], param_grid=self.parameters[model_name], n_jobs=-1, cv=self.cv, scoring='accuracy',error_score=0)
        grid_result = grid_search.fit(X_train, y_train)
        print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
        return grid_result

    def hypertune_random(self,model_name, n_iter=10):
        self.n_iter = n_iter
        start = time.time()
        self.model[model_name].fit(self.X_train, self.y_train)
        end = time.time()
        model_time = end-start

        sum = 1
        for model, para in self.parameters[model_name].items():
            sum = sum * len(para)
        print('Estimate time = ',np.round((sum*model_time*3)/60,3))
        
        random_search = RandomizedSearchCV(self.model[model_name], self.parameters[model_name], n_iter=self.n_iter, scoring='accuracy', n_jobs=-1, cv=self.cv, random_state=1)
        random_result = random_search.fit(self.X_train, self.y_train)
        print("Best: %f using %s" % (random_result.best_score_, random_result.best_params_))
        return random_result