import numpy as np
from risk_manage.Data_Prepare import Data_Prepare
class model_data_parse(Data_Prepare):
  def __init__(self, target, target_u, daypara):
    super().__init__(target, target_u, daypara)
    #self.target = target
    #self.target_u = target_u
    #self.daypara = daypara
    self.df = super(model_data_parse, self).fetch(target) 
    self.diff = super(model_data_parse, self).diff_data(1)
    self.df_np = np.array(self.df["price"]).reshape(-1,1)
    #self.n = np.arange(1,8)


  def parse_fig1(self, labels, n_class):
    """
    Parse Cluster Label Index V2
    """
    index = [[] for i in range(n_class)]
    for k in range(n_class):
      temp0 = list(filter(lambda i: i[1]==k, enumerate(labels)))
      index[k] = [temp[0] for temp in temp0]
    """
    Parse Crash Index V2
    """
    temp = list(filter(lambda i: (abs(i[1])>300), enumerate(self.diff)))
    crash_date_index = [i[0] for i in temp]

    """
    Parse Exact Crash Date
    """
    crash_date_sort = [[] for _ in range(n_class)]
    for outer_i in range(n_class):
      for i in range(len(index[outer_i])):
        if self.df.index[index[outer_i]][i] in self.diff.index[crash_date_index]:
          crash_date_sort[outer_i].append(self.df.index[index[outer_i]][i])
    return index, crash_date_index, crash_date_sort