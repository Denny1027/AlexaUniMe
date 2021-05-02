import sys
from ._utils import NumpyArrayEncoder, bcolors as c
from sklearn.metrics import confusion_matrix, precision_score, accuracy_score, f1_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import json

available_score = ('precision_score', 'accuracy_score', 'recall_score', 'f1_score')


def _class_tester_controller(x, y, score_type='f1_score', json_file=False, test_size=0.2):
    if score_type not in available_score:
        raise Exception('Score type not supported.')

    # divide into train and test set with train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=0)

    # Introduction
    print("{}***************************".format(c.OKGREEN))
    print("  CLASSIFICATOR FINDER")
    print("***************************{}".format(c.ENDC))

    json_results = {}
    methods_name = ('logistic_regression', 'k_nn', 'naive_bayes', 'SVM', 'classification_tree', 'random_forest')
    methods = [__logistic_regression_tester(x_train, y_train, x_test, y_test, score_type),
               __k_nn_tester(x_train, y_train, x_test, y_test, score_type),
               __naive_bayes_tester(x_train, y_train, x_test, y_test, score_type),
               __support_vector_machine(x_train, y_train, x_test, y_test, score_type),
               __classification_tree(x_train, y_train, x_test, y_test, score_type),
               __random_forest(x_train, y_train, x_test, y_test, score_type)
               ]

    for i in range(len(methods_name)):
        json_results[methods_name[i]] = methods[i]

    best_val = 0
    best_method = None
    conf_matr = None
    best_class = None

    for el in json_results.keys():
        if json_results[el][0][score_type] > best_val:
            best_val, best_method, conf_matr, best_class = json_results[el][0][score_type], el, json_results[el][0]['confusion_matrix'], json_results[el][1]

    print("\n")
    print("{}----------------------------------------------------".format(c.HEADER))
    print("                    RESULTS        ")
    print("                  for {}".format(score_type))
    print("----------------------------------------------------")
    print("Best method: {}".format(best_method))
    print("Score: {}".format(best_val))
    print("Confusion Matrix:")
    print(conf_matr)
    print("Full info:")
    print(json_results[best_method][0], c.ENDC)

    if json_file:
        filename = "{}_class.json".format(score_type)
        with open(filename, 'w') as outfile:
            json.dump(json_results, outfile, cls=NumpyArrayEncoder)

    json_results[best_method][0].update({'method': best_method})
    return json_results[best_method][0], best_class


def __logistic_regression_tester(x_train, y_train, x_test, y_test, score):
    from sklearn.linear_model import LogisticRegression

    print("\n{}-- Logistic Regression --{}".format(c.WARNING, c.ENDC))
    # Scaling
    sc = StandardScaler()
    x_train = sc.fit_transform(x_train)
    x_test = sc.transform(x_test)

    lr = LogisticRegression()
    lr.fit(x_train, y_train)
    y_pred = lr.predict(x_test)

    descr = {}
    if score == 'f1_score':
        descr[score] = f1_score(y_test, y_pred)
    elif score == 'precision_score':
        descr[score] = precision_score(y_test, y_pred)
    elif score == 'recall_score':
        descr[score] = recall_score(y_test, y_pred)
    elif score == 'accuracy_score':
        descr[score] = accuracy_score(y_test, y_pred)

    descr['confusion_matrix'] = confusion_matrix(y_test, y_pred)

    print("{}    --BEST--> {}:{}  | Conf. Matrix: {}{}".format(c.OKGREEN, score, descr[score],
                                                               descr['confusion_matrix'].tolist(), c.ENDC))
    return descr, lr


def __k_nn_tester(x_train, y_train, x_test, y_test, score):
    from sklearn.neighbors import KNeighborsClassifier

    value = sys.float_info.min
    neigh = 0
    matrix = None
    best_knn = None

    print("\n{}-- K-NN --{}".format(c.WARNING, c.ENDC))
    # Test
    for i in range(3, 21):
        knn = KNeighborsClassifier(n_neighbors=i, metric='minkowski', p=2)
        knn.fit(x_train, y_train)
        y_pred = knn.predict(x_test)

        temp_value = 0
        if score == 'f1_score':
            temp_value = f1_score(y_test, y_pred)
        elif score == 'precision_score':
            temp_value = precision_score(y_test, y_pred)
        elif score == 'recall_score':
            temp_value = recall_score(y_test, y_pred)
        elif score == 'accuracy_score':
            temp_value = accuracy_score(y_test, y_pred)
        temp_matrix = confusion_matrix(y_test, y_pred)

        if temp_value > value:
            print("{} ----> neigh: {}, {}: {} | conf.Matrix: {}{}".format(c.OKCYAN, i, score, temp_value,
                                                                          temp_matrix.tolist(), c.ENDC))
            value, neigh, matrix, best_knn = temp_value, i, temp_matrix, knn
        else:
            print(" ----> neigh: {}, {}: {} | conf.Matrix: {}".format(i, score, temp_value, temp_matrix.tolist()))

    # Results
    print("{}    --BEST--> neigh: {}, {}: {} | conf.Matrix: {}{}".format(c.OKGREEN, neigh, score, value,
                                                                         matrix.tolist(), c.ENDC))

    return {score: value, 'neighboors': neigh, 'confusion_matrix': matrix}, best_knn


def __naive_bayes_tester(x_train, y_train, x_test, y_test, score):
    from sklearn.naive_bayes import GaussianNB

    print("\n{}-- Naive Bayes Classificator --{}".format(c.WARNING, c.ENDC))
    nb = GaussianNB()
    nb.fit(x_train, y_train)
    y_pred = nb.predict(x_test)

    descr = {}
    if score == 'f1_score':
        descr[score] = f1_score(y_test, y_pred)
    elif score == 'precision_score':
        descr[score] = precision_score(y_test, y_pred)
    elif score == 'recall_score':
        descr[score] = recall_score(y_test, y_pred)
    elif score == 'accuracy_score':
        descr[score] = accuracy_score(y_test, y_pred)

    descr['confusion_matrix'] = confusion_matrix(y_test, y_pred)

    print("{}    --BEST--> {}:{}  | Conf. Matrix: {}{}".format(c.OKGREEN, score, descr[score],
                                                               descr['confusion_matrix'].tolist(), c.ENDC))
    return descr, nb


def __support_vector_machine(x_train, y_train, x_test, y_test, score):
    from sklearn.svm import SVC

    kernel_tuple = ('linear', 'rbf', 'sigmoid')

    sc = StandardScaler()
    x_train = sc.fit_transform(x_train)
    x_test = sc.transform(x_test)

    print("\n{}-- Support Vector Classificator --{}".format(c.WARNING, c.ENDC))

    value = sys.float_info.min
    degree_poly = 0
    kernel = None
    matrix = None
    best_svm = None

    # Not poly kernel
    for k in kernel_tuple:
        svm = SVC(kernel=k, random_state=0)
        svm.fit(x_train, y_train)
        y_pred = svm.predict(x_test)

        temp_value = 0
        if score == 'f1_score':
            temp_value = f1_score(y_test, y_pred)
        elif score == 'precision_score':
            temp_value = precision_score(y_test, y_pred)
        elif score == 'recall_score':
            temp_value = recall_score(y_test, y_pred)
        elif score == 'accuracy_score':
            temp_value = accuracy_score(y_test, y_pred)

        temp_matrix = confusion_matrix(y_test, y_pred)

        if temp_value > value:
            print("{}  ----> kernel: {}, {}: {} | conf.Matrix: {}{}".format(c.OKCYAN, k, score, temp_value,
                                                                            temp_matrix.tolist(), c.ENDC))
            value, kernel, matrix, best_svm = temp_value, k, temp_matrix, svm
        else:
            print("  ----> kernel: {}, {}: {} | conf.Matrix: {}".format(k, score, temp_value, temp_matrix.tolist()))

    # Now, poly kernel!
    for i in range(2, 11):

        svm = SVC(kernel='poly', degree=i, random_state=0)
        svm.fit(x_train, y_train)
        y_pred = svm.predict(x_test)

        temp_value = 0
        if score == 'f1_score':
            temp_value = f1_score(y_test, y_pred)
        elif score == 'precision_score':
            temp_value = precision_score(y_test, y_pred)
        elif score == 'recall_score':
            temp_value = recall_score(y_test, y_pred)
        elif score == 'accuracy_score':
            temp_value = accuracy_score(y_test, y_pred)

        temp_matrix = confusion_matrix(y_test, y_pred)

        if temp_value > value:
            print("{}  ----> kernel: poly, degree: {}, {}: {} | conf.Matrix: {}{}".format(c.OKCYAN, i, score, temp_value
                                                                                          , temp_matrix.tolist(),
                                                                                          c.ENDC))
            value, kernel, degree_poly, matrix, best_svm = temp_value, 'poly', i, temp_matrix, best_svm
        else:
            print("  ----> kernel: poly, degree: {}, {}: {} | conf.Matrix: {}".format(i, score, temp_value,
                                                                                      temp_matrix.tolist()))

    # Now, send results
    if degree_poly != 0:
        print("{}    --BEST--> kernel: poly, degree: {}, {}: {}  | Conf. Matrix: {}{}".format(c.OKGREEN, degree_poly,
                                                                                              score, value,
                                                                                              matrix.tolist(), c.ENDC))
    else:
        print("{}    --BEST--> kernel: {}, {}: {}  | Conf. Matrix: {}{}".format(c.OKGREEN, kernel, score, value,
                                                                                matrix.tolist(), c.ENDC))

    desc = {'kernel': kernel, 'poly_degree': degree_poly, score: value, 'confusion_matrix': matrix}
    return desc, best_svm


def __classification_tree(x_train, y_train, x_test, y_test, score):
    from sklearn.tree import DecisionTreeClassifier

    print("\n{}-- Classification Tree --{}".format(c.WARNING, c.ENDC))

    dt = DecisionTreeClassifier(criterion='entropy')
    dt.fit(x_train, y_train)
    y_pred = dt.predict(x_test)

    descr = {}
    if score == 'f1_score':
        descr[score] = f1_score(y_test, y_pred)
    elif score == 'precision_score':
        descr[score] = precision_score(y_test, y_pred)
    elif score == 'recall_score':
        descr[score] = recall_score(y_test, y_pred)
    elif score == 'accuracy_score':
        descr[score] = accuracy_score(y_test, y_pred)

    descr['confusion_matrix'] = confusion_matrix(y_test, y_pred)

    print("{}    --BEST--> {}:{}  | Conf. Matrix: {}{}".format(c.OKGREEN, score, descr[score],
                                                               descr['confusion_matrix'].tolist(), c.ENDC))
    return descr, dt


def __random_forest(x_train, y_train, x_test, y_test, score):
    from sklearn.ensemble import RandomForestClassifier

    trees = 0
    value = sys.float_info.min
    matrix = None
    best_forest = None

    print("\n{}-- Random Forest --{}".format(c.WARNING, c.ENDC))

    for i in range(20, 200, 20):
        rf = RandomForestClassifier(n_estimators=i, criterion='entropy', random_state=0)
        rf.fit(x_train, y_train)
        y_pred = rf.predict(x_test)

        temp_value = 0
        if score == 'f1_score':
            temp_value = f1_score(y_test, y_pred)
        elif score == 'precision_score':
            temp_value = precision_score(y_test, y_pred)
        elif score == 'recall_score':
            temp_value = recall_score(y_test, y_pred)
        elif score == 'accuracy_score':
            temp_value = accuracy_score(y_test, y_pred)
        temp_matrix = confusion_matrix(y_test, y_pred)

        if temp_value > value:
            print("{}  ----> estimators: {}, {}: {} | conf.Matrix: {}{}".format(c.OKCYAN, i, score, temp_value,
                                                                                temp_matrix.tolist(), c.ENDC))
            value, trees, matrix, best_forest = temp_value, i, temp_matrix, rf
        else:
            print("  ----> estimators: {}, {}: {} | conf.Matrix: {}".format(i, score, temp_value, temp_matrix.tolist()))

    # Now, send results
    print("{}    --BEST--> estimators: {}, {}: {}  | Conf. Matrix: {}{}".format(c.OKGREEN, trees, score, value,
                                                                                matrix.tolist(), c.ENDC))
    return {'estimators': trees, score: value, 'confusion_matrix': matrix}, best_forest
