from ._class_tester import _class_tester_controller
from ._regr_tester import _regr_tester_controller
from ._clust_tester import _cluster_tester_controller


def best_classificator(x, y, score_type='f1_score', json_file=False, test_size=0.2):
    """
    Returns the information and the object related to a classification algorithm with the best score
     for the dataset passed as parameter(x, y).

    :param x: Set of independent variables  (input set)
    :param y: Set of dependent variables    (output set)
    :param score_type: Type of score that determines the best algorithm to research. The available score are:
                        'precision_score', 'accuracy_score', 'recall_score' and 'f1_score'. Default is the 'f1_score'.
    :param json_file: Indicates whether to create a json file with the results of all tested algorithms.Default is False
    :param test_size: Allows you to set the size of the test set. Default is 0.2
    :return: a tuple:
                - dict object with info about the best chosen algorithm
                - the already fitted best chosen algorithm
    """
    return _class_tester_controller(x, y, score_type, json_file, test_size)


def best_regressor(x, y, score_type='r2_score', json_file=False, test_size=0.2, mean_squared_return=False):
    """
    Returns the information and the object related to a regression algorithm with the best score
     for the dataset passed as parameter(x, y).

    :param x: Set of independent variables  (input set)
    :param y: Set of dependent variables    (output set)
    :param score_type: Type of score that determines the best algorithm to research. The only available score type
                        is 'r2_score'. Default is 'r2_score'.
                        CAUTION: for non-linear dataset, r2_score is not a good score to consider.
                        Instead, it's always available the mean_squared_score. To select the best regressor with
                        the best mean_squared_error score, you must change in mean_squared_return=True.
    :param json_file: Indicates whether to create a json file with the results of all tested algorithms.Default is False
    :param test_size: Allows you to set the size of the test set. Default is 0.2
    :param mean_squared_return: set the return parameter to return the information and the regressor object
                                based on the best mean_squared_error. Default is False
    :return: a tuple:
                - dict object with info about the best chosen algorithm
                - the already fitted best chosen algorithm
    """
    return _regr_tester_controller(x, y, score_type, json_file, test_size, mean_squared_return)


def best_cluster(x, max_clusters=10, elbow_graph=False, bidim_graph=False):
    """
    Returns the information and the object related to the k-means algorithm with the best number of neighbours
    for the dataset x passed as parameters. The user can also choose to visualize graphs.

    :param x: Set of independent variables  (input set)
    :param max_clusters: Maximum number of clusters to test. Default is 10
    :param elbow_graph: Show the elbow graph about the tested number of neighbours. Default is False
    :param bidim_graph: It shows the dataset split according to the number of clusters defined as best.
                        It allows a better view of how the dataset has been split. Default is False.
    :return: a tuple:
                - dict object with info about the best chosen algorithm
                - the already fitted best chosen algorithm
    """
    return _cluster_tester_controller(x, max_clusters, elbow_graph, bidim_graph)
