import copy
import time
import shutil

from termcolor import colored
from sklearn.feature_extraction.text import TfidfVectorizer

from .Tools import *


class VM:

    def __init__(self, config_file):
        config = dict()
        # Parse the configuration file
        with open(config_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                temp = line.split(sep=':')
                config[temp[0]] = temp[1]
        f.close()

        self.doc2vec_dm = config['doc2vec_dm']
        self.doc2vec_alpha = config['doc2vec_alpha']
        self.doc2vec_min_alpha = config['doc2vec_min_alpha']
        self.doc2vec_min_count = config['doc2vec_min_count']
        self.doc2vec_iter = config['doc2vec_min_iter']
        self.doc2vec_negative = config['doc2vec_min_negative']

    # Runs doc2vec vectorization with manual iteration parameterization
    def run_doc2vec_manual_epochs(self, dv_data, dv_result_folder, dv_size, dv_window, dv_processed=True):
        assert gensim.models.doc2vec.FAST_VERSION > -1

        # Load the documents
        if not dv_processed:
            documents = get_doc_p(dv_data, dv_result_folder, for_='doc2vec')
        else:
            documents = dv_data

        # Build the model
        model = gensim.models.Doc2Vec(min_count=1, window=dv_window, size=dv_size, sample=1e-4, negative=5, workers=16,
                                      iter=1)
        model.build_vocab(documents)

        # Configure initial alpha, the number of iterations and alpha steps
        alpha, min_alpha, passes = (0.025, 0.005, 20)
        alpha_delta = (alpha - min_alpha) / passes

        # Start training
        for epoch in range(passes):
            d_tmp = documents.copy()
            random.shuffle(d_tmp)
            model.alpha, model.min_alpha = alpha, alpha
            model.train(d_tmp, total_examples=model.corpus_count, epochs=model.iter)
            alpha -= alpha_delta

        # Save the model
        joblib.dump(model, dv_result_folder + '/doc2vec_vectorizer')
        model.save(dv_result_folder + '/doc2vec_model')

        return model

    # Runs doc2vec vectorization with automatic iteration parameterization
    def run_doc2vec(self, dv_data, dv_result_folder, dv_size, dv_window, manual_=False, dv_processed=True):
        if not manual_:
            # Load the documents
            if not dv_processed:
                documents = get_doc_p(dv_data, dv_result_folder, for_='doc2vec')
            else:
                documents = dv_data

            # Build the model
            model = gensim.models.Doc2Vec(dm=self.doc2vec_dm, alpha=self.doc2vec_alpha, window=dv_window, size=dv_size,
                                          min_alpha=self.doc2vec_min_alpha, min_count=self.doc2vec_min_count,
                                          iter=self.doc2vec_iter, negative=self.doc2vec_negative)
            # Build the vocabulary dictionary
            model.build_vocab(documents)

            # Start training
            model.train(documents, total_examples=model.corpus_count, epochs=20)

            # Save the model
            joblib.dump(model, dv_result_folder + '/doc2vec_vectorizer')
            model.save(dv_result_folder + '/doc2vec_model')
            model.wv.save_word2vec_format(dv_result_folder + '/word2vec_model')

        else:
            model = self.run_doc2vec_manual_epochs(dv_data, dv_result_folder, dv_size, dv_window, dv_processed)

        return model

    # Runs TFIDF vectorization
    def run_tfidf(self, ti_data, ti_result_folder, ti_n_features, ti_processed=True):
        # Load the documents
        if not ti_processed:
            documents = get_doc_p(ti_data, ti_result_folder, for_="tfidf")
        else:
            documents = ti_data

        # Build the model
        vectorizer = TfidfVectorizer(max_features=ti_n_features)
        model = vectorizer.fit_transform([document[0] for document in documents])

        # scores = zip(vectorizer.get_feature_names(),
        #              np.asarray(model.sum(axis=0)).ravel())
        # sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        # print(len(sorted_scores))
        # for item in sorted_scores:
        #     print("{0:50} Score: {1}".format(item[0], item[1]))

        # Save the model
        joblib.dump(model, ti_result_folder + '/tfidf_model', compress=1)
        joblib.dump(vectorizer, ti_result_folder + '/tfidf_vectorizer', compress=1)

        return model

    # Takes a set of documents and vectorizes them using the input TFIDF model
    def vectorize_document_tfidf(self, vdt_doc_dict, vdt_result_folder, vdd_vectorizer):
        vdt_doc_sample_tfidf = []
        for index, document in vdt_doc_dict.items():
            vdt_temp = [index, vdd_vectorizer.transform([document]).toarray()[0]]
            vdt_doc_sample_tfidf.append(vdt_temp)

        vdt_vec_ = [x[1] for x in vdt_doc_sample_tfidf]
        joblib.dump(vdt_vec_,
                    vdt_result_folder + '/tfidf_sample_vecs_' + str(len(vdt_vec_)) + '_' + str(round(time.time())),
                    compress=1)

        return vdt_vec_

    # Takes a set of documents and vectorizes them using the input doc2vec model
    def vectorize_document_doc2vec(self, vdd_doc_dict, vdd_result_folder, vdd_vectorizer):
        vdd_doc_sample_doc2vec = []
        for index, document in vdd_doc_dict.items():
            vdt_temp = [index, vdd_vectorizer.infer_vector(document)]
            vdd_doc_sample_doc2vec.append(vdt_temp)

        vdd_vec_ = [x[1] for x in vdd_doc_sample_doc2vec]

        joblib.dump(vdd_vec_,
                    vdd_result_folder + '/doc2vec_sample_vecs_' + str(len(vdd_vec_)) + '_' + str(round(time.time())),
                    compress=1)
        return vdd_vec_

    # Run the Vectorizing module : train
    def run_vm_train(self, conf):
        print(colored('Training the vectorizers ', 'green'))

        # load configurations
        raw_data_folder = conf['raw_data_folder']
        output_result_folder = conf['output_result_folder']
        tokenized_data_folder = conf['tokenized_data_folder']
        vectorized_data_folder = conf['vectorized_data_folder']
        r_preprocessed_location = conf['r_preprocessed_location']

        # if vectorizers need to be trained
        if conf['process'] == 'train':
            if not os.path.exists(tokenized_data_folder):
                os.makedirs(tokenized_data_folder)

            if not os.path.exists(vectorized_data_folder):
                os.makedirs(vectorized_data_folder)

            r_tfidf_vector_size = conf['r_tfidf_vector_size']
            r_doc2vec_window_size = conf['r_doc2vec_window_size']
            r_doc2vec_vector_size = conf['r_doc2vec_vector_size']

        # if vectorizers are pre-trained
        if conf['process'] == 'copy':
            # copy the preprocessed models to the current run dir : to keep track of what data/models was used in each run
            shutil.copytree(r_preprocessed_location + '/vectorized', vectorized_data_folder)
            shutil.copytree(r_preprocessed_location + '/tokenized', tokenized_data_folder)

        # if TFIDF is needed
        if 'tfidf' in conf:
            if conf['tfidf'] == 'train':
                print('\t tfidf  \t ... \t', end="")
                data_tf = get_doc_p(raw_data_folder, output_result_folder, for_='tfidf')
                t0 = time.time()
                self.run_tfidf(data_tf, output_result_folder, r_tfidf_vector_size)
                t1 = time.time()
                print(round(t1 - t0, 6), 'sec \t... \t', end='')
                print('Done')

            if conf['tfidf'] == 'copy':
                try:
                    shutil.copyfile(r_preprocessed_location + '/tfidf_vectorizer',
                                    output_result_folder + '/tfidf_vectorizer')
                    shutil.copyfile(r_preprocessed_location + '/tfidf_model', output_result_folder + '/tfidf_model')
                    print('\t tfidf  \t ... \tVectorizer is pre-trained \t ... \t Done')
                except FileNotFoundError:
                    print("\t tfidf : You did not choose a location containing a pre-trained Doc2vec model : Skipped")

        # if doc2vec is needed
        if 'doc2vec' in conf:
            if conf['doc2vec'] == 'train':
                print('\t doc2vec\t ... \t', end="")
                data_d2v = get_doc_p(raw_data_folder, output_result_folder, for_='doc2vec')
                t0 = time.time()
                self.run_doc2vec(data_d2v, output_result_folder, dv_window=r_doc2vec_window_size,
                                 dv_size=r_doc2vec_vector_size)
                t1 = time.time()
                print(round(t1 - t0, 6), 'sec \t... \t', end='')
                print('Done')

            if conf['doc2vec'] == 'copy':
                try:
                    shutil.copyfile(r_preprocessed_location + '/doc2vec_vectorizer',
                                    output_result_folder + '/doc2vec_vectorizer')
                    shutil.copyfile(r_preprocessed_location + '/doc2vec_model', output_result_folder + '/doc2vec_model')
                    print('\t doc2vec\t ... \tVectorizer is pre-trained \t ... \t Done')

                except FileNotFoundError:
                    print("\t doc2vec : You did not choose a location containing a pre-trained Doc2vec model : Skipped")

        return 0

    # Run the Vectorizing module : sample/vectorize
    def run_vm_sample_vectorize(self, conf):
        vec_tfidf = []
        vec_doc2vec = []
        tasks_ids_ = []
        sample_tasks_ids_ = []
        doc_sample_dict = []
        name_dict_all = dict()
        name_vecs_all = dict()

        # load configurations
        r_pca_ = conf['r_pca_']
        r_pca_vs_ = conf['r_pca_vs_']
        r_sample_size = conf['r_sample_size']
        output_result_folder = conf['output_result_folder']
        vectorized_data_folder = conf['vectorized_data_folder']
        r_preprocessed_location = conf['r_preprocessed_location']
        r_different_custering_data = conf['r_different_custering_data']
        raw_clustering_data_folder = conf['raw_clustering_data_folder']

        # vectorizers are trained on the full dataset but it is possible to vectorized and clustered just a sample
        # If doc_sample_sizes equals -1 in the config file then no sampling is needed
        if conf['tfidf_vectorize'] == 'vectorize' or conf['doc2vec_vectorize'] == 'vectorize':
            tasks_ids_ = joblib.load(output_result_folder + '/vectorized/task_ids')
            sample_tasks_ids_ = random.sample(tasks_ids_, r_sample_size) if r_sample_size > -1 else tasks_ids_

        print(colored('Loading the trained Vectorizers', 'green'))
        if 'tfidf' in conf and conf['tfidf_vectorize'] != 'skip':
            if conf['tfidf_vectorize'] == 'vectorize':
                # load the vectorizers
                print('\t tfidf  \t ... \t Loading\t\t ...', end="")
                tfidf_vectorizer = joblib.load(output_result_folder + '/tfidf_vectorizer')

                # load documents
                if r_different_custering_data:
                    doc_tfidf = get_doc_p(raw_clustering_data_folder, output_result_folder, for_='tfidf')
                else:
                    doc_tfidf = joblib.load(vectorized_data_folder + '/data_tfidf')

                # sample the documents
                print('\t Sampling\t\t ...', end="")
                doc_sample_dict = []
                if r_sample_size != len(tasks_ids_):
                    for d in doc_tfidf:
                        if d[1][0] in sample_tasks_ids_:
                            doc_sample_dict.append(d)

                else:
                    doc_sample_dict = copy.deepcopy(doc_tfidf)

                # vectorize the sampled documents
                print('\t Vectorizing\t ... \t', end="")
                t0 = time.time()
                vec_tfidf = [tfidf_vectorizer.transform([index[0][1:]]).toarray()[0] for index in doc_sample_dict]
                t1 = time.time()

                # reduce the dimensionality of the TFIDF vectors using PCA
                if r_pca_:
                    pca = decomposition.PCA(n_components=r_pca_vs_)
                    pca.fit(vec_tfidf)
                    vec_tfidf = pca.transform(vec_tfidf)

                print(round(t1 - t0, 6), 'sec \t... \t', end='')

            if conf['tfidf_vectorize'] == 'copy':
                print("\t tfidf  \t ... \t pre-sampled and vectorized\t ... \t", end="")
                vec_tfidf = joblib.load(r_preprocessed_location + '/tfidf_sample_vecs_' + str(r_sample_size))
                doc_sample_dict = joblib.load(r_preprocessed_location + '/tfidf_sample_dict_' + str(r_sample_size))

            name_vecs = output_result_folder + '/tfidf_sample_vecs_' + str(r_sample_size)
            joblib.dump(vec_tfidf, name_vecs, compress=1)

            name_dict = output_result_folder + '/tfidf_sample_dict_' + str(r_sample_size)
            joblib.dump(doc_sample_dict, name_dict, compress=1)

            name_dict_all['tfidf'] = name_dict
            name_vecs_all['tfidf'] = name_vecs

            print('Done')

        if 'doc2vec' in conf and conf['doc2vec_vectorize'] != 'skip':
            if conf['doc2vec_vectorize'] == 'vectorize':

                # load the vectorizers
                print('\t doc2vec\t ... \t Loading\t\t ...', end="")
                doc2vec_vectorizer = joblib.load(output_result_folder + '/doc2vec_vectorizer')

                # load documents
                if r_different_custering_data:
                    doc_doc2vec = get_doc_p(raw_clustering_data_folder, output_result_folder)
                else:
                    doc_doc2vec = joblib.load(vectorized_data_folder + '/data_doc2vec')

                # Sample the documents
                print('\t Sampling\t\t ...', end="")
                doc_sample_dict = []
                if r_sample_size != len(tasks_ids_):
                    for d in doc_doc2vec:
                        if d[1][0] in sample_tasks_ids_:
                            doc_sample_dict.append(d)
                else:
                    doc_sample_dict = copy.deepcopy(doc_doc2vec)

                # Vectorize the sampled documents
                print('\t Vectorizing\t ... \t', end="")
                t0 = time.time()
                vec_doc2vec = [doc2vec_vectorizer.docvecs[index[1]][0] for index in doc_sample_dict]
                t1 = time.time()

                print(round(t1 - t0, 6), 'sec \t... \t', end='')

            if conf['doc2vec_vectorize'] == 'copy':
                print("\t doc2vec\t ...\t pre-sampled and vectorized\t ... \t", end="")
                vec_doc2vec = joblib.load(r_preprocessed_location + '/doc2vec_sample_vecs_' + str(r_sample_size))
                doc_sample_dict = joblib.load(r_preprocessed_location + '/doc2vec_sample_dict_' + str(r_sample_size))

            name_vecs = output_result_folder + '/doc2vec_sample_vecs_' + str(r_sample_size)
            joblib.dump(vec_doc2vec, name_vecs, compress=1)

            name_dict = output_result_folder + '/doc2vec_sample_dict_' + str(r_sample_size)
            joblib.dump(doc_sample_dict, name_dict, compress=1)

            name_dict_all['doc2vec'] = name_dict
            name_vecs_all['doc2vec'] = name_vecs
            print('Done')

        return name_dict_all, name_vecs_all, vec_tfidf, vec_doc2vec
