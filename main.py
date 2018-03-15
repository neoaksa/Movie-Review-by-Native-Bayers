from BayersDict import BayerDict
from multiprocessing import Process

def main():
    pos_inputpath = "D:\\minitest\\aclImdb\\train\\pos\\"
    pos_outpath = ".\\data\\pos_output.csv"
    neg_inputpath = "D:\\minitest\\aclImdb\\train\\neg\\"
    neg_outpath = ".\\data\\neg_output.csv"
    aBayerdict = BayerDict()
    p_neg = Process(target=aBayerdict.readfile, args=(neg_inputpath, "N",neg_outpath, "w"))
    p_pos = Process(target=aBayerdict.readfile, args=(pos_inputpath, "P",pos_outpath, "w"))
    p_neg.start()
    p_pos.start()
    # aBayerdict.readfile(neg_inputpath, "N",neg_outpath, "w") # negtive class
    # aBayerdict.readfile(pos_inputpath, "P",pos_outpath,"w") # postive class


if __name__ == '__main__':
    main()
