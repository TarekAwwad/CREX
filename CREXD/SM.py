import collections

from CREXD.EM import *


# The clustering sampling function
def sample_clusterings(r_clusterings, r_max_size, r_min_sample, r_max_iterations, sc_result_folder, sc_fitness):
    idx = {}
    r_pop = []
    labels = []

    # print(len(r_clusterings), r_max_size, r_min_sample, r_max_iterations, sc_result_folder)

    # ------------------------------------------------------------------------------------------------------------------#
    # r_clusterings_tmp = {}
    # for k in r_clusterings.keys():
    #     r_clusterings_tmp_c = {}
    #     for j in r_clusterings[k]:
    #         if len(r_clusterings[k][j]) < 4000:
    #             r_clusterings_tmp_c[j] = r_clusterings[k][j].copy()
    #     r_clusterings_tmp[k] = r_clusterings_tmp_c
    # ------------------------------------------------------------------------------------------------------------------#

    # Create population: concatenate the clusters of one clustering
    r_pop_ = next(iter(r_clusterings.values()))
    for element_ in r_pop_.values():
        for el in element_:
            r_pop.append(el)

    # Create the tagged population: labels are appended to element names
    temp_pop = []
    for clustering_ in r_clusterings.keys():
        clustering = r_clusterings[clustering_]
        for cluster_tmp in clustering.keys():
            labels.append(clustering_ + '_' + str(cluster_tmp))
            cluster__ = r_clusterings[clustering_][cluster_tmp]
            for element in cluster__:
                temp_pop.append(element + '-' + clustering_ + '_' + str(cluster_tmp))

    # Initialize the dictionary of indices: {element_: [list of clusters to which element_ belongs]}
    for element_ in r_pop:
        idx[element_] = []

    # Fill the dictionary of indices
    for element_ in temp_pop:
        element_temp_ = element_.split('-')
        idx[element_temp_[0]].append(element_temp_[1])

    # Create the map to track the number of sample tasks per cluster
    count_temp = np.zeros(len(labels))
    sample_elements_per_cluster_map = dict(zip(labels, count_temp))

    # Variable initialization
    it = 0
    it_changed = 0
    output_sample = []
    max_cluster_number = len(labels)

    # Convergence iterators and flag
    min_sample_it = 0.
    max_sample_it = 500.
    converged = False

    # ------------------------------------------------------------------------------------------------------------------#
    output_sample = random.sample(r_pop, r_max_size)
    for lab in labels:
        for sample in output_sample:
            if lab in idx[sample]:
                sample_elements_per_cluster_map[lab] += 1
    # ------------------------------------------------------------------------------------------------------------------#
    total_size_it = len(output_sample)

    sample_buffer = collections.deque(maxlen=15)

    # Do the actual sampling
    while it < r_max_iterations and not converged:
        if total_size_it <= r_max_size and min_sample_it >= r_min_sample:
            converged = True
            print("converged")
            continue

        if total_size_it < r_max_size:
            new_s = random.sample(r_pop, max_cluster_number)
            output_sample = output_sample + new_s

            # count samples per cluster:
            for lab in labels:
                for sample in new_s:
                    if lab in idx[sample]:
                        sample_elements_per_cluster_map[lab] += 1

        if total_size_it >= r_max_size:
            # print(total_size_it, len(r_pop), it, end='|', flush=True)

            # substitute a task vector inside the sample
            r = random.sample(output_sample, round(1))
            output_sample_temp = [n for n in output_sample if n not in r]

            new_s = random.sample(r_pop, round(1))
            output_sample_temp = output_sample_temp + new_s

            # update sample count per cluster:
            map_temp = sample_elements_per_cluster_map.copy()
            for lab in labels:
                for sample in r:
                    if lab in idx[sample]:
                        map_temp[lab] -= 1

            for lab in labels:
                for sample in new_s:
                    if lab in idx[sample]:
                        map_temp[lab] += 1

            # i = 0
            # for lab in labels:
            #     if map_temp[lab] > sample_elements_per_cluster_map[lab]:
            #         i += 1

            # print(i)

            # verify criteria
            err_it = 0
            if sc_fitness == 'rmse':
                err_temp = 0

                for lab in labels:
                    err_temp += pow((map_temp[lab] - r_min_sample), 2)
                    err_it += pow((sample_elements_per_cluster_map[lab] - r_min_sample), 2)

                err_it /= len(labels)
                err_temp /= len(labels)

                if err_temp > err_it:
                    it += 1
                    continue
                    None

                else:
                    sample_elements_per_cluster_map = map_temp.copy()
                    output_sample = output_sample_temp.copy()
                    sample_buffer.append(output_sample)
                    # output_sample = [n for n in output_sample if n not in r]
                    r_pop = r_pop + r

            if sc_fitness == 'minmax':
                min_sample_t = min(map_temp.values())
                max_sample_t = max(map_temp.values())

                if max_sample_t > max_sample_it or min_sample_t < min_sample_it:
                    it += 1
                    continue
                    # None

                else:
                    sample_elements_per_cluster_map = map_temp.copy()
                    output_sample = output_sample_temp.copy()
                    # output_sample = [n for n in output_sample if n not in r]
                    r_pop = r_pop + r

        r_pop = [n for n in r_pop if n not in output_sample]

        # check sample size
        total_size_it = len(output_sample)
        min_sample_it = min(sample_elements_per_cluster_map.values())
        max_sample_it = max(sample_elements_per_cluster_map.values())
        it += 1
        it_changed += 1

        red = 0
        yellow = 0
        green = 0
        blue = 0

        # print(it_changed % 50 )

        if it_changed % 50 == 0:
            for elll in sorted(list(sample_elements_per_cluster_map)):
                if 0 <= sample_elements_per_cluster_map[elll] <= 10:
                    red += 1
                    # print(colored(sample_elements_per_cluster_map[elll], 'red'), end=' ')
                if 10 < sample_elements_per_cluster_map[elll] <= 15:
                    yellow += 1
                    # print(colored(sample_elements_per_cluster_map[elll], 'yellow'), end=' ')
                if 15 < sample_elements_per_cluster_map[elll] <= 25:
                    green += 1
                    # print(colored(sample_elements_per_cluster_map[elll], 'green'), end=' ')
                if 25 < sample_elements_per_cluster_map[elll]:
                    blue += 1
                    # print(colored(sample_elements_per_cluster_map[elll], 'blue'), end=' ')
            # print(red, yellow, green, blue, end=' ')
            #
            # print(total_size_it, len(r_pop), it)

    print()

    map1 = dict(zip(labels, count_temp))
    for lab in labels:
        for sample in output_sample:
            if lab in idx[sample]:
                map1[lab] += 1
    # print(map1)
    # print('\t', np.array(sample_elements_per_cluster_map.values()))

    print('\t',
          colored("Used fitness \t : \t", 'blue'), sc_fitness, colored("\t fitness \t : \t", 'blue'), err_it,
          colored("\t Positive iterations \t : \t", 'blue'), it_changed,
          colored("\n\t *-Converged before Max iteration is reached \t : \t", 'blue'), it < r_max_iterations, it,
          colored("\n\t Sample per cluster - Const. respected   \t : \t", 'blue'),
          min(sample_elements_per_cluster_map.values()) >= r_min_sample,
          min(sample_elements_per_cluster_map.values()),
          colored("\n\t Sample size - Const. respected   \t\t : \t", 'blue'), total_size_it <= r_max_size,
          len(output_sample))

    f = open(sc_result_folder + 'sample_' + str(r_max_size) + '_' + str(r_min_sample) + '_' + str(
        round(time.time())) + '.txt', 'a')

    f.write("Converged before Max iteration is reached : " + str(it < r_max_iterations) + ' ' + str(it) +
            "\nSample per cluster - Const. respected : " + str(
        min(sample_elements_per_cluster_map.values()) >= r_min_sample) + ' ' +
            str(min(sample_elements_per_cluster_map.values())) +
            "\nSample size - Const. respected : " + str(total_size_it <= r_max_size) + ' ' + str(
        len(output_sample)) + '\n')
    f.write(str(output_sample))
    f.write('\n \n \n buffered samples')
    f.write(str(sample_buffer))

    # print(sample_buffer)

    return output_sample  # A parallel call of the sample_clusterings() function


# Parallel call of the sampling method
def sample_clusterings_p(args):
    return sample_clusterings(*args)


def run_sm(conf):
    print(colored('Sampling', 'green'))

    # load configurations
    fitness_ = conf['fitness_']
    max_sample_size_ = conf['max_sample_size_']
    clustering_models = conf['clustering_models']
    vectorizing_models = conf['vectorizing_models']
    output_result_folder = conf['output_result_folder']
    max_sampling_iteration_ = conf['max_sampling_iteration_']
    min_samples_per_cluster_ = conf['min_samples_per_cluster_']
    re_conf = joblib.load(output_result_folder + '/run_configuration_reduced')
    doc_sample_sizes = re_conf['sample_size']

    # warn for empty clustering model choice
    if len(clustering_models) == 0:
        warnings.warn('Choose the clustering model(s) to sample')
        return 1

    # warn for empty vectorizing model choice
    if len(vectorizing_models) == 0:
        warnings.warn('Choose the vectorizing model(s) to sample')
        return 1

    clusterings_cluster_set = {}

    # Evaluate the results
    for vec_model in vectorizing_models:
        for clu_model in clustering_models:

            sc_comb_name = clu_model + '_' + vec_model

            # Load the used models
            re_models_file_names = glob.glob(output_result_folder + '/' + clu_model + '_' + vec_model + '_model_*')
            re_models_file_names.sort()  # help getting sorted evaluation lost : unnecessary

            try:
                re_models = [joblib.load(re_models_file) for re_models_file in re_models_file_names]
            except FileNotFoundError:
                print("\t No models file for " + clu_model + '_' + vec_model + " was found : Skipped")

            # Load the true labeled data (many data sets are used to build the corpus, they are used as true labels)
            try:
                re_true_raw = joblib.load(
                    output_result_folder + '/' + vec_model + '_sample_dict_' + str(doc_sample_sizes))

                # Fetching just the labels
                re_true_labels = [index[1][0].split('_')[0] for index in re_true_raw]

                re_tasks_ids = [index[1][0] for index in re_true_raw]

                for sss_model in re_models:
                    clusterings_cluster_set[clu_model + '_' + vec_model] = fetch_cluster_content(sss_model,
                                                                                                 re_true_labels,
                                                                                                 re_tasks_ids,
                                                                                                 sc_comb_name,
                                                                                                 True)
            except FileNotFoundError:
                print("\t No vector file for " + vec_model + " was found : Skipped")
                print("\t If you are using pre-computed vectors check the preprocessed_location configuration")
                print("\t Else check the processing/vectorizing/clustering configurations")

    if len(clusterings_cluster_set) == 0 or len(re_models) == 0:
        print("\t No clustering was found for the selected models: Sampling Skipped")
    else:
        sample_clusterings(clusterings_cluster_set, max_sample_size_, min_samples_per_cluster_, max_sampling_iteration_,
                           output_result_folder, fitness_)

    return 0
