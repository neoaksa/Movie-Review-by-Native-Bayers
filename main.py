from BayersDict import BayerDict
from multiprocessing import Process

def main():
    # windows
    # pos_inputpath = "D:\\minitest\\aclImdb\\train\\pos\\"   # training folder for positive
    # pos_outpath = "D:\\minitest\\aclImdb\\pos_output.csv"   # positive output
    # neg_inputpath = "D:\\minitest\\aclImdb\\train\\neg\\"   # training folder for negative
    # neg_outpath = "D:\\minitest\\aclImdb\\neg_output.csv"   # negative output
    # linux
    pos_inputpath = "/home/jie/Documents/aclImdb/train/pos/"   # training folder for positive
    pos_outpath = "/home/jie/Documents/aclImdb/pos_output.csv"  # positive output
    neg_inputpath = "/home/jie/Documents/aclImdb/train/neg/"   # training folder for negative
    neg_outpath = "/home/jie/Documents/aclImdb/neg_output.csv"   # negative output

    aBayerdict = BayerDict()
    p_neg = Process(target=aBayerdict.readfile, args=(neg_inputpath, "N",neg_outpath, "w"))
    p_pos = Process(target=aBayerdict.readfile, args=(pos_inputpath, "P",pos_outpath, "w"))
    p_neg.start()
    p_pos.start()
    # aBayerdict.readfile(neg_inputpath, "N",neg_outpath, "w") # negtive class
    # aBayerdict.readfile(pos_inputpath, "P",pos_outpath,"w") # postive class


if __name__ == '__main__':
    main()
