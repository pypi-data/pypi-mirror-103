import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import seaborn as sns
sns.set()
from risk_manage.model_data_parse import model_data_parse

class cluster_model(model_data_parse):
  def __init__(self, target, target_u, daypara):
    super().__init__(target, target_u, daypara)
    #self.target = target
    #self.daypara = daypara
    #self.df_np = np.array(self.df["price"]).reshape(-1,1)
    self.n = np.arange(1,8)
    self.model = [GaussianMixture(n, covariance_type='full', random_state=0).fit(self.df_np) for n in self.n]
    
  def plot_info_criteria(self):
    plt.plot(self.n, [m.bic(self.df_np) for m in self.model], label='BIC')
    plt.plot(self.n, [m.aic(self.df_np) for m in self.model], label='AIC')
    plt.legend(loc='best')
    plt.xlabel('n_clusters')

  def fit(self, n_clusters):
    #n = 3
    global n_class
    n_class = n_clusters
    gmm = GaussianMixture(n_components=n_class)
    gmm.fit(self.df_np)
    labels = gmm.predict(self.df_np)
    #self.labels = labels
    return labels

  def plot(self):

    index, crash_date_index, crash_date_sort = super(cluster_model, self).parse_fig1(self.fit(n_class),n_class)

    fig1 = plt.figure(figsize=(14,8), constrained_layout=True)
    gs = fig1.add_gridspec(3,3, width_ratios=[1,2,1])

    ax1 = fig1.add_subplot(gs[1,:-1])
    ax2 = fig1.add_subplot(gs[-1,:-1], sharex=ax1) 
    ax3 = fig1.add_subplot(gs[1:,-1])  

    ax1.plot(self.diff.index, self.diff)
    x = range(n_class)
    y = []

    for i in range(n_class):
      ax2.scatter(self.df["Date"][index[i]], self.df["price"][index[i]],cmap="inferno",marker="o", label=i)
      y.append(len(crash_date_sort[i]))

    for i in range(len(crash_date_index)):
      ax1.axvline(self.diff.index[crash_date_index][i],0,ymax=1000,c="lightblue")
      ax2.axvline(self.diff.index[crash_date_index][i],0,ymax=80,c="lightblue")

    ax1.title.set_text("Quote Change by Day of TWII")
    ax1.set_ylabel("Changes")
    ax2.title.set_text("Vix of S&P500")
    ax2.set_ylabel("Vix")

    color_set = ["red","blue","purple","grey","orange"]
    ax2.legend()
    ax3_list = ax3.bar(x,y, width=0.6)
    ax3.title.set_text("Number of Crashes happen in nth Cluster")
    ax3.locator_params(axis='x', integer=True)

    for i in range(n_class):
      ax3_list[i].set_color(color_set[i])