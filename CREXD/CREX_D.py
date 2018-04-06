import sys
import socket
import calendar
import datetime
import itertools

from CREXD.VM import *
from CREXD.CM import *
from CREXD.SM import *
from CREXD.EM import *


class Tee(object):
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)

    def flush(self):
        pass


def vectorize_cluster_sample_evaluate(r_cluster_, r_evaluate_, r_sample_, r_sample_size, r_doc2vec_window_size,
                                      r_doc2vec_vector_size, r_tfidf_vector_size, r_clustering_vectorizing_combs,
                                      r_kmeans_k_, r_minibatch_, r_dbscan_eps_minpts_, r_agg_k_linkage_, r_metric_,
                                      r_n_clustering_processes, r_preprocess_, r_preprocess_tfidf, r_preprocess_doc2vec,
                                      r_vectorize_, r_different_custering_data, r_preprocessed_location, r_pca_,
                                      r_pca_vs_, r_n_evaluation_processes, r_eva_vectorizing_models,
                                      r_eva_clustering_models, r_eva_measures, r_fitness_, r_max_sample_size_,
                                      r_min_samples_per_cluster_, r_max_sampling_iteration_, r_output_result_folder,
                                      r_tokenized_data_folder, r_vectorized_data_folder, r_raw_clustering_data_folder,
                                      r_raw_data_folder, r_more_config):
    assert (any(x in r_clustering_vectorizing_combs for x in ['kmeans_tfidf', 'dbscan_tfidf', 'agg_tfidf',
                                                              'kmeans_doc2vec', 'dbscan_doc2vec', 'agg_doc2vec']))

    if not r_cluster_ and (r_preprocess_ or r_vectorize_):
        warnings.warn("Possible data inconsistency in the run folder: clustering models might not be trained on the "
                      "vectorized vectors found in the folder\nCause: cluster_= False and Preprcess_/vectorize_= True")

    # ------------------------------------------------------------------------------
    # VECTORIZE - TRAIN
    # ------------------------------------------------------------------------------

    # log start time
    t_before_load_train = time.time()

    # configure vectorizing
    vectorizing_config = dict()
    vectorizing_config['raw_data_folder'] = r_raw_data_folder
    vectorizing_config['output_result_folder'] = r_output_result_folder
    vectorizing_config['r_preprocessed_location'] = r_preprocessed_location
    vectorizing_config['vectorized_data_folder'] = r_vectorized_data_folder
    vectorizing_config['tokenized_data_folder'] = r_tokenized_data_folder
    vectorizing_config['r_tfidf_vector_size'] = r_tfidf_vector_size
    vectorizing_config['r_doc2vec_window_size'] = r_doc2vec_window_size
    vectorizing_config['r_doc2vec_vector_size'] = r_doc2vec_vector_size

    # check which vectorizers need to be trained/loaded
    vectorizing_config['tfidf'] = 'train' if r_preprocess_tfidf and r_preprocess_ else 'copy'
    vectorizing_config['doc2vec'] = 'train' if r_preprocess_doc2vec and r_preprocess_ else 'copy'
    vectorizing_config['tfidf_vectorize'] = 'vectorize' if r_preprocess_tfidf and r_vectorize_ else 'copy'
    vectorizing_config['doc2vec_vectorize'] = 'vectorize' if r_preprocess_doc2vec and r_vectorize_ else 'copy'

    # if vectorizers are not pre-trained then configure VM to train else configure VM to load pre-trained vectorizers
    vectorizing_config['process'] = 'train' if r_preprocess_ else 'copy'

    # warn about useless training
    if r_preprocess_tfidf:
        if not any(x in r_clustering_vectorizing_combs for x in ['kmeans_tfidf', 'dbscan_tfidf', 'agg_tfidf']):
            warnings.warn("No clustering combination requiring TFIDF was found in your configuration, useless train!")
            vectorizing_config['doc2vec'] = 'skip'
    else:
        vectorizing_config['tfidf_vectorize'] = 'skip'

    if r_preprocess_doc2vec:
        if not any(x in r_clustering_vectorizing_combs for x in ['kmeans_doc2vec', 'dbscan_doc2vec', 'agg_doc2vec']):
            warnings.warn("No clustering combination requiring Doc2vec was found in your configuration, useless train!")
            vectorizing_config['doc2vec'] = 'skip'
    else:
        vectorizing_config['doc2vec_vectorize'] = 'skip'

    # run the VM module to train
    vm_inst = VM(r_more_config)
    vm_inst.run_vm_train(vectorizing_config)

    # time to train/load vectorizers
    t_after_load_train = time.time()
    print(colored(str(t_after_load_train - t_before_load_train) + 'sec to train/load vectorizers \n', 'red'))

    # ------------------------------------------------------------------------------
    # VECTORIZE - SAMPLE AND COMPUTE VECTORS
    # ------------------------------------------------------------------------------

    # log start time
    t_before_sampling_vectorizing = time.time()

    # configure vectorizing
    vectorizing_config['process'] = 'vecotrize'
    vectorizing_config['r_pca_'] = r_pca_
    vectorizing_config['r_pca_vs_'] = r_pca_vs_
    vectorizing_config['r_sample_size'] = r_sample_size
    vectorizing_config['r_different_custering_data'] = r_different_custering_data
    vectorizing_config['raw_clustering_data_folder'] = r_raw_clustering_data_folder

    # run the VM module to sample and vectorize
    name_dict_all, name_vecs_all, vec_tfidf, vec_doc2vec = vm_inst.run_vm_sample_vectorize(vectorizing_config)

    # reduced configuration file logged
    r_configuration = dict()
    r_configuration['sample_size'] = r_sample_size
    r_configuration['doc2vec_window_size'] = r_doc2vec_window_size
    r_configuration['doc2vec_vector_size'] = r_doc2vec_vector_size
    r_configuration['tfidf_vector_size'] = r_tfidf_vector_size

    joblib.dump(r_configuration, r_output_result_folder + 'run_configuration_reduced', compress=1)

    # time to sample and vectorize
    t_after_sampling_vectorizing = time.time()
    print(colored(str(t_after_sampling_vectorizing - t_before_sampling_vectorizing) + 'sec to vectorize\n', 'red'))

    # ------------------------------------------------------------------------------
    # CLUSTER
    # ------------------------------------------------------------------------------

    # log start time
    t_before_clustering = time.time()

    # configure clustering
    clustering_config = dict()
    for cl in r_clustering_vectorizing_combs:
        clustering_config[cl] = True

    clustering_config['r_metric_'] = r_metric_
    clustering_config['r_kmeans_k_'] = r_kmeans_k_
    clustering_config['r_minibatch_'] = r_minibatch_
    clustering_config['r_agg_k_linkage_'] = r_agg_k_linkage_
    clustering_config['r_dbscan_eps_minpts_'] = r_dbscan_eps_minpts_
    clustering_config['output_result_folder'] = r_output_result_folder
    clustering_config['r_preprocessed_location'] = r_preprocessed_location
    clustering_config['r_n_clustering_processes'] = r_n_clustering_processes

    # if tasks are not pre-clustered then configure CM to cluster else configure CM to load pre-trained models
    clustering_config['process'] = 'train' if r_cluster_ else 'copy'

    # run clustering
    cm_inst = CM(r_more_config)
    cm_inst.run_cm(clustering_config, vec_doc2vec=vec_doc2vec, vec_tfidf=vec_tfidf)

    # time to cluster
    t_after_clustering = time.time()
    print(colored(str(t_after_clustering - t_before_clustering) + 'sec to cluster  \n', 'red'))

    # ------------------------------------------------------------------------------
    # SAMPLE
    # ------------------------------------------------------------------------------

    # log start time
    t_before_sampling = time.time()

    if r_sample_:
        # configure evaluation
        sampling_config = dict()
        sampling_config['fitness_'] = r_fitness_
        sampling_config['max_sample_size_'] = r_max_sample_size_
        sampling_config['min_samples_per_cluster_'] = r_min_samples_per_cluster_
        sampling_config['max_sampling_iteration_'] = r_max_sampling_iteration_
        sampling_config['measures'] = r_eva_measures
        sampling_config['vectorizing_models'] = r_eva_vectorizing_models
        sampling_config['clustering_models'] = r_eva_clustering_models
        sampling_config['output_result_folder'] = r_output_result_folder
        sampling_config['n_evaluation_processes'] = r_n_evaluation_processes

        # run evaluation
        run_sm(sampling_config)

    # time to cluster
    t_after_sampling = time.time()
    print(colored(str(t_after_sampling - t_before_sampling) + 'sec to sample  \n', 'red'))

    # ------------------------------------------------------------------------------
    # EVALUATE
    # ------------------------------------------------------------------------------

    # log start time
    t_before_evaluation = time.time()

    if r_evaluate_:
        # configure evaluation
        evaluation_config = dict()
        evaluation_config['measures'] = r_eva_measures
        evaluation_config['vectorizing_models'] = r_eva_vectorizing_models
        evaluation_config['clustering_models'] = r_eva_clustering_models
        evaluation_config['output_result_folder'] = r_output_result_folder
        evaluation_config['n_evaluation_processes'] = r_n_evaluation_processes

        # run evaluation
        run_em(evaluation_config)

    # time to cluster
    t_after_evaluation = time.time()
    print(colored(str(t_after_evaluation - t_before_evaluation) + 'sec to evaluate  \n', 'red'))

    # ------------------------------------------------------------------------------
    # RETURN
    # ------------------------------------------------------------------------------
    return name_dict_all, name_vecs_all, r_configuration


def main(args):
    # Create the dictionary to store the configurations
    config = dict()

    # Parse the configuration file
    with open(args[0], 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            temp = line.split(sep=':')
            config[temp[0]] = temp[1]
    f.close()

    # Process configurations
    preprocess_ = eval(config['preprocess_'])
    vectorize_ = eval(config['vectorize_'])
    cluster_ = eval(config['cluster_'])
    evaluate_ = eval(config['evaluate_'])
    sample_ = eval(config['sample_'])
    preprocess_tfidf = eval(config['preprocess_tfidf'])
    preprocess_doc2vec = eval(config['preprocess_doc2vec'])
    different_custering_data = eval(config['different_custering_data'])

    # Parallelism configurations
    n_clustering_processes = eval(config['n_clustering_processes'])
    n_evaluation_processes = eval(config['n_evaluation_processes'])

    # Clustering configurations
    kmeans_k_ = eval(config['kmeans_k_'])
    minibatch_km_ = eval(config['minibatch_km_'])
    dbscan_eps_ = eval(config['dbscan_eps_'])
    dbscan_min_points_ = eval(config['dbscan_min_points_'])
    metric_ = config['distance_metric_']
    agg_k_ = eval(config['agg_k_'])
    agg_linkage_ = eval(config['agg_linkage_'])

    # Vectorizing configuration
    doc2vec_windows_ = eval(config['doc2vec_windows_'])
    doc2vec_sizes_ = eval(config['doc2vec_sizes_'])
    tfidf_vector_sizes_ = eval(config['tfidf_vector_sizes_'])
    pca_ = eval(config['tfidf_pca_'])
    pca_vs_ = eval(config['tfidf_vector_sizes_pca_'])

    # Running configuration
    doc_sample_sizes = eval(config['doc_sample_sizes'])
    clustering_vectorizing_combs = eval(config['clustering_vectorizing_combs'])

    # Combined configurations: for algorithms that takes multiple parameters
    agg_k_linkage_ = list(itertools.product(agg_k_, agg_linkage_))
    dbscan_eps_minpts_ = list(itertools.product(dbscan_eps_, dbscan_min_points_))

    # Sampling configurations
    fitness_ = config['sampling_fitness']
    max_sample_size_ = eval(config['max_sample_size_'])
    min_samples_per_cluster_ = eval(config['min_samples_per_cluster_'])
    max_sampling_iteration_ = eval(config['max_sampling_iteration_'])

    # Evaluation configurations
    eva_vectorizing_models = eval(config['eva_vectorizing_models'])
    eva_clustering_models = eval(config['eva_clustering_models'])
    eva_measures = eval(config['eva_measures'])

    # get day and month
    day = datetime.date.today().day
    month_num = datetime.date.today().month
    month = calendar.month_name[month_num]
    run_date = str(day) + '_' + month[:3] + '/'

    # Location configurations
    raw_data_folder = eval(config['raw_data_folder'])
    raw_clustering_data_folder = eval(config['raw_clustering_data_folder'])
    result_folder = eval(config['result_folder'])

    # create parent folder if missing : experiments per date
    location = socket.gethostname() + '/'
    if not os.path.exists(result_folder + location + run_date):
        os.makedirs(result_folder + location + run_date)

    run_counter = len(list(os.walk(result_folder + location + run_date))[0][1])
    run_it = 'run_1/' if run_counter < 1 else 'run_' + str(
        np.sort([int(x.split('_')[1]) for x in list(os.walk(result_folder + location + run_date))[0][1]])[-1] + 1) + '/'

    run_id = run_date + run_it

    output_result_folder = result_folder + location + run_id
    tokenized_data_folder = output_result_folder + '/tokenized'
    vectorized_data_folder = output_result_folder + '/vectorized'
    preprocessed_location = '../Results/' + location + config['preprocessed_location']

    if not os.path.exists(output_result_folder):
        os.makedirs(output_result_folder)

    # Output logging config
    log_file = open(output_result_folder + 'logfile', 'w')
    backup = sys.stdout
    sys.stdout = Tee(sys.stdout, log_file)

    # Copy the configuration file to the run folder for traceability
    shutil.copyfile("./main_config", output_result_folder + 'main_config')
    shutil.copyfile("./more_config", output_result_folder + 'more_config')

    # Run the main vectorizing/clustering script
    # TODO: CHECK AND FIX THE [0] THING
    vectorize_cluster_sample_evaluate(r_cluster_=cluster_,
                                      r_sample_size=doc_sample_sizes[0],  # [0] to be remove in future version
                                      r_doc2vec_vector_size=doc2vec_sizes_[0],
                                      r_doc2vec_window_size=doc2vec_windows_[0],
                                      r_tfidf_vector_size=tfidf_vector_sizes_[0],
                                      r_clustering_vectorizing_combs=clustering_vectorizing_combs,
                                      r_kmeans_k_=kmeans_k_,
                                      r_minibatch_=minibatch_km_,
                                      r_dbscan_eps_minpts_=dbscan_eps_minpts_,
                                      r_agg_k_linkage_=agg_k_linkage_,
                                      r_metric_=metric_,
                                      r_n_clustering_processes=n_clustering_processes,
                                      r_n_evaluation_processes=n_evaluation_processes,
                                      r_preprocess_=preprocess_,
                                      r_evaluate_=evaluate_,
                                      r_preprocess_tfidf=preprocess_tfidf,
                                      r_preprocess_doc2vec=preprocess_doc2vec,
                                      r_different_custering_data=different_custering_data,
                                      r_preprocessed_location=preprocessed_location,
                                      r_vectorize_=vectorize_,
                                      r_pca_=pca_,
                                      r_pca_vs_=pca_vs_[0],
                                      r_eva_vectorizing_models=eva_vectorizing_models,
                                      r_eva_clustering_models=eva_clustering_models,
                                      r_eva_measures=eva_measures,
                                      r_sample_=sample_,
                                      r_fitness_=fitness_,
                                      r_max_sample_size_=max_sample_size_,
                                      r_min_samples_per_cluster_=min_samples_per_cluster_,
                                      r_max_sampling_iteration_=max_sampling_iteration_,
                                      r_output_result_folder=output_result_folder,
                                      r_tokenized_data_folder=tokenized_data_folder,
                                      r_vectorized_data_folder=vectorized_data_folder,
                                      r_raw_clustering_data_folder=raw_clustering_data_folder,
                                      r_raw_data_folder=raw_data_folder,
                                      r_more_config=args[1],
                                      )

    sys.stdout = backup
    log_file.close()


if __name__ == "__main__":
    main(sys.argv)
