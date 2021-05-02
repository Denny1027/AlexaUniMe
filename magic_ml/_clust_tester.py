import sys
from ._utils import bcolors as c
from matplotlib import pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans


def _cluster_tester_controller(x, max_clusters=10, elbow_graph=False, bidim_graph=False):

    wcss = []
    sil_list = []
    best_sil = sys.float_info.min
    best_kmeans = None
    predict_list = None

    for i in range(2, max_clusters+1):
        #kmeans
        kmeans_model = KMeans(n_clusters=i, random_state=0)
        fitted_kmeans = kmeans_model.fit(x)
        labels = fitted_kmeans.labels_

        temp_sil = silhouette_score(x, labels, metric='euclidean')
        sil_list.append(temp_sil)
        wcss.append(kmeans_model.inertia_)

        if temp_sil > best_sil:
            best_sil, best_kmeans, predict_list = temp_sil, kmeans_model, kmeans_model.fit_predict(x)

    result_list = sorted(range(len(sil_list)), key=lambda k: sil_list[k])
    result_list.reverse()

    print("{}---- K-MEANS BEST N of NEIGHBOOR -----".format(c.OKGREEN))
    print("BEST 3 RESULT ---> {} {}{}".format(c.HEADER, [x+2 for x in result_list][:3], c.ENDC))

    if elbow_graph:
        if x.shape[1] == 2:
            plt.plot(range(2, max_clusters+1), wcss)
            plt.xlabel("Cluster number")
            plt.ylabel("WCSS")
            plt.title("Elbow Method")
            plt.show()
        else:
            print("{} Elbow graph: Only 2 dimension x set {}".format(c.FAIL, c.ENDC))

    if bidim_graph:
        if x.shape[1] == 2:
            for i in range(result_list[0]+2):
                plt.scatter(x[predict_list == i, 0], x[predict_list == i, 1], s=100, label=('Cluster ', i + 1))
            plt.scatter(best_kmeans.cluster_centers_[:, 0], best_kmeans.cluster_centers_[:, 1], s=300, c='yellow',
                        label='Centroids')
            plt.legend()
            plt.show()
        else:
            print("{} 2D graph: Only 2 dimension x set {}".format(c.FAIL, c.ENDC))

    return best_kmeans, predict_list
