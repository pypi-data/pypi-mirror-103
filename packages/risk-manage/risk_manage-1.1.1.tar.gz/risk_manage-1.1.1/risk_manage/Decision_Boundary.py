from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_text
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from risk_manage.model_data_parse import model_data_parse
from risk_manage.Data_Prepare import cluster_model

class Decision_Boundary(cluster_model, model_data_parse):
    def __init__(self, target, target_u, daypara, n_cluster):
        super().__init__(target, target_u, daypara)
        self.label = super(Decision_Boundary, self).fit(n_cluster)
        self.dic_cluster = {"Date":self.df["Date"][-len(self.diff):], "price":self.df["price"][-len(self.diff):], "cluster":self.label[-len(self.diff):]}
        self.df_cluster = pd.DataFrame(self.dic_cluster)
        self.df_cluster.insert(2, "diff", self.diff)
        self.df_cluster = self.df_cluster.dropna()

    def plot(self, depth, n_estimator, resolution, use_tree):
        global tree
        tree = DecisionTreeClassifier(criterion='entropy', max_depth=depth,random_state=3)
        forest = RandomForestClassifier(criterion="entropy", n_estimators=n_estimator, random_state=3)
        tree.fit(self.df_cluster[['price','diff']], self.df_cluster[['cluster']])
        forest.fit(self.df_cluster[['price','diff']], self.df_cluster[['cluster']])
        if use_tree:
            classifier = tree
        else: 
            classifier = forest

        X = self.df_cluster[['price','diff']].values
        y = self.df_cluster["cluster"].values

        plt.figure(figsize=(8,6))
        markers = ('s', 'x', 'o', '^', 'v')
        x1_min, x1_max = X[:,0].min()-1, X[:,0].max()+1
        x2_min, x2_max = X[:,1].min()-1, X[:,1].max()+1
        xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                                np.arange(x2_min, x2_max, resolution))
        
        Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
        Z = Z.reshape(xx1.shape)

        plt.contourf(xx1, xx2, Z, alpha=0.4, cmap="viridis")
        plt.xlim(xx1.min(), xx1.max())
        plt.ylim(xx2.min(), xx2.max())

        for idx, cl in enumerate(np.unique(y)):
            plt.scatter(x=X[y==cl,0], 
                        y=X[y==cl,1],
                        alpha=0.6, 
                        marker=markers[idx], 
                        label=cl)
            
        plt.xlabel('vix')
        plt.ylabel('diff')
        plt.title("Decision Boundaries with respect to Vix & daily Changes")
        plt.legend()

    def log(self):
        r = export_text(tree, feature_names = ["vix","diff"])  
        print(r)