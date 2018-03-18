from BayersDict import BayerDict
from multiprocessing import Process
from multiprocessing import Pool
from functools import partial
import pandas as pd

def main():
    # windows
    # pos_inputpath = "D:\\minitest\\aclImdb\\train\\pos\\"   # training folder for positive
    # pos_outpath = "D:\\minitest\\aclImdb\\pos_output.csv"   # positive output
    # neg_inputpath = "D:\\minitest\\aclImdb\\train\\neg\\"   # training folder for negative
    # neg_outpath = "D:\\minitest\\aclImdb\\neg_output.csv"   # negative output
    # linux
    pos_inputpath = "/home/jie/Documents/aclImdb/train/pos/"  # training folder for positive
    pos_outpath = "/home/jie/Documents/aclImdb/pos_output.csv"  # positive output
    neg_inputpath = "/home/jie/Documents/aclImdb/train/neg/"  # training folder for negative
    neg_outpath = "/home/jie/Documents/aclImdb/neg_output.csv"  # negative output

    # create dictionary
    # createDic(pos_inputpath,neg_inputpath,pos_outpath,neg_outpath)
    # analysis dictionary
    createanlysis(pos_outpath,neg_outpath)
    # neg_df = pd.read_csv(neg_outpath)
    # neg_df = neg_df.sort_values(by=["perc"], ascending=False)
    # print(neg_df[neg_df["word"] == "Pita"].empty)

# create dictionary
def createDic(pos_inputpath,neg_inputpath,pos_outpath,neg_outpath):
    aBayerdict = BayerDict()
    p_neg = Process(target=aBayerdict.readfile, args=(neg_inputpath, "N", neg_outpath, "w"))
    p_pos = Process(target=aBayerdict.readfile, args=(pos_inputpath, "P", pos_outpath, "w"))
    p_neg.start()
    p_pos.start()
    # aBayerdict.readfile(neg_inputpath, "N",neg_outpath, "w") # negtive class
    # aBayerdict.readfile(pos_inputpath, "P",pos_outpath,"w") # postive class

def createanlysis(pos_outpath,neg_outpath):
    slice_list = [1,2,3,4]
    params_x = partial(analysis_dic, posfile=pos_outpath, negfile=neg_outpath,
                       analysis_perc=0.01,slice=4,gap_threhold=0.4)
    result_list = Pool(4).map(params_x, slice_list)
    df_result = pd.DataFrame(data=None, columns=["word", "perc", "category", "type"])
    for i in range(4):
        if result_list[i].empty:
            continue
        else:
            df_result.append(result_list[i])
    df_result.to_csv("/home/jie/Documents/aclImdb/new.csv")

    # p_analysis1 = Process(target=analysis_dic, args=(pos_outpath,neg_outpath,analysis_perc, slice,1, gap_threhold))
    # p_analysis2 = Process(target=analysis_dic, args=(pos_outpath, neg_outpath, analysis_perc,slice, 2, gap_threhold))
    # p_analysis3 = Process(target=analysis_dic, args=(pos_outpath, neg_outpath, analysis_perc,slice, 3, gap_threhold))
    # p_analysis4 = Process(target=analysis_dic, args=(pos_outpath, neg_outpath, analysis_perc,slice, 4, gap_threhold))
    # p_analysis1.start()
    # p_analysis2.start()
    # p_analysis3.start()
    # p_analysis4.start()

# analysis two dictionary
# analysis_perc: proportion of analysis words
# gap_threhold: gap of same words between pos and neg
# slice: how many slices for multi process
# sliceindex: which slice for this function processing
def analysis_dic(sliceindex,posfile,negfile,analysis_perc, slice,gap_threhold):
    # df for save result
    df_result = pd.DataFrame(data=None,columns=["word","perc","category","type"])
    # read csv from pos and neg files
    pos_df = pd.read_csv(posfile)
    neg_df = pd.read_csv(negfile)
    pos_df = pos_df.sort_values(by=["perc"],ascending=False)
    neg_df = neg_df.sort_values(by=["perc"], ascending=False)
    max_pos_row = int(len(pos_df.axes[0]) * analysis_perc)
    max_neg_row = int(len(neg_df.axes[0]) * analysis_perc)
    pos_slice_size = int(max_pos_row / slice)
    neg_slice_size = int(max_neg_row / slice)
    start_pos_row = (sliceindex - 1) * pos_slice_size
    start_neg_row = (sliceindex - 1) * neg_slice_size
    end_pos_row = sliceindex * pos_slice_size
    end_neg_row = sliceindex * neg_slice_size
    pos_df_slice = pos_df.iloc[start_pos_row: end_pos_row]
    neg_df_slice = neg_df.iloc[start_neg_row: end_neg_row]
    # iterative item in data frame pos
    row_num = 0
    row_num_result = 0
    try:
        for index, item in pos_df_slice.iterrows():
            # print(item)
            # if row_num < start_pos_row:
            #     row_num += 1
            #     continue
            if row_num > end_pos_row:
                break
            # not find
            elif neg_df[neg_df["word"] == item["word"]].empty:
                df_result.loc[row_num_result] = [item["word"], item["perc"], "P","1"]
                row_num_result += 1
                row_num += 1
                print(item["word"])
            # gap greater than threshold
            elif abs(neg_df[neg_df["word"] == item["word"]].iloc[0]["perc"] - item["perc"]) >= gap_threhold:
                df_result.loc[row_num_result] = [item["word"],item["perc"],"P","2"]
                row_num_result += 1
                row_num += 1
                print(item["word"])

    except:
        print(item)
    # iterative item in data frame neg
    row_num = 0
    try:
        for index, item in neg_df_slice.iterrows():
            # print(item)
            # if row_num < start_pos_row:
            #     row_num += 1
            #     continue
            if row_num > end_neg_row:
                break
            # not find
            elif pos_df[pos_df["word"] == item["word"]].empty:
                df_result.loc[row_num_result] = [item["word"], item["perc"], "N","1"]
                row_num_result += 1
                row_num += 1
                print(item["word"])
            # gap greater than threshold
            elif abs(pos_df[pos_df["word"] == item["word"]].iloc[0]["perc"] - item["perc"]) >= gap_threhold:
                df_result.loc[row_num_result] = [item["word"], item["perc"], "N","2"]
                row_num_result += 1
                row_num += 1
                print(item["word"])

    except:
        print(item)

    return df_result

if __name__ == '__main__':
    main()
