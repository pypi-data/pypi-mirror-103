import time #内置模块
import pysam
import pyBigWig
import numpy as np
import pandas as pd
from pysam import FastaFile
from scipy.ndimage import gaussian_filter1d


#辅助函数，用于one-hot编码
#用此函数对100万条1000长度的序列编码需要约700秒（GPU02节点）
def one_hot_dna(dna):
    dna_dict={'A':[1.0,0.,0.,0.],'C':[0.,1.0,0.,0.],'G':[0.,0.,1.0,0.],'T':[0.,0.,0.,1.0],'N':[0.,0.,0.,0.]}
    return np.array([dna_dict[k] for k in dna])


#辅助函数，控制获得固定长度开放区序列
def get_new_bed_df(bed_df , seq_len):
    
    diff = np.array(bed_df.end - bed_df.start)-seq_len
    
    new_start_list = list(np.rint(np.array(bed_df.start) + np.floor(diff*0.5)))
    new_end_list = list(np.rint(np.array(bed_df.end) - np.ceil(diff*0.5)))
    
    #到此处为止，未破坏bed文件原始结构
    new_bed3_df = pd.DataFrame({ 'chr':bed_df.chr,'start':new_start_list,'end':new_end_list})
    
    new_bed3_df.start = new_bed3_df.start.astype(int)
    new_bed3_df.end = new_bed3_df.end.astype(int)
    return new_bed3_df


def get_new_bed4_df(bed_df , seq_len):
    
    diff = np.array(bed_df.end - bed_df.start)-seq_len
    
    new_start_list = list(np.rint(np.array(bed_df.start) + np.floor(diff*0.5)))
    new_end_list = list(np.rint(np.array(bed_df.end) - np.ceil(diff*0.5)))
    
    #到此处为止，未破坏bed文件原始结构
    new_bed3_df = pd.DataFrame({ 'chr':bed_df.chr,'start':new_start_list,'end':new_end_list,'classes':bed_df.classes})
    
    new_bed3_df.start = new_bed3_df.start.astype(int)
    new_bed3_df.end = new_bed3_df.end.astype(int)
    return new_bed3_df



#根据控制文件（记录染色体号和长度，tab间隔）过滤样本
def sample_control(bed_df,genome_control_df):
    #Python内置函数locals()，返回记录当前所有局部变量的字典
    #此处用于局部变量的动态创建
    ld = locals() 
    for i in range(len(genome_control_df)):
        bed_chr_ = bed_df[bed_df.chr == genome_control_df.iloc[i,0]]
        bed_chr =  bed_chr_[bed_chr_.end<genome_control_df.iloc[i,1]]
        ld['sample_' + str(genome_control_df.iloc[i,0])] =bed_chr[bed_chr.start>0]
        
    bed_df_all = []
    for j in genome_control_df.chr:
        bed_df_all.append(ld['sample_' + j])
    bed_df_control = pd.concat(bed_df_all,axis=0)
    print(len(bed_df)-len(bed_df_control),'个样本被筛除，因为它们不在control文件中或超越了control文件中规定的界限')
    return bed_df_control


#这里的第二个参数可以给bed_df而非bed原始文件，即只作为辅助函数，不独立
#约91秒可以完成10万1024长度序列的onehot编码并返回
def get_one_hot_seq_list(fasta_path,sample_bed_df):
    print('对',str(len(sample_bed_df)),'条序列进行one-hot编码')
    start_time = time.time()
    fasta_file = pysam.FastaFile( fasta_path) #打开fasta文件,需要对应目录下有fasta文件的fai索引
    seq=[]
    for index,data in sample_bed_df.iterrows():
        seq.append(one_hot_dna(fasta_file.fetch(data.chr,data.start,data.end) ))
    end_time = time.time()
    print('序列one-hot编码完成,该步骤累计耗时：',end_time-start_time,'秒')
    return seq


def get_regression(bw_path,sample_bed_df):
    print('对',str(len(sample_bed_df)),'个样本进行信息提取')
    start_time = time.time()
    bw_file = pyBigWig.open(bw_path)
    bw_regression = []
    for index,data in sample_bed_df.iterrows():
        #bw.stats在范围内取均值
        bw_regression.append(bw_file.stats(str(data.chr),int(data.start),int(data.end))[0])
    bw_file.close()
    end_time = time.time()
    print('信息提取完成,该步骤累计耗时：',end_time-start_time,'秒')
    return bw_regression  

def get_base_regression(bw_path,sample_bed_df):
    print('对',str(len(sample_bed_df)),'个样本进行碱基分辨率信息提取')
    start_time = time.time()
    bw_file = pyBigWig.open(bw_path)
    bw_base_regression = []
    for index,data in sample_bed_df.iterrows():
        #bw.values取范围内每个点的值
        bw_base_regression.append(bw_file.values(str(data.chr),int(data.start),int(data.end)))
    bw_file.close()
    end_time = time.time()
    print('信息提取完成,该步骤累计耗时：',end_time-start_time,'秒')
    return bw_base_regression 

#获取反向互补序列，用于数据增强
def DNA_complement(sequence):
    trantab = str.maketrans('ACGTacgt', 'TGCAtgca')     #翻译表
    com_sequence = sequence[::-1].translate(trantab)     # 反向、转换互补
    return com_sequence

#获取序列而不是one-hot的序列
def get_seq_list(fasta_path,sample_bed_df):
    fasta_file = pysam.FastaFile( fasta_path) #打开fasta文件,需要对应目录下有fasta文件的fai索引
    seq_=[]
    for index,data in sample_bed_df.iterrows():
        seq_.append(fasta_file.fetch(data.chr,data.start,data.end))
    return seq_


#为了针对分类问题，应该给定bed第四列作为类别标签！
def genome_dataset(bed_path,fasta_path,seq_len=1024,genome_size_control=None,dataset_type='regression',bw_path=None,Data_Augmentation=False):
    #注意匹配，chr01或chr1，有没有0，大小写，和fasta、bw文件比较
    
    #注意容错机制：文件头有无均可读(待实现)
    with open(bed_path,'r')as f:
        #第一行第一个数据单位（应该是chrom或者chrxx）
        chek_bed = f.readline().strip().split('\t')[0]
        if chek_bed[:3]!='chr' and chek_bed[:3]!='CHR' and chek_bed[:3]!='Chr':
            raise IOError("bed文件格式不合规范，请检查！\n 注：各列需以tab间隔，无文件头")
        else:
            print('bed文件检查通过')
        
    if dataset_type=='regression' or dataset_type=='base_regression':
        bed_df = pd.read_csv(bed_path,sep='\t',header=None).iloc[:,:3]
        bed_df.columns = ['chr','start','end']
        #得到定长的bed文件
        new_bed_df = get_new_bed_df(bed_df,seq_len)
    elif dataset_type=='classification':
        bed_df = pd.read_csv(bed_path,sep='\t',header=None).iloc[:,:4]
        bed_df.columns = ['chr','start','end','classes']
        new_bed_df = get_new_bed4_df(bed_df,seq_len)
    else:
        raise Exception("请选择正确的模式")
        
        
    
    #样本控制
    if genome_size_control!=None:
        print('使用控制文件，将过滤长度不合文件要求的序列和未在文件中出现的染色体对应的序列')
        genome_control = pd.read_csv(genome_size_control,sep='\t',names=['chr','control'])
        control_bed_df = sample_control(new_bed_df,genome_control)
    else:
        control_bed_df = new_bed_df
        print('您选择不使用控制文件')
    
  
    #获取原始序列的one-hot编码结果
    seq = get_one_hot_seq_list(fasta_path,control_bed_df)

    sample_name = []
    #获取sample_name，原始
    for k in range(len(control_bed_df)):
        sample_name.append(str(control_bed_df.iloc[k,0])+','+str(control_bed_df.iloc[k,1])+','+str(control_bed_df.iloc[k,2]))
        
    if dataset_type=='classification':
        if Data_Augmentation:
            print('通过取反向互补序列进行数据增强,经此步骤，您最终得到的样本量将翻倍')
            seq_ = get_seq_list(fasta_path,control_bed_df)
            reverse_com_seq = list(map(DNA_complement , seq_))
            #reverse_com_seq要在此处进行one-hot编码
            seq_all = seq+list(map(one_hot_dna,reverse_com_seq))
            m_sample_name = []
            for k in range(len(control_bed_df)):
                m_sample_name.append(str(control_bed_df.iloc[k,0])+','+str(control_bed_df.iloc[k,1])+','+str(control_bed_df.iloc[k,2])+','+'Reverse_complementation')
            sample_name_all = sample_name+m_sample_name
            classes_all = list(control_bed_df.classes)+list(control_bed_df.classes)
            dataset_df = pd.DataFrame({'sample':sample_name_all,'seq_one_hot':seq_all,'classes':classes_all})
            return dataset_df
                 
        else:
            print('您选择不使用数据增强')
            dataset_df = pd.DataFrame({'sample':sample_name,'seq_one_hot':seq,'classes':list(control_bed_df.classes)})
            return dataset_df
    
    if dataset_type=='regression':
        if Data_Augmentation:
            print('通过取反向互补序列进行数据增强,经此步骤，您最终得到的样本量将翻倍')
            #map返回迭代器，需要list转换
            #返回反向互补序列
            #这里错了，放进来的不能是seq
            seq_ = get_seq_list(fasta_path,control_bed_df)
            reverse_com_seq = list(map(DNA_complement , seq_))
            #reverse_com_seq要在此处进行one-hot编码
            seq_all = seq+list(map(one_hot_dna,reverse_com_seq))
            bw_regression = get_regression(bw_path,control_bed_df)
            print('获取反向互补序列的信号')
            bw_regression_all = bw_regression+bw_regression
            m_sample_name = []
            for k in range(len(control_bed_df)):
                m_sample_name.append(str(control_bed_df.iloc[k,0])+','+str(control_bed_df.iloc[k,1])+','+str(control_bed_df.iloc[k,2])+','+'Reverse_complementation')
            sample_name_all = sample_name+m_sample_name
            dataset_df = pd.DataFrame({'sample':sample_name_all,'seq_one_hot':seq_all,'target':bw_regression_all})
            return dataset_df
        else:
            print('您选择不使用数据增强')
            bw_regression = get_regression(bw_path,control_bed_df)
            dataset_df = pd.DataFrame({'sample':sample_name,'seq_one_hot':seq,'target':bw_regression})
            return dataset_df
        
        
        
    if dataset_type=='base_regression':
        if Data_Augmentation:
            print('通过取反向互补序列进行数据增强，经此步骤，您最终得到的样本量将翻倍')
            #map返回迭代器，需要list转换
            #返回反向互补序列
            #这里错了，放进来的不能是seq
            seq_ = get_seq_list(fasta_path,control_bed_df)
            reverse_com_seq = list(map(DNA_complement , seq_))
            #reverse_com_seq要在此处进行one-hot编码
            seq_all = seq+list(map(one_hot_dna,reverse_com_seq))
            bw_base_regression = get_base_regression(bw_path,control_bed_df)
            print('获取反向互补序列的信号')
            bw_base_regression_all = bw_base_regression+bw_base_regression
            m_sample_name = []
            for k in range(len(control_bed_df)):
                m_sample_name.append(str(control_bed_df.iloc[k,0])+','+str(control_bed_df.iloc[k,1])+','+str(control_bed_df.iloc[k,2])+','+'Reverse_complementation')
            sample_name_all = sample_name+m_sample_name
            dataset_df = pd.DataFrame({'sample':sample_name_all,'seq_one_hot':seq_all,'target':bw_base_regression_all})
            return dataset_df
            
        else:
            print('您选择不使用数据增强')
            bw_base_regression = get_base_regression(bw_path,control_bed_df)
            dataset_df = pd.DataFrame({'sample':sample_name,'seq_one_hot':seq,'target':bw_base_regression})
            return dataset_df

