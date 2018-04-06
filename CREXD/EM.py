import time
import glob
import warnings
import matplotlib.cm as cm

from termcolor import colored
from collections import Counter
from scipy.stats import pearsonr
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.metrics import silhouette_samples
from sklearn.metrics.pairwise import cosine_distances
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances

from .Tools import *


# Returns the list of tasks contained in a given cluster
def fetch_cluster_content(fcc_clustering_model, fcc_clustering_vectors, fcc_task_ids, fcc_name, fcc_stats_=True):
    if isinstance(fcc_clustering_model, dict):
        labels_ = fcc_clustering_model['labels_']
    else:
        labels_ = fcc_clustering_model.labels_

    categories_ = np.unique(labels_)
    vectors_labels_ = list(zip(fcc_clustering_vectors, labels_))
    vectors_labels_ids_ = list(zip(fcc_task_ids, labels_))
    clusters_ = {}

    for cat_ in categories_:
        temp_ = []
        for vec_ in vectors_labels_ids_:
            if vec_[1] == cat_:
                temp_.append(vec_[0])
        clusters_[cat_] = temp_

    for i in categories_:
        np.random.shuffle(clusters_[i])

    # print("'" + fcc_name + "' : [", end="")

    # print(fcc_name)
    if fcc_stats_:
        clusters_stat_ = {}
        for cat_ in categories_:
            temp_ = []
            for vec_ in vectors_labels_:
                if vec_[1] == cat_:
                    temp_.append(vec_[0])
            clusters_stat_[cat_] = temp_

        for cat_ in categories_:
            ind = [str(el) for el in clusters_stat_[cat_]]
            cat_temp = Counter(ind).keys()
            cat_temp1 = Counter(ind).values()
            s = list(zip(cat_temp, cat_temp1))
            # print(s)

    return clusters_


# Compare the similarity between 2 clusterings
def compare_clustering_results(ccr_vecs, ccr_clustering_1, ccr_clustering_2):
    occ_1 = compute_occurence_matrix(ccr_vecs, ccr_clustering_1)
    occ_2 = compute_occurence_matrix(ccr_vecs, ccr_clustering_2)
    corr_ = compute_correlation(occ_1, occ_2)[1][0]

    return corr_


# Computes the pair-wise distance between all tasks
def compute_distance_matrix(csm_vecs, threshold_=None, binary_=False, dis_='cos'):
    csm_matrix_b = np.zeros((len(csm_vecs), len(csm_vecs)))
    csm_matrix_r = []
    if dis_ == 'cos':
        csm_matrix_r = cosine_distances(csm_vecs, csm_vecs)

    if dis_ == 'euc':
        csm_matrix_r = euclidean_distances(csm_vecs, csm_vecs)

    if dis_ == 'cos_sim':
        csm_matrix_r = cosine_similarity(csm_vecs, csm_vecs)

    if binary_:
        for csm_vec_1 in range(len(csm_vecs)):
            for csm_vec_2 in range(len(csm_vecs)):
                temp_ = csm_matrix_r[csm_vec_1][csm_vec_2]
                csm_matrix_b[csm_vec_1][csm_vec_2] = 1 if temp_ > threshold_ else 0
        print(csm_matrix_b)
        return csm_matrix_b

    else:
        return csm_matrix_r


# Computes the occurence matrix of a clustered set of tasks i.e. does a pair of tasks belong to the same cluster or not
def compute_occurence_matrix(com_vecs, com_clustering_model):
    com_clustering_model_labels = com_clustering_model.labels_
    com_matrix = np.zeros((len(com_vecs), len(com_vecs)))

    for com_vec_1 in range(len(com_vecs)):
        for com_vec_2 in range(com_vec_1, len(com_vecs)):
            com_matrix[com_vec_1][com_vec_2] = 1 if com_clustering_model_labels[com_vec_1] == \
                                                    com_clustering_model_labels[com_vec_2] else 0

    return com_matrix


# Computes the Personr correlation between the occurence and similarity/distance matrix
def compute_correlation(ec_similarity, ec_occurence):
    ec_o = ec_occurence.flatten()
    ec_s = ec_similarity.flatten()

    res1 = np.corrcoef(ec_s, ec_o)
    res2 = pearsonr(ec_s, ec_o)

    return res1, res2


# Computes and plots a set of silhouette measures to evaluate the clustering model
# (original code from: http://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html)
def silhouette_study(ss_vecs_file, ss_models_files, ss_result_folder, m):
    ss_vecs = joblib.load(ss_vecs_file)
    ss_models = [joblib.load(ss_models_file) for ss_models_file in ss_models_files]
    sizes = []
    for ss_model in ss_models:
        n_clusters = len(np.unique(ss_model.labels_))

        # Create a subplot with 1 row and 2 columns
        fig, ax1 = plt.subplots(1, 1)
        fig.set_size_inches(18, 7)

        # The 1st subplot is the silhouette plot
        # The silhouette coefficient can range from -1, 1 but in this example all
        # lie within [-0.1, 1]
        ax1.set_xlim([-0.3, 1])
        # The (n_clusters+1)*10 is for inserting blank space between silhouette
        # plots of individual clusters, to demarcate them clearly.
        ax1.set_ylim([0, len(ss_vecs) + (n_clusters + 1) * 20])

        # Initialize the clusterer with n_clusters value and a random generator
        # seed of 10 for reproducibility.
        cluster_labels = ss_model.predict(ss_vecs)

        # The silhouette_score gives the average value for all the samples.
        # This gives a perspective into the density and separation of the formed
        # clusters
        silhouette_avg = silhouette_score(ss_vecs, cluster_labels)
        print("For n_clusters =", n_clusters,
              "The average silhouette_score is :", silhouette_avg)

        # Compute the silhouette scores for each sample
        sample_silhouette_values = silhouette_samples(ss_vecs, cluster_labels)

        y_lower = 10
        for i in range(n_clusters):
            # Aggregate the silhouette scores for samples belonging to
            # cluster i, and sort them
            ith_cluster_silhouette_values = \
                sample_silhouette_values[cluster_labels == i]

            ith_cluster_silhouette_values.sort()

            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            sizes.append(size_cluster_i)
            y_upper = y_lower + size_cluster_i

            color = cm.spectral(float(i) / n_clusters)
            ax1.fill_betweenx(np.arange(y_lower, y_upper),
                              0, ith_cluster_silhouette_values,
                              facecolor=color, edgecolor=color, alpha=0.7)

            # Label the silhouette plots with their cluster numbers at the middle
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

            # Compute the new y_lower for next plot
            y_lower = y_upper + 10  # 10 for the 0 samples

        ax1.set_title("The silhouette plot for the various clusters.")
        ax1.set_xlabel("The silhouette coefficient values")
        ax1.set_ylabel("Cluster label")

        # The vertical line for average silhouette score of all the values
        ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

        ax1.set_yticks([])  # Clear the yaxis labels / ticks
        ax1.set_xticks([-0.2, -0.3, -0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

        plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
                      "with n_clusters = %d" % n_clusters),
                     fontsize=14, fontweight='bold')

        plt.savefig(ss_result_folder + str(n_clusters) + m + '.png')


# Computes the following quality measures silhouette, correlation matrix, homogeneity, completeness and v-measure
def validity_measure(vm_vecs, vm_model, vm_true_labels, measures=None):
    if measures is None:
        measures = ['hcv']

    k = 0
    labels = None

    if isinstance(vm_model, KMeans) or isinstance(vm_model, AgglomerativeClustering):
        k = vm_model.n_clusters
        labels = vm_model.labels_

    if isinstance(vm_model, dict):
        k = vm_model['n_clusters_']
        labels = vm_model['labels_']

    if isinstance(vm_model, DBSCAN):
        k = len(set(vm_model.labels_)) - (1 if -1 in vm_model.labels_ else 0)
        labels = vm_model.labels_

    sil_c = None
    sil_e = None
    corr_c = None
    corr_e = None
    homog = None
    compl = None
    vmeas = None

    if k > 1:
        ran_seed = random.randint(1, 1000)

        if 'sil' in measures:
            sil_c = metrics.silhouette_score(vm_vecs, labels, sample_size=10000, random_state=ran_seed, metric='cosine')
            sil_e = metrics.silhouette_score(vm_vecs, labels, sample_size=10000, random_state=ran_seed,
                                             metric='euclidean')

        if 'coc' in measures:
            sim_c = compute_distance_matrix(vm_vecs, binary_=False, dis_='cos')
            sim_e = compute_distance_matrix(vm_vecs, binary_=False, dis_='euc')
            occ = compute_occurence_matrix(vm_vecs, vm_model)
            corr_c = compute_correlation(sim_c, occ)[1][0]
            corr_e = compute_correlation(sim_e, occ)[1][0]

        if 'hcv' in measures:
            homog = metrics.homogeneity_score(vm_true_labels, labels)
            compl = metrics.completeness_score(vm_true_labels, labels)
            vmeas = metrics.v_measure_score(vm_true_labels, labels)

    return [k, sil_c, sil_e, corr_c, corr_e, homog, compl, vmeas]


# A parallel call of the validity_measure() function
def validity_measure_p(args):
    return validity_measure(*args)


# The vectorizing/clustering evaluation function
def evaluate(e_result_folder, e_clustering_models_, e_clustering_vecs_, e_name, e_configuration, e_true_labels_,
             e_task_ids, write_=True, print_=False, n_jobs=1, e_measures_=None):
    assert (n_jobs > 0)

    # Create list to append inividual results
    e_res_f = []

    if n_jobs == 1:
        # load data and evaluate
        for e_model in e_clustering_models_:
            e_res_ = validity_measure(e_clustering_vecs_, e_model, e_true_labels_, e_measures_)
            e_res_f.append(e_res_)
    else:
        e_pool = Pool(processes=n_jobs)
        agrs = [(e_clustering_vecs_, e_clustering_model_, e_true_labels_, e_measures_) for e_clustering_model_ in
                e_clustering_models_]
        e_res_f = list(e_pool.map(validity_measure_p, agrs))
        e_pool.close()

    # Create file to log results
    f = open(e_result_folder + 'eval_' + e_name + '_' + str(e_configuration['sample_size']) + '_' + str(
        round(time.time())) + '.txt', 'a')

    f.write('Combination : ' + e_name + '\n')
    f.write('Sample size : ' + str(e_configuration['sample_size']) + '\n')

    f.write('doc2vec - window size : ' + str(e_configuration['doc2vec_window_size']) + '\n')
    f.write('doc2vec - vector size : ' + str(e_configuration['doc2vec_vector_size']) + '\n')
    f.write('tfidf - vector size : ' + str(e_configuration['tfidf_vector_size']) + '\n')

    f.write('k sil_c sil_e corr_c corr_e homog compl vmeas' + '\n')

    print('\t' + e_name + ' \t ... \t', end='')

    if print_:
        print('\n')

    for e_res_i in e_res_f:
        if print_:
            print(str(e_res_i[0]) + ' ' + str(e_res_i[1]) + ' ' + str(e_res_i[2]) + ' ' + str(e_res_i[3]) + ' ' + str(
                e_res_i[4]) + ' ' + str(e_res_i[5]) + ' ' + str(e_res_i[6]) + ' ' + str(e_res_i[7]))
        if write_:
            f.write(str(e_res_i[0]) + ' ' + str(e_res_i[1]) + ' ' + str(e_res_i[2]) + ' ' + str(e_res_i[3]) + ' ' + str(
                e_res_i[4]) + ' ' + str(e_res_i[5]) + ' ' + str(e_res_i[6]) + ' ' + str(e_res_i[7]) + '\n')

    return e_res_f


# Run the evaluation module
def run_em(conf):
    print(colored('Evaluating', 'green'))

    # load configurations
    measures = conf['measures']
    vectorizing_models = conf['vectorizing_models']
    clustering_models = conf['clustering_models']
    output_result_folder = conf['output_result_folder']
    n_evaluation_processes = conf['n_evaluation_processes']
    re_conf = joblib.load(output_result_folder + '/run_configuration_reduced')
    doc_sample_sizes = re_conf['sample_size']

    # warn for empty clustering model choice
    if len(clustering_models) == 0:
        warnings.warn('Choose the clustering model(s) to evaluate')
        return 1

    # warn for empty vectorizing model choice
    if len(vectorizing_models) == 0:
        warnings.warn('Choose the vectorizing model(s) to evaluate')
        return 1

    # Evaluate the results
    for vec_model in vectorizing_models:
        for clu_model in clustering_models:

            # Load the used models
            re_name = clu_model + '_' + vec_model
            re_models_file_names = glob.glob(output_result_folder + '/' + re_name + '_model_*')
            re_models_file_names.sort()  # help getting sorted evaluation lost : unnecessary
            try:
                re_models = [joblib.load(re_models_file) for re_models_file in re_models_file_names]
            except FileNotFoundError:
                print("\t No models file for " + vec_model + " was found : Skipped")

            # Load the data vectors
            try:
                re_vecs = joblib.load(output_result_folder + '/' + vec_model + '_sample_vecs_' + str(doc_sample_sizes))
            except FileNotFoundError:
                print("\t No vector file for " + vec_model + " was found : Skipped")

            # Load the true labeled data (many data sets are used to build the corpus, they are used as true labels)
            try:
                re_true_raw = joblib.load(
                    output_result_folder + '/' + vec_model + '_sample_dict_' + str(doc_sample_sizes))
            except FileNotFoundError:
                print("\t No vector file for " + vec_model + " was found : Skipped")

            # Fetching just the labels
            re_true_labels = [index[1][0].split('_')[0] for index in re_true_raw]

            re_tasks_ids = [index[1][0] for index in re_true_raw]

            # Evaluate
            t0 = time.time()
            if len(re_true_raw) == 0 or len(re_models) or len(re_vecs) == 0:
                print("\t No clustering was found for the selected models: Evaluation Skipped")
            else:
                evaluate(e_result_folder=output_result_folder, e_clustering_models_=re_models,
                         e_clustering_vecs_=re_vecs,
                         e_name=re_name, e_true_labels_=re_true_labels, e_task_ids=re_tasks_ids,
                         e_configuration=re_conf, n_jobs=n_evaluation_processes, print_=False, e_measures_=measures)

            t1 = time.time()
            print(t1 - t0, '\t ... \t', end='')
            print('Done')

    return 0
