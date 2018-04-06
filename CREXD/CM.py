import nltk
import time
import glob
import shutil

from termcolor import colored
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import kneighbors_graph
from sklearn.metrics.pairwise import cosine_distances
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances

from .Tools import *


class CM:

    def __init__(self, config_file):
        config = dict()
        # Parse the configuration file
        with open(config_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                temp = line.split(sep=':')
                config[temp[0]] = temp[1]
        f.close()

        self.kmeans_init = config['kmeans_init']
        self.kmeans_n_init = config['kmeans_n_init']
        self.kmeans_n_job = config['kmeans_n_job']
        self.kmeans_max_iter = config['kmeans_max_iter']
        self.kmeans_verbose = config['kmeans_verbose']
        self.dbscan_algorithm = config['dbscan_algorithm']
        self.dbscan_leaf_size = config['dbscan_leaf_size']
        self.dbscan_p = config['dbscan_p']

    # Computes the pair-wise distance between all tasks
    def compute_distance_matrix(self, csm_vecs, threshold_=None, binary_=False, dis_='cos'):
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

    # Runs K-means clustering
    def run_kmeans(self, km_vectors, k, km_result_folder, vec_='', km_metric_='euclidean', km_minibatch_=1000):
        model_kmeans = None

        if km_metric_ == 'euclidean':
            if km_minibatch_ > 0:
                model_kmeans = self.run_mb_kmeans(km_vectors, k, km_result_folder, km_minibatch_, vec_=vec_)
            else:
                model_kmeans = KMeans(n_clusters=k, init=self.kmeans_init, verbose=self.kmeans_verbose,
                                      max_iter=self.kmeans_max_iter, n_init=self.kmeans_n_init,
                                      n_jobs=self.kmeans_n_job)
                model_kmeans.fit(km_vectors)
                joblib.dump(model_kmeans,
                            km_result_folder + '/kmeans_' + vec_ + '_model_' + str(len(km_vectors)) + '_' + str(k),
                            compress=1)

        if km_metric_ == 'cosine':
            model_kmeans = self.run_spherical_kmeans(km_vectors, k, km_result_folder, vec_=vec_)

        return model_kmeans

    # Runs multiple instances of K-means clustering in parallel
    def run_kmeans_p(self, args):
        return self.run_kmeans(*args)

    # Runs K-means clustering with minibatch to handle a large amount of data
    def run_mb_kmeans(self, km_vectors, k, km_result_folder, km_batch_size_, vec_):
        model_kmeans = MiniBatchKMeans(n_clusters=k, init='k-means++', max_iter=2000, n_init=20,
                                       batch_size=km_batch_size_,
                                       max_no_improvement=None)
        model_kmeans.fit(km_vectors)
        joblib.dump(model_kmeans,
                    km_result_folder + '/kmeans_' + vec_ + '_model_' + str(len(km_vectors)) + '_' + str(k),
                    compress=1)
        return model_kmeans

    # Runs multiple instances of K-means clustering with minibatch in parallel
    def run_mb_kmeans_p(self, args):
        return self.run_mb_kmeans(*args)

    # Runs spherical K-means clustering (to support cosine distance)
    def run_spherical_kmeans(self, ckm_vectors, ckm_k, ckm_result_folder, vec_):
        clusterer = nltk.cluster.KMeansClusterer(ckm_k, nltk.cluster.cosine_distance, repeats=10,
                                                 avoid_empty_clusters=True)
        clusters = clusterer.cluster(ckm_vectors, True)
        model_kmeans = dict()
        model_kmeans['n_clusters_'] = clusterer.num_clusters()
        model_kmeans['labels_'] = clusters
        joblib.dump(model_kmeans,
                    ckm_result_folder + '/kmeans_' + vec_ + '_model_' + str(len(ckm_vectors)) + '_' + str(ckm_k),
                    compress=1)

        return model_kmeans

    # Runs DBSCAN clustering
    def run_dbscan(self, db_vectors, db_eps, db_min_sample, db_result_folder, vec_='', metric_='euclidean', stats_=False):
        model_dbscan = DBSCAN(eps=db_eps, min_samples=db_min_sample, leaf_size=None, n_jobs=1, algorithm='brute',
                              metric=metric_)

        if metric_ == 'precomputed':
            precom_mat = self.compute_distance_matrix(db_vectors, dis_='cos')
            # print(random.sample(list(precom_mat.flatten()), 500))
            model_dbscan.fit(precom_mat)

        else:
            model_dbscan.fit(db_vectors)

        k = len(set(model_dbscan.labels_)) - (1 if -1 in model_dbscan.labels_ else 0)
        un = [1 if i == -1 else 0 for i in model_dbscan.labels_]

        joblib.dump(model_dbscan,
                    db_result_folder + '/dbscan_' + vec_ + '_model_' + str(db_eps) + '_' + str(db_min_sample),
                    compress=1)

        # print(db_eps, db_min_sample, k, sum(un), '\t ... \t')

        if stats_:
            stats = [db_eps, db_min_sample, k, sum(un)]
            # print(db_eps, db_min_sample, k, sum(un), '\t ... \t', end='')

        return model_dbscan

    # Runs multiple instances of  DBSCAN clustering in parallel
    def run_dbscan_p(self, args):
        return self.run_dbscan(*args)

    # Runs agglomerative clustering
    def run_agglomerative(self, ag_vectors, k, ag_linkage, ag_result_folder, vec_='', metric_='euclidean'):
        # t0 = time.time()
        # TODO: this
        knn_graph = kneighbors_graph(ag_vectors, 30, include_self=False)
        model_agg = AgglomerativeClustering(linkage=ag_linkage, n_clusters=k, connectivity=None, affinity=metric_)
        model_agg.fit(ag_vectors)
        joblib.dump(model_agg, ag_result_folder + '/agg_' + vec_ + '_model_' + str(k) + '_' + ag_linkage, compress=1)
        # print(k, time.time() - t0)
        # print(model_agg.labels_)
        # print(model_agg.children_)
        # ii = itertools.count(ag_vectors.shape[0])
        # a = [{'node_id': next(ii), 'left': x[0], 'right': x[1]} for x in model_agg.children_]
        # print(a)
        return model_agg

    # Runs multiple instances of  agglomerative clustering in parallel
    def run_agglomerative_p(self, args):
        return self.run_agglomerative(*args)

    # Run the clustering module
    def run_cm(self, conf, vec_tfidf, vec_doc2vec):
        # load configurations
        r_metric_ = conf['r_metric_']
        r_kmeans_k_ = conf['r_kmeans_k_']
        r_minibatch_ = conf['r_minibatch_']
        r_agg_k_linkage_ = conf['r_agg_k_linkage_']
        r_dbscan_eps_minpts_ = conf['r_dbscan_eps_minpts_']
        output_result_folder = conf['output_result_folder']
        r_preprocessed_location = conf['r_preprocessed_location']
        r_n_clustering_processes = conf['r_n_clustering_processes']

        # if clustering models are pre-trained
        if conf['process'] == 'copy':
            print(colored('Pre-processed, pre-vecotrized and pre-clustered', 'green'))

            r_models_to_load = []

            if 'kmeans_tfidf' in conf:
                r_models_to_load.append('kmeans_tfidf')

            if 'dbscan_tfidf' in conf:
                r_models_to_load.append('dbscan_tfidf')

            if 'agg_tfidf' in conf:
                r_models_to_load.append('agg_tfidf')

            if 'kmeans_doc2vec' in conf:
                r_models_to_load.append('kmeans_doc2vec')

            if 'dbscan_doc2vec' in conf:
                r_models_to_load.append('dbscan_doc2vec')

            if 'agg_doc2vec' in conf:
                r_models_to_load.append('agg_doc2vec')

            # copy the preprocessed models to the current run dir : to keep track of what data/models was used in each run
            for r_model_to_load in r_models_to_load:
                for name in glob.glob(r_preprocessed_location + '/' + r_model_to_load + '_model_*'):
                    shutil.copy(name, output_result_folder)

            shutil.copy(r_preprocessed_location + '/run_configuration_reduced', output_result_folder)

        # if clustering models need to be trained
        if conf['process'] == 'train':
            print(colored('Clustering', 'green'))

            # for each clustering/vectorizing combination:
            # 1- load the relevant vectorized data
            # 2- Build the configuration list (if parallel) or loop over the configurations (if sequential)
            # 3- Run the relevant clustering algorithm

            if r_n_clustering_processes > 1:
                if len(vec_doc2vec) == 0:
                    print('\t kmeans_doc2vec: No vectors to cluster: Skipped')
                else:
                    if 'kmeans_tfidf' in conf:
                        print('\t kmeans_tfidf \t ... \t', end='', flush=True)
                        job_args = [(vec_tfidf, config, output_result_folder, 'tfidf', r_metric_, r_minibatch_) for
                                    config in
                                    r_kmeans_k_]
                        p = Pool(processes=r_n_clustering_processes)
                        t0 = time.time()
                        list(p.map(self.run_kmeans_p, job_args))
                        t1 = time.time()
                        print(round(t1 - t0, 6), 'sec \t ... \t', end='')
                        p.close()

                    if 'dbscan_tfidf' in conf:
                        print('\t dbscan_tfidf \t ... \t', end='', flush=True)
                        job_args = [(vec_tfidf, config[0], config[1], output_result_folder, 'tfidf', r_metric_) for
                                    config in
                                    r_dbscan_eps_minpts_]
                        p = Pool(processes=r_n_clustering_processes)
                        t0 = time.time()
                        list(p.map(self.run_dbscan_p, job_args))
                        t1 = time.time()
                        print(round(t1 - t0, 6), 'sec \t ... \t', end='')
                        p.close()

                    if 'agg_tfidf' in conf:
                        print('\t agg_tfidf \t ... \t', end='', flush=True)
                        job_args = [(vec_tfidf, config[0], config[1], output_result_folder, 'tfidf', r_metric_) for
                                    config in
                                    r_agg_k_linkage_]
                        p = Pool(processes=r_n_clustering_processes)
                        t0 = time.time()
                        list(p.map(self.run_agglomerative_p, job_args))
                        t1 = time.time()
                        print(round(t1 - t0, 6), 'sec \t ... \t', end='')
                        p.close()

                if len(vec_doc2vec) == 0:
                    print('\t kmeans_doc2vec: No vectors to cluster: Skipped')
                else:
                    if 'kmeans_doc2vec' in conf:
                        print('\t kmeans_doc2vec\t ... \t', end='', flush=True)
                        job_args = [(vec_doc2vec, config, output_result_folder, 'doc2vec', r_metric_, r_minibatch_) for
                                    config
                                    in r_kmeans_k_]
                        p = Pool(processes=r_n_clustering_processes)
                        t0 = time.time()
                        list(p.map(self.run_kmeans_p, job_args))
                        t1 = time.time()
                        print(round(t1 - t0, 6), 'sec \t ... \t', end='')
                        p.close()

                    if 'dbscan_doc2vec' in conf:
                        print('\t dbscan_doc2vec\t ... \t', end='', flush=True)
                        job_args = [(vec_doc2vec, config[0], config[1], output_result_folder, 'doc2vec', r_metric_) for
                                    config
                                    in r_dbscan_eps_minpts_]
                        p = Pool(processes=r_n_clustering_processes)
                        t0 = time.time()
                        list(p.map(self.run_dbscan_p, job_args))
                        t1 = time.time()
                        print(round(t1 - t0, 6), 'sec \t ... \t', end='')
                        p.close()

                    if 'agg_doc2vec' in conf:
                        print('\t agg_doc2vec \t ... \t', end='', flush=True)
                        job_args = [(vec_doc2vec, config[0], config[1], output_result_folder, 'doc2vec', r_metric_) for
                                    config
                                    in r_agg_k_linkage_]
                        p = Pool(processes=r_n_clustering_processes)
                        t0 = time.time()
                        list(p.map(self.run_agglomerative_p, job_args))
                        t1 = time.time()
                        print(round(t1 - t0, 6), 'sec \t ... \t', end='')
                        p.close()

            else:
                if len(vec_tfidf) == 0:
                    print('\t kmeans_doc2vec: No vectors to cluster: Skipped')
                else:
                    if 'kmeans_tfidf' in conf:
                        print('\t kmeans_tfidf \t ... \t', end='', flush=True)
                        t0 = time.time()
                        for config in r_kmeans_k_:
                            self.run_kmeans(vec_tfidf, config, output_result_folder, vec_='tfidf', km_metric_=r_metric_,
                                            km_minibatch_=r_minibatch_)
                        t1 = time.time()
                        print(round(t1 - t0, 6), 'sec \t ... \t', end='')
                        print('Done')

                    if 'dbscan_tfidf' in conf:
                        print('\t dbscan_tfidf \t ... \t', end='')
                        t0 = time.time()
                        for config in r_dbscan_eps_minpts_:
                            self.run_dbscan(vec_tfidf, config[0], config[1], output_result_folder, vec_='tfidf',
                                            metric_=r_metric_)
                        t1 = time.time()
                        print(round(t1 - t0, 6), 'sec \t ... \t', end='')
                        print('Done')

                    if 'agg_tfidf' in conf:
                        print('\t agg_tfidf \t\t ... \t', end='')
                        t0 = time.time()
                        for config in r_agg_k_linkage_:
                            self.run_agglomerative(vec_tfidf, config[0], config[1], output_result_folder, vec_='tfidf',
                                                   metric_=r_metric_)
                        t1 = time.time()
                        print(round(t1 - t0, 6), 'sec \t ... \t', end='')
                        print('Done')

                if len(vec_doc2vec) == 0:
                    print('\t kmeans_doc2vec: No vectors to cluster: Skipped')
                else:
                    if 'kmeans_doc2vec' in conf:
                        print('\t kmeans_doc2vec\t ... \t', end='')
                        t0 = time.time()

                        for config in r_kmeans_k_:
                            self.run_kmeans(vec_doc2vec, config, output_result_folder, vec_='doc2vec',
                                            km_metric_=r_metric_,
                                            km_minibatch_=r_minibatch_)
                        t1 = time.time()
                        print(round(t1 - t0, 6), 'sec \t ... \t', end='')
                        print('Done')

                    if 'dbscan_doc2vec' in conf:
                        print('\t dbscan_doc2vec\t ... \t', end='')
                        t0 = time.time()
                        for config in r_dbscan_eps_minpts_:
                            self.run_dbscan(vec_doc2vec, config[0], config[1], output_result_folder, vec_='doc2vec',
                                            metric_=r_metric_)
                        t1 = time.time()
                        print(round(t1 - t0, 6), 'sec \t ... \t', end='')
                        print('Done')

                    if 'agg_doc2vec' in conf:
                        print('\t agg_doc2vec \t ... \t', end='')
                        t0 = time.time()
                        for config in r_agg_k_linkage_:
                            self.run_agglomerative(vec_doc2vec, config[0], config[1], output_result_folder,
                                                   vec_='doc2vec',
                                                   metric_=r_metric_)
                        t1 = time.time()
                        print(round(t1 - t0, 6), 'sec \t ... \t', end='')
                        print('Done')
