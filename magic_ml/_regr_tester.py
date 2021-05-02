import json
import sys
from ._utils import NumpyArrayEncoder, bcolors as c
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

available_score = ('r2_score')


def _regr_tester_controller(x, y, score_type='r2_score', json_file=False, test_size=0.2, mean_squared_return=False):
    """ ATTENZIONE! Non considerare r2_score per regressione non lineare.
    Guardare invece la mean_squared_error (Errore quadratico medio) """
    if score_type not in available_score:
        raise Exception('Score type not supported.')

    # Introduction
    print("{}***************************".format(c.OKGREEN))
    print("  REGRESSOR FINDER")
    print("***************************{}".format(c.ENDC))

    json_results = {}
    methods_name = ('simple_linear', 'poly_regr', 'support_vector_regressor', 'random_forest')
    methods = [__simple_linear_regression(x, y, score_type, test_size),
               __poly_linear_regression(x, y, score_type),
               __support_vector_regressor(x, y, score_type),
               # __decision_tree_regressor(x, y, score_type),
               __random_forest_regressor(x, y, score_type)
               ]

    for i in range(len(methods_name)):
        json_results[methods_name[i]] = methods[i]

    best_val = sys.float_info.min
    best_method = None
    best_regr = None
    best_sq_val = sys.float_info.max
    best_sq_method = None
    best_sq_regr = None

    for el in json_results.keys():
        if el is None:
            continue
        elif json_results[el][0][score_type] > best_val:
            best_val, best_method, best_regr = json_results[el][0][score_type], el, json_results[el][1]

        if json_results[el][0]['mean_squared_error'] < best_sq_val:
            best_sq_val, best_sq_method, best_sq_regr = json_results[el][0]['mean_squared_error'], el, json_results[el][
                1]

    # Print results
    print("\n")
    print("{}----------------------------------------------------".format(c.HEADER))
    print("                    RESULTS        ")
    print("                  for {}".format(score_type))
    print("----------------------------------------------------")
    print(" for {}".format(score_type))
    print("----------------------")
    print("Best method: {}".format(best_method))
    print("Score: {}".format(best_val))
    print("Full info:")
    print(json_results[best_method][0])
    print("----------------------")
    print(" for mean-squared-error")
    print("----------------------")
    print("Best method: {}".format(best_sq_method))
    print("Score: {}".format(best_sq_val))
    print("Full info:")
    print(json_results[best_sq_method][0], c.ENDC)

    # Create a JSON FILE with all info
    if json_file:
        filename = "{}_regr.json".format(score_type)
        with open(filename, 'w') as outfile:
            json.dump(json_results, outfile, cls=NumpyArrayEncoder)

    json_results[best_method][0].update({'method': best_method})
    json_results[best_sq_method][0].update({'method': best_sq_method})

    regressor = best_sq_regr if mean_squared_return else best_regr
    data_result = {'best_score': json_results[best_method][0], 'best_mean_squared_errore': json_results[best_sq_method][0]}
    return data_result, regressor


def __simple_linear_regression(x, y, score, test_size):
    from sklearn.linear_model import RidgeCV, LassoCV, ElasticNetCV

    print('{}-- Simple Linear Regression --{}'.format(c.WARNING, c.ENDC))

    methods_list = (RidgeCV(store_cv_values=True), LassoCV(), ElasticNetCV())

    # returned value
    value = sys.float_info.min
    m2e = sys.float_info.min
    meth = None
    best_regr = None

    # split x and y sets in train and test
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=0)

    # Foreach regressor in methods_list
    for el in methods_list:
        regr = el

        try:
            regr.fit(x_train, y_train)
        except ValueError:
            print("** ", type(el).__name__, ' Error during fitting: abort')
            continue

        y_pred = regr.predict(x_test)

        temp_value = sys.float_info.min
        if score == 'r2_score':
            temp_value = r2_score(y_test, y_pred)

        temp_m2e = mean_squared_error(y_test, y_pred)

        if temp_value > value:
            print("{}  ----> Method: {}, Score: {:f}, MeanSqError: {}{}".format(c.OKCYAN, type(regr).__name__,
                                                                                temp_value, temp_m2e, c.ENDC))
            value, m2e, meth, best_regr = temp_value, temp_m2e, type(regr).__name__, regr
        else:
            print("  ----> Method: {}, Score: {:f}, MeanSqError: {}".format(type(regr).__name__, temp_value, temp_m2e))

    if meth is None:
        print("No Linear Regressor -> Abort")
        return None

    print("{}  --BEST--> Method: {}, Score: {:f}, MeanSqError: {}{}".format(c.OKGREEN, meth, value, m2e, c.ENDC))
    return {'method': meth, score: value, 'mean_squared_error': m2e}, best_regr


def __poly_linear_regression(x, y, score):
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import PolynomialFeatures

    degree = None
    value = sys.float_info.min
    m2e = sys.float_info.min
    best_regr = None

    print('{}-- Polynomial Regression --{}'.format(c.WARNING, c.ENDC))

    for i in range(2, 11):
        polynomial = PolynomialFeatures(degree=i)
        x_poly = polynomial.fit_transform(x)

        regr = LinearRegression()
        regr.fit(x_poly, y)

        y_pred = regr.predict(x_poly)

        temp_value = 0
        if score == 'r2_score':
            temp_value = r2_score(y, y_pred)
        temp_m2e = mean_squared_error(y, y_pred)

        if temp_value > value:
            print("{} ----> Degree: {}, {}:{}, MeanSqError: {}{}".format(c.OKCYAN, i, score, temp_value, temp_m2e,
                                                                         c.ENDC))
            value, degree, m2e, best_regr = temp_value, i, temp_m2e, regr
        else:
            print("-- Degree: {}, {}:{}, MeanSqError: {}".format(i, score, temp_value, temp_m2e))

    print("{}    --BEST--> Degree: {}, Score: {:f}, MeanSqError: {}{}".format(c.OKGREEN, degree, value, m2e, c.ENDC))

    return {'degree': degree, score: value, 'mean_squared_error': m2e}, best_regr


def __support_vector_regressor(x, y, score):
    from sklearn.svm import SVR
    from sklearn.preprocessing import StandardScaler

    scx = StandardScaler()
    scy = StandardScaler()

    y = y.reshape(len(y), 1)
    x = scx.fit_transform(x)
    y = scy.fit_transform(y)

    kernel_type = ('linear', 'poly', 'rbf', 'sigmoid')

    value = sys.float_info.min
    m2error = 0
    kernel = None
    best_regr = None

    print("{}-- Support Vector Regression -- {}".format(c.WARNING, c.ENDC))
    for el in kernel_type:

        svr = SVR(kernel=el)
        svr.fit(x, y.ravel())
        y_pred = svr.predict(x)

        temp_value = sys.float_info.min
        if score == 'r2_score':
            temp_value = r2_score(y, y_pred)
        temp_m2e = mean_squared_error(y, y_pred)

        if temp_value > value:
            print("{}  ----> Kernel: {}, Score: {:f}, MeanSqError: {}{}".format(c.OKCYAN, el, temp_value,
                                                                                temp_m2e, c.ENDC))
            value, kernel, m2error, best_regr = temp_value, el, temp_m2e, svr
        else:
            print("  ----> Kernel: {}, Score: {:f}, MeanSqError: {}".format(el, temp_value, temp_m2e))

    print("{}    --BEST--> Kernel: {}, {}: {:f}, MeanSqError: {}{}".format(c.OKGREEN, kernel, score, value,
                                                                           m2error, c.ENDC))
    return {'Kernel': kernel, score: value, 'mean_squared_error': m2error}, best_regr


def __decision_tree_regressor(x, y, score):
    from sklearn.tree import DecisionTreeRegressor

    print('{}-- Decision Tree Regressor -- {}'.format(c.OKGREEN, c.ENDC))

    criterion_list = ("mse", "friedman_mse", "mae")

    value = sys.float_info.min
    m2error = 0
    crit = None
    best_regr = None

    for el in criterion_list:
        dtr = DecisionTreeRegressor(criterion=el)
        dtr.fit(x, y)
        y_pred = dtr.predict(x)

        temp_value = sys.float_info.min
        if score == 'r2_score':
            temp_value = r2_score(y, y_pred)
        temp_m2e = mean_squared_error(y, y_pred)

        if temp_value > value:
            print("{}  ----> criterion: {}, Score: {:f}, MeanSqError: {}{}".format(c.OKGREEN, el, temp_value,
                                                                                   temp_m2e, c.ENDC))
            value, crit, m2error, best_regr = temp_value, el, temp_m2e, dtr
        else:
            print("  ----> criterion: {}, Score: {:f}, MeanSqError: {}".format(el, temp_value, temp_m2e))

    print("{}    --BEST--> Criterion: {}, {}: {}, MeanSqErr: {}{}".format(c.OKGREEN, crit, score, value,
                                                                          m2error, c.ENDC))
    return {'criterion': crit, score: value, 'mean_squared_error': m2error}, best_regr


def __random_forest_regressor(x, y, score):
    from sklearn.ensemble import RandomForestRegressor

    value = sys.float_info.min
    m2error = sys.float_info.min
    trees = 0
    best_regr = None

    print('{}-- Random Forest Regressor --{}'.format(c.WARNING, c.ENDC))
    for i in range(200, 1601, 200):
        rfr = RandomForestRegressor(n_estimators=i)
        rfr.fit(x, y)
        y_pred = rfr.predict(x)

        temp_value = sys.float_info.min
        if score == 'r2_score':
            temp_value = r2_score(y, y_pred)
        temp_m2e = mean_squared_error(y, y_pred)

        if temp_value > value:
            print("{}  ----> Trees: {}, {}:{}, MeanSqErr: {}{}".format(c.OKCYAN, i, score, temp_value,
                                                                       temp_m2e, c.ENDC))
            value, m2error, trees, best_regr = temp_value, temp_m2e, i, rfr
        else:
            print("  ----> Trees: {}, {}:{}, MeanSqErr: {}".format(i, score, temp_value, temp_m2e))

    print("{}    --BEST--> Estimators: {}, {}: {:f}, MeanSqError: {}{}".format(c.OKGREEN, trees, score, value,
                                                                               m2error, c.ENDC))
    return {'estimators': trees, score: value, 'mean_squared_error': m2error}, best_regr
