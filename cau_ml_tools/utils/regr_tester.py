import sys
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error


def __simple_linear_regression(x, y, score, test_size):
    from sklearn.linear_model import RidgeCV, LassoCV, ElasticNetCV

    print("        -- Simple Linear Regression --")

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
            print("  [B]--> Method: {}, Score: {:f}, MeanSqError: {}".format(type(regr).__name__,
                                                                             temp_value, temp_m2e))
            value, m2e, meth, best_regr = temp_value, temp_m2e, type(regr).__name__, regr
        else:
            print("  ----> Method: {}, Score: {:f}, MeanSqError: {}".format(type(regr).__name__, temp_value, temp_m2e))

    if meth is None:
        print("No Linear Regressor -> Abort")
        return None

    print("  --BEST--> Method: {}, Score: {:f}, MeanSqError: {}\n".format(meth, value, m2e))
    return {'method': meth, score: value, 'mean_squared_error': m2e}, best_regr


def __poly_linear_regression(x, y, score):
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import PolynomialFeatures

    degree = None
    value = sys.float_info.min
    m2e = sys.float_info.min
    best_regr = None

    print("        -- Polynomial Regression --")

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
            print(" [B]--> Degree: {}, {}:{}, MeanSqError: {}".format(i, score, temp_value, temp_m2e))
            value, degree, m2e, best_regr = temp_value, i, temp_m2e, regr
        else:
            print(" -----> Degree: {}, {}:{}, MeanSqError: {}".format(i, score, temp_value, temp_m2e))

    print("     --BEST--> Degree: {}, Score: {:f}, MeanSqError: {}\n".format(degree, value, m2e))

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

    print("        -- Support Vector Regression --")
    for el in kernel_type:

        svr = SVR(kernel=el)
        svr.fit(x, y.ravel())
        y_pred = svr.predict(x)

        temp_value = sys.float_info.min
        if score == 'r2_score':
            temp_value = r2_score(y, y_pred)
        temp_m2e = mean_squared_error(y, y_pred)

        if temp_value > value:
            print(" [B]--> Kernel: {}, Score: {:f}, MeanSqError: {}".format(el, temp_value, temp_m2e))
            value, kernel, m2error, best_regr = temp_value, el, temp_m2e, svr
        else:
            print("  ----> Kernel: {}, Score: {:f}, MeanSqError: {}".format(el, temp_value, temp_m2e))

    print("     --BEST--> Kernel: {}, {}: {:f}, MeanSqError: {}\n".format(kernel, score, value, m2error))
    return {'Kernel': kernel, score: value, 'mean_squared_error': m2error}, best_regr


def __decision_tree_regressor(x, y, score):
    from sklearn.tree import DecisionTreeRegressor

    print("        -- Decision Tree Regressor --")

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
            print(" [B]--> criterion: {}, Score: {:f}, MeanSqError: {}".format(el, temp_value, temp_m2e))
            value, crit, m2error, best_regr = temp_value, el, temp_m2e, dtr
        else:
            print(" ----> criterion: {}, Score: {:f}, MeanSqError: {}".format(el, temp_value, temp_m2e))

    print("     --BEST--> Criterion: {}, {}: {}, MeanSqErr: {}\n".format(crit, score, value, m2error))
    return {'criterion': crit, score: value, 'mean_squared_error': m2error}, best_regr


def __random_forest_regressor(x, y, score):
    from sklearn.ensemble import RandomForestRegressor

    value = sys.float_info.min
    m2error = sys.float_info.min
    trees = 0
    best_regr = None

    print("        -- Random Forest Regressor --")
    for i in range(200, 2001, 200):
        rfr = RandomForestRegressor(n_estimators=i)
        rfr.fit(x, y)
        y_pred = rfr.predict(x)

        temp_value = sys.float_info.min
        if score == 'r2_score':
            temp_value = r2_score(y, y_pred)
        temp_m2e = mean_squared_error(y, y_pred)

        if temp_value > value:
            print(" [B]--> Trees: {}, {}:{}, MeanSqErr: {}".format(i, score, temp_value, temp_m2e))
            value, m2error, trees, best_regr = temp_value, temp_m2e, i, rfr
        else:
            print(" ----> Trees: {}, {}:{}, MeanSqErr: {}".format(i, score, temp_value, temp_m2e))

    print("     --BEST--> Estimators: {}, {}: {:f}, MeanSqError: {}\n".format(trees, score, value, m2error))
    return {'estimators': trees, score: value, 'mean_squared_error': m2error}, best_regr
