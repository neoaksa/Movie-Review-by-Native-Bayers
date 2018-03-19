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
    # createanlysis(pos_outpath,neg_outpath)

    # validation
    test_pos_inputpath = "/home/jie/Documents/aclImdb/test/pos/"
    test_neg_inputpath = "/home/jie/Documents/aclImdb/test/neg/"
    validation(test_pos_inputpath,test_neg_inputpath,pos_outpath,neg_outpath)

# create dictionary
def createDic(pos_inputpath,neg_inputpath,pos_outpath,neg_outpath):
    aBayerdict = BayerDict()
    p_neg = Process(target=aBayerdict.readfile, args=(neg_inputpath, "N", neg_outpath, "w"))
    p_pos = Process(target=aBayerdict.readfile, args=(pos_inputpath, "P", pos_outpath, "w"))
    p_neg.start()
    p_pos.start()

def createanlysis(pos_outpath,neg_outpath):
    slice_list = [1,2,3,4]
    params_x = partial(analysis_dic, posfile=pos_outpath, negfile=neg_outpath,
                       analysis_perc=0.01,slice=4,gap_threhold=0.1)
    result_list = Pool(4).map(params_x, slice_list)
    df_result = pd.DataFrame(data=None, columns=["word", "perc", "category", "type"])
    for i in range(4):
        if result_list[i].empty:
            continue
        else:
            df_result = df_result.append(result_list[i], ignore_index=True)
    df_result.to_csv("/home/jie/Documents/aclImdb/new.csv")

def validation(test_pos_inputpath,test_neg_inputpath, pos_outpath,neg_outpath):
    aBayerdict = BayerDict()
    p_pos = Process(target=aBayerdict.validation, args=(test_pos_inputpath, \
                                                        pos_outpath, neg_outpath, "pos", 150, 6.778643071565863e-07))
    p_neg = Process(target=aBayerdict.validation, args=(test_neg_inputpath, \
                                                        pos_outpath, neg_outpath, "neg", 150, 6.965745597735854e-07))
    p_pos.start()
    p_neg.start()

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
            mapped_item = neg_df[neg_df["word"] == item["word"]]

            # not find
            if mapped_item.empty:
                df_result.loc[row_num_result] = [item["word"], item["perc"], "P","1"]
                row_num_result += 1
                row_num += 1
                print(item["word"] + " type P1")
            # gap greater than threshold
            elif item["perc"] - mapped_item.iloc[0]["perc"] >= gap_threhold:
                df_result.loc[row_num_result] = [item["word"],item["perc"],"P","2"]
                row_num_result += 1
                row_num += 1
                print(item["word"] + " type P2")
            # else:
            #     print(str(mapped_item.iloc[0]["perc"]) +" / " +  str(item["perc"]))

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
            mapped_item = pos_df[pos_df["word"] == item["word"]]
            # not find
            if mapped_item.empty:
                df_result.loc[row_num_result] = [item["word"], item["perc"], "N","1"]
                row_num_result += 1
                row_num += 1
                # print(item["word"] + " type N1")
            # gap greater than threshold
            elif item["perc"] - mapped_item.iloc[0]["perc"] >= gap_threhold:
                df_result.loc[row_num_result] = [item["word"], item["perc"], "N","2"]
                row_num_result += 1
                row_num += 1
                # print(item["word"] + " type N2")

    except:
        print(item)

    return df_result

if __name__ == '__main__':
    main()
