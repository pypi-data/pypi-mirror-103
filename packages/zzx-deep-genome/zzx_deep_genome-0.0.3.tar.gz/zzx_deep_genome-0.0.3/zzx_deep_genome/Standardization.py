import pyBigWig
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d

#已测试通过
#用于对bw文件进行标准化和平滑，输出新bw文件
def bw_scale(in_path,out_path,standard=32 ):
    in_bw = pyBigWig.open(in_path)
    out_bw = pyBigWig.open(out_path,'w')
    out_bw.addHeader([(k,v) for k,v in in_bw.chroms().items()])
    for i in in_bw.chroms():
        scale_ = sum(in_bw.values(i,0,in_bw.chroms()[i]))/in_bw.chroms()[i]
        scale_bw_list = np.array(in_bw.values(i,0,in_bw.chroms()[i]))/scale_
        #sigma设置了高斯核的标准差
        fil_scale_bw_list = gaussian_filter1d(list(scale_bw_list), sigma=standard, truncate=3)
        out_bw.addEntries(i, 0, values = fil_scale_bw_list.astype('float16'), span=1, step=1)
    out_bw.close()
    in_bw.close()