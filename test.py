import multiprocessing


def runSimulation(params):
    """This is the main processing function. It will contain whatever
    code should be run on multiple processors.

    """


    return params


if __name__ == '__main__':
    # Define the parameters to test
    param1 = range(10)
    param2 = range(2, 10, 2)

    # Zip the parameters because pool.map() takes only one iterable
    params = zip(param1, param2)

    pool = multiprocessing.Pool()
    results = pool.map(runSimulation, params)
    print(results)
