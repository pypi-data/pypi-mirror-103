# zzz_deep_genome

一个辅助基因组学深度学习模型构建的函数库

A library of functions to assist in the construction of deep learning models for genomics.



## 主要功能（Key Features）

1、根据给定文件（bed、bigwig等）和条件（序列长度等），获取用于组学深度学习训练的训练集。

Obtain a training set for deep learning training in genomics based on a given file (bed, bigwig, etc.) and conditions (sequence length, etc.).



2、训练数据（label）的标准化。

Normalization of training data (label).



3、根据JASPAR数据库的pfms矩阵信息，构建用于初始化CNN的参数矩阵。

The parameter matrix for initializing the CNN is constructed based on the pfms matrix information from the JASPAR database.



4、获取一组或多组等长短序列对应的pfm、ppm、pwm矩阵。

Get the pfm, ppm, and pwm matrices corresponding to one or more sets of equal-length short sequences.



## 快速开始（Quick Start）

### 安装

```python
pip install zzx-deep-genome
```



### 获取训练数据集（Obtain training data set）

```python
from zzx_deep_genome.get_dataset import genome_dataset

genome_dataset(bed_path,fasta_path,seq_len=1024,
               genome_size_control=None,dataset_type='regression',
               bw_path=None,Data_Augmentation=False)
```



1、参数：

- bed_path：bed文件路径，指定用于构建数据集的样本。

  对分类任务，要求四列：chr、start、end、class

  对分类任务，要求三列：chr、start、end

- fasta_path：参考基因组路径

- seq_len：指定每个样本长度

  若bed文件中某样本的长度超过指定长度，则截取中间seq_len长度

  若bed文件中某样本的长度小于指定长度，则向两边扩展到seq_len长度

- genome_size_control：控制文件，如果指定该文件路径，则从根据seq_len截取（或扩展）出的样本中过滤掉不符合控制文件条件的样本。控制文件(指定染色体及其最大长度，列由TAB间隔)格式如下：

  ```
  chr01<TAB>1998644
  chr02<TAB>5783384
  ...
  chrn<TAB>6457466
  ```

  

- dataset_type：该模块支持对三种任务（classification、regression、base_regression）进行数据预处理，获取数据集。

- bw_path：对回归任务，需要给定对应bigwig文件路径，该模块将从bigwig文件中提取信号。

- Data_Augmentation：是否进行数据增强，若为True，则会使用反向互补序列进行数据增强。



2、返回结果

根据dataset_type的选择有不同返回：

- classification：返回一个三列的数据框，第一列为染色体号起止点等信息（即原始bed文件信息）、第二列为one-hot编码后的对应定长DNA序列，第三列为类别标签。
- regression：返回一个三列的数据框，第一列为染色体号起止点等信息（即原始bed文件信息）、第二列为one-hot编码后的对应定长DNA序列，第三列为对应序列上的平均信号值。
- base_regression：返回一个三列的数据框，第一列为染色体号起止点等信息（即原始bed文件信息）、第二列为one-hot编码后的对应定长DNA序列，第三列为对应序列上的信号值（每个碱基位置都有值）。



### 数据集（label）的标准化

``` python
from zzx_deep_genome.Standardization import bw_scale
bw_scale(in_path,out_path,standard=32)
```



1、参数

- in_path：输入（bigwig）文件路径
- out_path：输出（标准化后的bigwig）文件路径
- standard：高斯核的标准差



2、返回结果

标准化后的（bigwig）文件



### 根据JASPAR数据库先验信息进行CNN初始化

```python
from zzx_deep_genome.filter_initialization import filter_initialization_matrix

filter_initialization_matrix(taxonomic_groups='plants',data_local = None,
                                 filters=64,
                                 L_=8,
                                 pattern='ppm_rp25',
                                 background_acgt=[0.25, 0.25, 0.25, 0.25])
```



1、参数：

- taxonomic_groups：选择类群，目前只支持plants、fungi、vertebrates、insects

- data_local：本地文件（要求JASPAR PFMS格式）路径，若为None，则该模块将根据taxonomic_groups的设置，自动从JASPAR数据库下载对应文件到当前工作目录。

- filters：卷积滤波器的数目

- L_：卷积核的尺寸（对长度超过设定值的PFM，会根据信息熵筛选片段）

- pattern：模式，支持ppm_rp25（返回ppm矩阵每个位置减0.25后得到的均值为0的矩阵）、ppm（返回pp m矩阵）、pwm（返回pwm矩阵）

- background_acgt：计算pwm时需要的ACGT背景

  

2、返回结果

根据pattern的设置有不同返回：

- pattern = "ppm_rp25"，返回ppm矩阵每个位置减0.25后得到的均值为0的矩阵（可以尝试直接用于初始化）
- pattern = "ppm"，返回ppm矩阵
- pattern = "pwm"，返回pwm矩阵



### 获取pfm、ppm、pwm矩阵

```python
from zzx_deep_genome.get_pwm import get_pwm
get_pwm(file_path,background_acgt = [0.25,0.25,0.25,0.25],type_='pfm')
```



1、参数：

- file_path：输入文件路径，输入文件形如：

  ``` 
  >1
  ACTTTG
  ACCCCG
  ACCCTG
  
  >2
  AATAGCAAA
  AAATCCCGG
  AATTTCCCG
  ATCCCGGGA
  CGTTTGGGG
  ```

  

- background_acgt：计算pwm需要的ACGT背景

- type_：可选pfm、ppm、pwm，决定了最终的返回结果



2、返回结果

根据type_的设置有不同返回：

- pfm：返回pfm矩阵列表
- ppm：返回ppm矩阵列表
- pwm：返回pwm矩阵列表

