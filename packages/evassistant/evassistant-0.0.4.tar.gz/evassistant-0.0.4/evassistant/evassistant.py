# %%
import numpy as np
class logistic:
    def __init__(self,ls_or,ls_xvar,intercept):
        self.ls_or=ls_or
        self.ls_xvar=ls_xvar
        self.intercept=intercept
    def prob(self):
        ls_beta=[np.log(x) for x in self.ls_or]
        ls_weight=[a*b for a,b in zip(ls_beta,self.ls_xvar)]
        z=sum(ls_weight)+self.intercept
        q=1+np.exp(-z)
        prob=1/q
        return prob
    def pi(self):
        ls_beta=[np.log(x) for x in self.ls_or]
        ls_weight=[a*b for a,b in zip(ls_beta,self.ls_xvar)]
        pi=sum(ls_weight)
        return pi
    @staticmethod
    def intercept(prob,ls_xvar,ls_or):
        ls_beta=[np.log(x) for x in ls_or]
        ls_weight=[a*b for a,b in zip(ls_beta,ls_xvar)]
        var2=np.subtract(np.divide(1,prob),1)
        intercept = -np.log(var2)-sum(ls_weight)
        return intercept
    @staticmethod
    def score(ls_right_value,ls_left_value,ls_or,ls_xvar):#提供列线图右边的数值和左边的数值,分类变量为1和0,多分类变量为多个1和0
        ls_beta=[np.log(x) for x in ls_or]
        ls_beta_abs=[np.abs(x) for x in ls_beta]
        ls_distance_abs=[np.abs(a-b) for a,b in zip(ls_right_value,ls_left_value)]# 各自标尺的右边数值与左边数值的差
        ls_pi_pre=[a*b for a,b in zip(ls_beta_abs,ls_distance_abs)]
        ls_max_score=[]#求各个变量最大的得分
        for pi_pre in ls_pi_pre:        
            max_score=np.divide(pi_pre,np.max(ls_pi_pre))*100
            ls_max_score.append(max_score)
        ls_unit_score=[a/b for a,b in zip(ls_max_score,ls_distance_abs)]#求各个变量每个刻度单位的得分
        ls_actual_distance=[a-b for a,b in zip(ls_xvar, ls_left_value)]#求实际的总得分
        ls_actual_distance_abs=map(np.abs,ls_actual_distance)
        ls_score=[a*b for a,b in zip(ls_unit_score,ls_actual_distance_abs)]
        total_score=0
        for i,val in enumerate(ls_score):
            total_score +=ls_score[i]
        return ls_score,total_score
class cox:
    def __init__(self,ls_hr,ls_xvar,basic_rate):
        self.ls_hr=ls_hr
        self.ls_xvar=ls_xvar
        self.basic_rate=basic_rate
    def survival_rate(self):
        ls_beta=[np.log(x) for x in self.ls_hr]
        ls_weight=[a*b for a,b in zip(ls_beta,self.ls_xvar)]
        pi=sum(ls_weight)
        survival_rate=self.basic_rate**np.exp(pi)
        return survival_rate
    def pi(self):
        ls_beta=[np.log(x) for x in self.ls_hr]
        ls_weight=[a*b for a,b in zip(ls_beta,self.ls_xvar)]
        pi=sum(ls_weight)
        return pi
    @staticmethod
    def basic_rate_estimate(survival_rate,ls_xvar,ls_hr):
        ls_beta=[np.log(x) for x in self.ls_hr]
        ls_weight=[a*b for a,b in zip(ls_beta,ls_xvar)]
        var=np.exp(sum(ls_weight))    
        basic_rate=pow(survival_rate,1.0/var)
        return basic_rate 
#%%
if __name__=="__main__":
    # basic_rate = 0.73710233
    # ls_hr = [1.2,1.5,1.00005,1.7,2.1]
    # ls_xvar = [1,2,3,4,5]
    # model=cox(ls_hr,ls_xvar,basic_rate)
    # print(model.survival_rate())
    ls_or=[1.26579,2.50828,0.94866]
    a,b=logistic.score(ls_right_value=[10,1,10],ls_left_value=[1,0,75],ls_or=ls_or,ls_xvar=[5,1,40])
    print(b)
# %%

