import numpy as np
import pandas as pd

#对一组序列文件，获取其pfm,ppm,pwm；仍需检查是否正确
def one_hot_dna(dna):
    dna_dict={'A':[1.0,0.,0.,0.],'C':[0.,1.0,0.,0.],'G':[0.,0.,1.0,0.],'T':[0.,0.,0.,1.0],'N':[0.,0.,0.,0.]}
    return np.array([dna_dict[j] for j in dna])

#获取pfm或ppm或pwm矩阵
def get_pwm(file_path,background_acgt = [0.25,0.25,0.25,0.25],type_='pfm'):
    seq_all_list = []
    #这样会漏掉最后一个！！！！！
    with open(file_path,'r')as f:
        seq_list = []
        seq_file = f.readlines()
        for i in seq_file:
            if i[0]=='>':
                seq_all_list.append(seq_list)
                seq_list=[]
            elif i[0]=='A'or i[0]=='C' or i[0]== 'G' or i[0]=='T' or i[0]=='a'or i[0]=='c'or i[0]=='g'or i[0]=='t':
                seq_list.append(i.strip())
            else:
                pass
        #最后一个>对应的不能漏了
        seq_all_list.append(seq_list)
            
    pfm_all = []
    ppm_all = []
    pwm_all = []
    for i in seq_all_list[1:]:
        one_hot_seq = []
        for j in i:
            one_hot_seq.append(one_hot_dna(j))
        
        pfm = np.sum(np.array(one_hot_seq),axis=0).T
        ppm = pfm/np.sum(pfm,axis=0)
        pwm = []
        for k in range(4):
            pwm.append(list(np.log2((ppm[k])/background_acgt[k])))
        pfm_all.append(pfm)
        ppm_all.append(ppm)
        pwm_all.append(pwm)
    if type_ == 'pfm':
        return pfm_all
    if type_ == 'ppm':
        return ppm_all
    if type_ == 'pwm':
        return pwm_all
