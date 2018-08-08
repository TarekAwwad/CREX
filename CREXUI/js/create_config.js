function create_default_config(config_to_generate) {
    var dict_default = {};

    if (config_to_generate === 'main') {
        // What to do :
        dict_default.preprocess_ = "False";
        dict_default.vectorize_ = "False";
        dict_default.cluster_ = "False";
        dict_default.sample_ = "False";
        dict_default.evaluate_ = "False";

        // Shared configuration (Clusterers/vectorizers)
        dict_default.distance_metric_ = "euclidean";
        dict_default.doc_sample_sizes = "[1000]";
        dict_default.preprocess_tfidf = "False";
        dict_default.preprocess_doc2vec = "False";
        dict_default.different_custering_data = "False";

        // Multi-threading
        dict_default.n_clustering_processes = "1";
        dict_default.n_evaluation_processes = "4";

        // Clustering configuration
        dict_default.kmeans_k_ = "[10]";
        dict_default.minibatch_km_ = "0";
        dict_default.dbscan_min_points_ = "[10]";
        dict_default.dbscan_eps_ = "[10]";
        dict_default.agg_k_ = "[10]";
        dict_default.agg_linkage_ = "'ward'";

        // Vectorizing configuration
        dict_default.doc2vec_sizes_ = "[50]";
        dict_default.doc2vec_windows_ = "[20]";
        dict_default.tfidf_vector_sizes_ = "[10000]";
        dict_default.tfidf_pca_ = "True";
        dict_default.tfidf_vector_sizes_pca_ = "[1000]";

        // Sampling configuration
        dict_default.sampling_fitness = "rmse";
        dict_default.max_sample_size_ = "500";
        dict_default.min_samples_per_cluster_ = "10";
        dict_default.max_sampling_iteration_ = "10000";

        // Evaluation configuration
        dict_default.eva_measures = "['hcv']";
        dict_default.eva_vectorizing_models = "['tfidf']";
        dict_default.eva_clustering_models = "['kmeans']";

        // Locations
        dict_default.result_folder = "'../Results'";
        dict_default.raw_data_folder = "'../TestData/20news/'";
        dict_default.preprocessed_location = '';
        dict_default.raw_clustering_data_folder = "'../TestData/20news/'";
        dict_default.clustering_vectorizing_combs = "['kmeans_tfidf']";
    }
    if (config_to_generate === 'more') {
        // kmeans configurations
        dict_default.kmeans_init = "'kmeans++'";
        dict_default.kmeans_n_init = "10";
        dict_default.kmeans_n_job = "1";
        dict_default.kmeans_max_iter = "100";
        dict_default.kmeans_verbose = "0";

        // dbscan configuration
        dict_default.dbscan_algorithm = "'brute'";
        dict_default.dbscan_leaf_size = 'None';
        dict_default.dbscan_p = "30";

        // dbscan configuration
        dict_default.doc2vec_dm = "1";
        dict_default.doc2vec_alpha = "0.025";
        dict_default.doc2vec_min_alpha = "0.005";
        dict_default.doc2vec_min_count = "4";
        dict_default.doc2vec_iter = "20";
        dict_default.doc2vec_negative = "5";
    }
    return dict_default;
}

function trueToTrue(x) {
    if (x) {
        return 'True';
    }
    else {
        return 'False';
    }
}

// Create the configuration files
function create_crexd_config() {

    var res_main_content = "";
    var res_more_content = "";
    var res_label = "";

    // Create the copy to clipboard button
    var copyCB = document.createElement("input");
    copyCB.setAttribute("type", "button");
    copyCB.setAttribute("value", "Copy to clipboard");
    copyCB.setAttribute("class", "a2a_dd btn");
    copyCB.setAttribute("onclick", "copyToCB(this.id)");
    copyCB.setAttribute("id", "config-main-button");

    var copyCB_more = document.createElement("input");
    copyCB_more.setAttribute("type", "button");
    copyCB_more.setAttribute("value", "Copy to clipboard");
    copyCB_more.setAttribute("class", "a2a_dd btn");
    copyCB_more.setAttribute("onclick", "copyToCB(this.id)");
    copyCB_more.setAttribute("id", "config-more-button");

    // Create the download button
    var dlCB = document.createElement("input");
    dlCB.setAttribute("type", "button");
    dlCB.setAttribute("value", "Download");
    dlCB.setAttribute("class", "btn");
    dlCB.setAttribute("id", "dl-main-button");
    dlCB.setAttribute("onclick", "download('main_config', 'config-main-content')");

    var dlCB_more = document.createElement("input");
    dlCB_more.setAttribute("type", "button");
    dlCB_more.setAttribute("value", "Download");
    dlCB_more.setAttribute("class", "btn");
    dlCB_more.setAttribute("id", "dl-more-button");
    dlCB_more.setAttribute("onclick", "download('more_config', 'config-more-content')");

    // Dictionary of available vectorizing/clustering/evaluation methods
    var clusterer_ids = ['km', 'db', 'ag'];
    var vectorizer_ids = ['tfidf', 'doc2vec', 'pact'];
    var measures_ids = ['hcv', 'sil', 'coc'];

    // Data holders
    var clusterers_ = [];
    var vectorizers_ = [];
    var eval_measures_ = [];
    var evaluate_vectorizers_ = [];
    var evaluate_clusterers_ = [];
    var clustering_vectorizing_combs = [];
    var text_input_to_verify = [];

    // Initialize the configuration dictionary with the default configurations
    var dict = create_default_config('main');
    var dict_more = create_default_config('more');

    // Get the custom configurations
    if (document.getElementById('custom').checked) {
        dict.doc_sample_sizes = "[" + document.getElementsByName('sample-s')[0].value + "]";
        dict.distance_metric_ = document.getElementsByName('distance-metric')[0].value;
        dict.preprocess_ = trueToTrue(document.getElementsByName('process')[0].checked);
        dict.vectorize_ = trueToTrue(document.getElementsByName('vectorize')[0].checked);
        dict.different_custering_data = document.getElementsByName('diffdata')[0].value;

        if (dict.preprocess_ === 'True') {
            dict.preprocess_tfidf = trueToTrue(document.getElementById('process-doc2vec').checked);
            dict.preprocess_doc2vec = trueToTrue(document.getElementById('process-tfidf').checked);
        }
        else {
            dict.preprocessed_location = document.getElementsByName('preprocessed-location')[0].value;
            text_input_to_verify.push('preprocessed-location')
        }

        text_input_to_verify.push('sample-s')
    }

    // Get the advanced configurations
    if (document.getElementById('advanced').checked) {
        dict.result_folder = document.getElementsByName('result-folder')[0].value;
        dict.raw_data_folder = document.getElementsByName('raw-data-folder')[0].value;
        dict.raw_clustering_data_folder = document.getElementsByName('raw-clustering-data-folder')[0].value;
        dict.n_clustering_processes = document.getElementsByName('n-clustering-processes')[0].value;
        dict.n_evaluation_processes = document.getElementsByName('n-evaluation-processes')[0].value;

        text_input_to_verify.push('result-folder');
        text_input_to_verify.push('raw-data-folder');
        text_input_to_verify.push('n-clustering-processes');
        text_input_to_verify.push('n-evaluation-processes');
        text_input_to_verify.push('raw-clustering-data-folder');
    }

    // Get the list of activated clustering models and evaluators
    for (var key_clusterer_id in clusterer_ids) {
        var temp_ = document.getElementById(clusterer_ids[key_clusterer_id]);
        if (temp_.checked) {
            clusterers_.push(temp_.value)
        }

        var temp_eval = document.getElementsByName('eval-clustering-' + clusterer_ids[key_clusterer_id])[0];
        if (temp_eval.checked) {
            evaluate_clusterers_.push(temp_eval.value)
        }
    }

    // Get the list of activated vectorizing models and evaluators
    for (var key_vectorizer_id in vectorizer_ids) {
        temp_ = document.getElementById(vectorizer_ids[key_vectorizer_id]);
        if (temp_.checked) {
            vectorizers_.push(temp_.value)
        }

        temp_eval = document.getElementsByName('eval-vectorizing-' + vectorizer_ids[key_vectorizer_id])[0];
        if (temp_eval.checked) {
            evaluate_vectorizers_.push(temp_eval.value)
        }
    }

    // Get the list of activated evaluation measures
    for (var measures_id in measures_ids) {
        temp_eval = document.getElementsByName('eval-measures-' + measures_ids[measures_id])[0];
        if (temp_eval.checked) {
            eval_measures_.push(temp_eval.value)
        }
    }

    // Get the configurations of the sampling module
    var sample_ = document.getElementsByName('sample')[0].checked;
    if (sample_) {
        dict.sample_ = trueToTrue(sample_);
        dict.sampling_fitness = document.getElementsByName('sampling-fitness')[0].value;
        dict.max_sample_size_ = document.getElementsByName('max-sample-size')[0].value;
        dict.min_samples_per_cluster_ = document.getElementsByName('min-samples-per-cluster')[0].value;
        dict.max_sampling_iteration_ = document.getElementsByName('max-sampling-iteration')[0].value;
        text_input_to_verify.push('max-sample-size');
        text_input_to_verify.push('min-samples-per-cluster');
        text_input_to_verify.push('max-sampling-iteration');
    }

    // Get the configurations of the evaluation module
    var evaluate_ = document.getElementsByName('evaluate')[0].checked;
    if (evaluate_) {
        var eva_measures = [];
        var eva_vectorizing_models = [];
        var eva_clustering_models = [];

        for (var key_eval_measure_ in eval_measures_) {
            eva_measures.push("'" + eval_measures_[key_eval_measure_] + "'");
        }

        for (var key_evaluate_vectorizer_ in evaluate_vectorizers_) {
            eva_vectorizing_models.push("'" + evaluate_vectorizers_[key_evaluate_vectorizer_] + "'");
        }

        for (var key_evaluate_clusterer_ in evaluate_clusterers_) {
            eva_clustering_models.push("'" + evaluate_clusterers_[key_evaluate_clusterer_] + "'");
        }

        dict.evaluate_ = trueToTrue(evaluate_);
        dict.eva_measures = '[' + eva_measures + ']';
        dict.eva_vectorizing_models = '[' + eva_vectorizing_models + ']';
        dict.eva_clustering_models = '[' + eva_clustering_models + ']';
    }

    // Get the configurations of the clustering module
    for (var key_clusterer_ in clusterers_) {
        for (var key_vectorizer_temp in vectorizers_) {
            clustering_vectorizing_combs.push("'" + clusterers_[key_clusterer_] + "_" + vectorizers_[key_vectorizer_temp] + "'")
        }

        if (clusterers_[key_clusterer_] === 'kmeans') {
            if (document.getElementById('kmeans-python').checked) {
                var kmeans_k_ = document.getElementsByName('kmeans-k')[0].value;
                text_input_to_verify.push('kmeans-k');
            }
            else {
                var min_k = document.getElementsByName('kmeans-k-min')[0].value;
                var max_k = document.getElementsByName('kmeans-k-max')[0].value;
                var step_k = document.getElementsByName('kmeans-k-step')[0].value;
                text_input_to_verify.push('kmeans-k-min');
                text_input_to_verify.push('kmeans-k-max');
                text_input_to_verify.push('kmeans-k-step');

                kmeans_k_ = '[i for i in range(' + min_k + ',' + max_k + ',' + step_k + ')]'
            }
            var minibatch_km_use_ = document.getElementById('kmeans-mb').checked;
            var minibatch_km_ = 0;
            if (minibatch_km_use_) {
                minibatch_km_ = document.getElementsByName('kmeans-mb-s')[0].value;
                dict.minibatch_km_ = minibatch_km_;
            }

            dict.kmeans_k_ = kmeans_k_;

            // Get the additional configuration
            var kmeans_more_ = document.getElementById('kmeans-more').checked;
            if (kmeans_more_) {
                var kmeans_init = document.getElementsByName('kmeans-init')[0].value;
                var kmeans_n_init = document.getElementsByName('kmeans-n-init')[0].value;
                var kmeans_n_job = document.getElementsByName('kmeans-n-job')[0].value;
                var kmeans_max_iter = document.getElementsByName('kmeans-max-iter')[0].value;
                var kmeans_verbose = document.getElementsByName('kmeans-verbose')[0].value;

                if (kmeans_init !== '') {
                    dict_more.kmeans_init = kmeans_init;
                }
                if (kmeans_n_init !== '') {
                    dict_more.kmeans_n_init = kmeans_n_init;
                }
                if (kmeans_n_job !== '') {
                    dict_more.kmeans_n_job = kmeans_n_job;
                }
                if (kmeans_max_iter !== '') {
                    dict_more.kmeans_max_iter = kmeans_max_iter;
                }
                if (kmeans_verbose !== '') {
                    dict_more.kmeans_verbose = kmeans_verbose;
                }
            }
        }

        if (clusterers_[key_clusterer_] === 'dbscan') {
            if (document.getElementById('dbscan-python1').checked) {
                var dbscan_min_points_ = document.getElementsByName('dbscan-min-pts')[0].value;
                text_input_to_verify.push('dbscan-min-pts');
            }
            else {
                var min_pts = document.getElementsByName('dbscan-min-pts-min')[0].value;
                var max_pts = document.getElementsByName('dbscan-min-pts-max')[0].value;
                var step_pts = document.getElementsByName('dbscan-min-pts-step')[0].value;
                text_input_to_verify.push('dbscan-min-pts-min');
                text_input_to_verify.push('dbscan-min-pts-max');
                text_input_to_verify.push('dbscan-min-pts-step');

                dbscan_min_points_ = '[i for i in range(' + min_pts + ',' + max_pts + ',' + step_pts + ')]'
            }

            if (document.getElementById('dbscan-python2').checked) {
                var dbscan_eps_ = document.getElementsByName('dbscan-eps')[0].value;
                text_input_to_verify.push('dbscan-eps');
            }
            else {
                var min_eps = document.getElementsByName('dbscan-eps-min')[0].value;
                var max_eps = document.getElementsByName('dbscan-eps-max')[0].value;
                var step_eps = document.getElementsByName('dbscan-eps-step')[0].value;
                text_input_to_verify.push('dbscan-eps-min');
                text_input_to_verify.push('dbscan-eps-max');
                text_input_to_verify.push('dbscan-eps-step');

                dbscan_eps_ = '[i for i in range(' + min_eps + ',' + max_eps + ',' + step_eps + ')]';
            }

            dict.dbscan_min_points_ = dbscan_min_points_;
            dict.dbscan_eps_ = dbscan_eps_;

            // Get the additional configuration
            var dbscan_more_ = document.getElementById('dbscan-more').checked;
            if (dbscan_more_) {
                var dbscan_algorithm = document.getElementsByName('dbscan-algorithm')[0].value;
                var dbscan_leaf_size = document.getElementsByName('dbscan-leaf-size')[0].value;
                var dbscan_p = document.getElementsByName('dbscan-p')[0].value;

                if (dbscan_algorithm !== '') {
                    dict_more.dbscan_algorithm = dbscan_algorithm;
                }
                if (dbscan_leaf_size !== '') {
                    dict_more.dbscan_leaf_size = dbscan_leaf_size;
                }
                if (dbscan_p !== '') {
                    dict_more.dbscan_p = dbscan_p;
                }
            }
        }

        if (clusterers_[key_clusterer_] === 'agg') {
            if (document.getElementById('agg-python').checked) {
                var agg_k_ = document.getElementsByName('agg-k')[0].value;
                text_input_to_verify.push('agg-k');
            }
            else {
                var min_k_agg = document.getElementsByName('agg-k-min')[0].value;
                var max_k_agg = document.getElementsByName('agg-k-max')[0].value;
                var step_k_agg = document.getElementsByName('agg-k-step')[0].value;
                text_input_to_verify.push('agg-k-min');
                text_input_to_verify.push('agg-k-max');
                text_input_to_verify.push('agg-k-step');

                agg_k_ = '[i for i in range(' + min_k_agg + ',' + max_k_agg + ',' + step_k_agg + ')]'
            }
            var agg_link_ = document.getElementsByName('agg-link')[0].value;

            dict.agg_k_ = agg_k_;
            dict.agg_linkage_ = agg_link_;
        }

        dict.cluster_ = 'True';
    }

    // Get the configurations of the vectorizing module
    for (var key_vectorizer_ in vectorizers_) {
        if (vectorizers_[key_vectorizer_] === 'doc2vec') {
            if (document.getElementById('doc2vec-python1').checked) {
                var doc2vec_sizes_ = document.getElementsByName('doc2vec-vs')[0].value;
                text_input_to_verify.push('doc2vec-vs');
            }
            else {
                var min_vs = document.getElementsByName('doc2vec-vs-min')[0].value;
                var max_vs = document.getElementsByName('doc2vec-vs-max')[0].value;
                var step_vs = document.getElementsByName('doc2vec-vs-step')[0].value;
                text_input_to_verify.push('doc2vec-vs-min');
                text_input_to_verify.push('doc2vec-vs-max');
                text_input_to_verify.push('doc2vec-vs-step');

                doc2vec_sizes_ = '[i for i in range(' + min_vs + ',' + max_vs + ',' + step_vs + ')]'
            }

            if (document.getElementById('doc2vec-python2').checked) {
                var doc2vec_windows_ = document.getElementsByName('doc2vec-ws')[0].value;
                text_input_to_verify.push('doc2vec-ws');
            }
            else {
                var min_ws = document.getElementsByName('doc2vec-ws-min')[0].value;
                var max_ws = document.getElementsByName('doc2vec-ws-max')[0].value;
                var step_ws = document.getElementsByName('doc2vec-ws-step')[0].value;
                text_input_to_verify.push('doc2vec-ws-min');
                text_input_to_verify.push('doc2vec-ws-max');
                text_input_to_verify.push('doc2vec-ws-step');

                doc2vec_windows_ = '[i for i in range(' + min_ws + ',' + max_ws + ',' + step_ws + ')]'
            }
            dict.doc2vec_sizes_ = doc2vec_sizes_;
            dict.doc2vec_windows_ = doc2vec_windows_;

            // Get the additional configuration
            var doc2vec_more_ = document.getElementById('doc2vec-more').checked;
            if (doc2vec_more_) {
                var doc2vec_dm = document.getElementsByName('doc2vec-dm')[0].value;
                var doc2vec_alpha = document.getElementsByName('doc2vec-alpha')[0].value;
                var doc2vec_min_alpha = document.getElementsByName('doc2vec-min-alpha')[0].value;
                var doc2vec_min_count = document.getElementsByName('doc2vec-min-count')[0].value;
                var doc2vec_iter = document.getElementsByName('doc2vec-iter')[0].value;
                var doc2vec_negative = document.getElementsByName('doc2vec-negative')[0].value;

                if (kmeans_init !== '') {
                    dict_more.doc2vec_dm = doc2vec_dm;
                }
                if (kmeans_n_init !== '') {
                    dict_more.doc2vec_alpha = doc2vec_alpha;
                }
                if (doc2vec_min_alpha !== '') {
                    dict_more.doc2vec_min_alpha = doc2vec_min_alpha;
                }
                if (doc2vec_min_count !== '') {
                    dict_more.doc2vec_min_count = doc2vec_min_count;
                }
                if (doc2vec_iter !== '') {
                    dict_more.doc2vec_iter = doc2vec_iter;
                }
                if (doc2vec_negative !== '') {
                    dict_more.doc2vec_negative = doc2vec_negative;
                }
            }
        }

        if (vectorizers_[key_vectorizer_] === 'tfidf') {
            if (document.getElementById('tfidf-python').checked) {
                var tfidf_vector_sizes_ = document.getElementsByName('tfidf-vs')[0].value;
                text_input_to_verify.push('tfidf-vs');
            }
            else {
                var min_vs_tfidf = document.getElementsByName('tfidf-vs-min')[0].value;
                var max_vs_tfidf = document.getElementsByName('tfidf-vs-max')[0].value;
                var step_vs_tfidf = document.getElementsByName('tfidf-vs-step')[0].value;
                text_input_to_verify.push('tfidf-vs-min');
                text_input_to_verify.push('tfidf-vs-max');
                text_input_to_verify.push('tfidf-vs-step');

                tfidf_vector_sizes_ = '[i for i in range(' + min_vs_tfidf + ',' + max_vs_tfidf + ',' + step_vs_tfidf + ')]'
            }
            var tfidf_pca_ = document.getElementById('pca').checked;
            if (tfidf_pca_) {
                dict.tfidf_vector_sizes_pca_ = document.getElementsByName('tfidf-vs-pca')[0].value;
                text_input_to_verify.push('tfidf-vs-pca');
            }

            dict.tfidf_vector_sizes_ = tfidf_vector_sizes_;
            dict.tfidf_pca_ = trueToTrue(tfidf_pca_);
        }

        if (vectorizers_[key_vectorizer_] === 'pact') {
            //
        }

        dict.vectorize_ = 'True';
    }

    // Create the clustering/vectorizing combinations
    if (clustering_vectorizing_combs.length > 0) {
        dict.clustering_vectorizing_combs = '[' + clustering_vectorizing_combs + ']';
    }

    // Verify if all activated fields are filled
    var continue_ = true;
    for (var field_to_veriy in text_input_to_verify) {
        temp_ = document.getElementsByName(text_input_to_verify[field_to_veriy])[0];
        if (temp_.value === '') {
            temp_.setAttribute('class', 'required');
            continue_ = false;
        }
        else {
            temp_.setAttribute('class', null);
        }
    }

    // Conditional output message
    if (!continue_) {
        res_label = "Missing configuration: Default configuration generated";
        dict = create_default_config('main');
    }
    else {
        if (text_input_to_verify.length === 0) {
            res_label = "No configuration made: Default configuration generated";
        }
        else {
            res_label = "Generated configuration";
        }
    }

    // Format the final configurations (Main)
    for (var key in dict) {
        res_main_content = res_main_content + key + ":" + dict[key] + "\r\n";
    }

    // Format the final configurations (More)
    for (var key1 in dict_more) {
        res_more_content = res_more_content + key1 + ":" + dict_more[key1] + "\r\n";
    }

    document.getElementById("err-config").innerText = res_label;
    document.getElementById("config-main-content").value = res_main_content;
    document.getElementById("config-main-content").setAttribute("rows", "10");
    document.getElementById("config-more-content").value = res_more_content;
    document.getElementById("config-more-content").setAttribute("rows", "10");
    document.getElementById("config-main-").innerHTML = copyCB.outerHTML;
    document.getElementById("config-more-").innerHTML = copyCB_more.outerHTML;
    document.getElementById("script-main-").innerHTML = dlCB.outerHTML;
    document.getElementById("script-more-").innerHTML = dlCB_more.outerHTML;
    document.getElementById("script-content").setAttribute("rows", "10");
    document.getElementById("script-content").value = "python3 CREX_D.py PATH/TO/main_config PATH/TO/more_config";
}

// Create the configuration files
function create_crexc_config() {
    var dict = {};
    var text_input_to_verify = [];
    var res_label = '';
    var res_main_content = '';

    var texts = document.getElementsByTagName('input');
    var textareas = document.getElementsByTagName('TextArea');
    var selects = document.getElementsByTagName('select');


    // Get the text fields IDs
    for (var input in texts) {
        if (texts[input].type === 'text' || texts[input].type === 'number') {
            var temp = texts[input];
            dict[temp.id] = temp.value;
            text_input_to_verify.push(temp.id);
        }
    }

    // Get the select list IDs
    for (var input_s = 0; input_s < selects.length; input_s++) {
        var temp_s = selects[input_s];
        dict[temp_s.id] = temp_s.value;
        text_input_to_verify.push(temp_s.id);
    }

    // Get the textareas list IDs
    for (var input_ta = 0; input_ta < textareas.length; input_ta++) {
        if (textareas[input_ta].id !== 'script-content' && textareas[input_ta].id !== 'config-main-content') {
            var temp_ta = textareas[input_ta];
            dict[temp_ta.id] = temp_ta.value;
            text_input_to_verify.push(temp_ta.id);
        }
    }

    // Create the copy button
    var copyCB = document.createElement("input");
    copyCB.setAttribute("type", "button");
    copyCB.setAttribute("value", "Copy to clipboard");
    copyCB.setAttribute("class", "a2a_dd btn");
    copyCB.setAttribute("onclick", "copyToCB(this.id)");
    copyCB.setAttribute("id", "config-main-button");

    // Create the download button
    var dlCB = document.createElement("input");
    dlCB.setAttribute("type", "button");
    dlCB.setAttribute("value", "Download");
    dlCB.setAttribute("class", "btn");
    dlCB.setAttribute("id", "dl-main-button");
    dlCB.setAttribute("onclick", "download('main_config', 'config-main-content')");

    // Verify if all activated fields are filled
    var continue_ = true;
    for (var field_to_veriy in text_input_to_verify) {
        var temp_ = document.getElementById(text_input_to_verify[field_to_veriy]);
        if (temp_.value === '') {
            temp_.setAttribute('class', 'required');
            continue_ = false;
        }
        else {
            temp_.setAttribute('class', null);
        }
    }

    // Conditional output message
    if (!continue_) {
        res_label = "Missing configuration";
    }
    else {
        res_label = "Generated configuration";

        // Format the final configurations (Main)
        for (var key in dict) {
            res_main_content = res_main_content + key + "|" + dict[key].replace(/[\n\r]/g, ' ') + "\r\n";
        }


        document.getElementById("err-config").innerText = res_label;
        document.getElementById("config-main-content").value = res_main_content;
        document.getElementById("config-main-content").setAttribute("rows", "10");
        document.getElementById("config-main-").innerHTML = copyCB.outerHTML;
        document.getElementById("script-main-").innerHTML = dlCB.outerHTML;
        document.getElementById("script-content").setAttribute("rows", "10");
        document.getElementById("script-content").value = "python3 CREX_C.py PATH/TO/data.csv PATH/TO/config";
    }
}

// Create the fields in CREX-C UI
function create_fields(type) {

    document.getElementById(type + '-content').innerHTML = '';
    var num_of_elements = document.getElementById(type).value;
    var elements_array = [];

    // Create as much entries as needed
    for (var i = 0; i < num_of_elements; i++) {

        // Create the element container
        var element_container = document.createElement('div');
        element_container.setAttribute('class', 'col-sm-2');

        // Create the element text box that will contain th column number
        var element = document.createElement('input');
        element.setAttribute('id', type + '-' + i);
        element.setAttribute('type', 'number');
        element.setAttribute('placeholder', 'Col. for ' + type + ' ' + (i + 1));
        element_container.appendChild(element);
        // for MCQ and OAQ add a te get the number of answers
        if (type === 'mcq') {
            var element_2 = document.createElement('input');
            element_2.setAttribute('id', type + '-o-' + i);
            element_2.setAttribute('type', 'number');
            element_2.setAttribute('placeholder', 'Num of options');
            element_container.appendChild(element_2);
        }
        elements_array.push(element_container);
    }
    // update the form
    for (var element_ in elements_array) {
        document.getElementById(type + '-content').innerHTML += elements_array[element_].outerHTML;

    }
}

// Copy to clipboard
function copyToCB(id) {

    // get the config text field
    var copyText = document.getElementById('config-' + id.split('-')[1] + '-content');
    // select text
    copyText.select();
    // copy text
    document.execCommand("Copy");
}

// Copy to clipboard
function copyToCBDiv(id) {

    // get the config text field
    var copyText = document.getElementById('config-' + id.split('-')[1] + '-content');

    // select text stupid work around
    temp = document.createElement('textarea');
    copyText.appendChild(temp);
    temp.innerText = copyText.innerText;
    temp.select();

    // copy text
    document.execCommand("Copy");
    copyText.removeChild(temp);
    not = document.getElementById("notification");
    not.innerHTML = '<div class="alert alert-info fade in title">Copied</div>';
    window.setTimeout(function() {
        $(".alert").fadeTo(500, 0).slideUp(500, function(){
            $(this).remove();
        });
    }, 1000);
}

// Download file : adapted from https://tinyurl.com/y7tlbzhs
function download(filename, text_id) {
    var text = document.getElementById(text_id).value;
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}
