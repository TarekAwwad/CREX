#!/usr/bin/python

# Import modules for CGI handling
import cgi

# Default config
doc_sample_sizes = [80000]
vectorize_ = True
sample_ = True
evaluate_ = False
preprocess_ = True
preprocess_tfidf = True
preprocess_doc2vec = True
different_custering_data = False
preprocessed_location = "''"

kmeans_k_ = []
minibatch_km_ = None
dbscan_eps_ = []
dbscan_min_points_ = []
dbscan_metric_ = ''
agg_k_ = []
agg_linkage_ = ['ward']

doc2vec_windows_ = [5]
doc2vec_sizes_ = [50]
tfidf_vector_sizes_ = [20000]
tfidf_vector_sizes_pca_ = [500]

clustering_vectorizing_combs = []

n_clustering_processes = 1
n_evaluation_processes = 4

max_sample_size_ = 450
min_samples_per_cluster_ = 30
max_sampling_iteration_ = 4000

# clustering and vectorizing options
clusterer_ids = ['km', 'db', 'ag']
vectorizer_ids = ['tfidf', 'doc2vec', 'pact']
clusterers_ = []
vectorizers_ = []

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Run option
run_option = form.getvalue('run-option')

if form.getvalue('custom') == 'True':
    doc_sample_sizes = "[" + form.getvalue('sample-s') + "]"
    dbscan_metric_ = form.getvalue('distance-metric')
    evaluate_ = form.getvalue('evaluate') == 'True'
    preprocess_ = form.getvalue('process') == 'True'
    vectorize_ = form.getvalue('vectorize') == 'True'
    sample_ = form.getvalue('sample') == 'True'

    if preprocess_:
        preprocess_tfidf = form.getvalue('process-doc2vec') == 'True'
        preprocess_doc2vec = form.getvalue('process-tfidf') == 'True'

    else:
        preprocessed_location = form.getvalue('preprocessed-location')

    different_custering_data = form.getvalue('diffdata')

    if form.getvalue('advanced') == 'True':
        n_clustering_processes = form.getvalue('n-clustering-processes')
        n_evaluation_processes = form.getvalue('n-evaluation-processes')
    else:
        n_clustering_processes = 1
        n_evaluation_processes = 4

    if sample_:
        max_sample_size_ = form.getvalue('max-sample-size')
        min_samples_per_cluster_ = form.getvalue('min-samples-per-cluster')
        max_sampling_iteration_ = form.getvalue('max-sampling-iteration')

for clusterer_id in clusterer_ids:
    temp_ = form.getvalue(clusterer_id)
    if temp_ != None:
        clusterers_.append(temp_)

for vectorizer_id in vectorizer_ids:
    temp_ = form.getvalue(vectorizer_id)
    if temp_ != None:
        vectorizers_.append(temp_)

for clusterer_ in clusterers_:
    for vectorizer_ in vectorizers_:
        clustering_vectorizing_combs.append(clusterer_ + '_' + vectorizer_)

if 'kmeans' in clusterers_:
    if form.getvalue('kmeans-python') == 'True':
        kmeans_k_ = form.getvalue('kmeans-k')
    else:
        min_k = form.getvalue('kmeans-k-min')
        max_k = form.getvalue('kmeans-k-max')
        step_k = form.getvalue('kmeans-k-step')
        kmeans_k_ = '[i for i in range(' + min_k + ',' + max_k + ',' + step_k + ')]'

    minibatch_km_ = form.getvalue('kmeans-mb')

if 'dbscan' in clusterers_:
    if form.getvalue('dbscan-python1') == 'True':
        dbscan_min_points_ = form.getvalue('dbscan-min-pts')
    else:
        min_pts = form.getvalue('dbscan-min-pts-min')
        max_pts = form.getvalue('dbscan-min-pts-max')
        step_pts = form.getvalue('dbscan-min-pts-step')
        dbscan_min_points_ = '[i for i in range(' + min_pts + ',' + max_pts + ',' + step_pts + ')]'

    if form.getvalue('dbscan-python2') == 'True':
        dbscan_eps_ = form.getvalue('dbscan-eps')
    else:
        min_eps = form.getvalue('dbscan-eps-min')
        max_eps = form.getvalue('dbscan-eps-max')
        step_eps = form.getvalue('dbscan-eps-step')
        dbscan_eps_ = '[i for i in np.arange(' + min_eps + ',' + max_eps + ',' + step_eps + ')]'

if 'agg' in clusterers_:
    if form.getvalue('agg-python') == 'True':
        agg_k_ = form.getvalue('agg-k')

    else:
        min_k = form.getvalue('agg-k-min')
        max_k = form.getvalue('agg-k-max')
        step_k = form.getvalue('agg-k-step')
        agg_k_ = '[i for i in range(' + min_k + ',' + max_k + ',' + step_k + ')]'

    agg_linkage_ = "['" + form.getvalue('agg-link') + "']"

if 'tfidf' in vectorizers_:
    if form.getvalue('tfidf-python') == 'True':
        tfidf_vector_sizes_ = form.getvalue('tfidf-vs')
    else:
        min_vs = form.getvalue('tfidf-vs-min')
        max_vs = form.getvalue('tfidf-vs-max')
        step_vs = form.getvalue('tfidf-vs-step')
        tfidf_vector_sizes_ = '[i for i in range(' + min_vs + ',' + max_vs + ',' + step_vs + ')]'

    pca = form.getvalue('pca')
    if pca == 'True':
        tfidf_vector_sizes_pca_ = form.getvalue('tfidf-vs-pca')

if 'doc2vec' in vectorizers_:

    if form.getvalue('doc2vec-python1') == 'True':
        doc2vec_sizes_ = form.getvalue('doc2vec-vs')
    else:
        min_vs = form.getvalue('doc2vec-vs-min')
        max_vs = form.getvalue('doc2vec-vs-max')
        step_vs = form.getvalue('doc2vec-vs-step')
        doc2vec_sizes_ = '[i for i in range(' + min_vs + ',' + max_vs + ',' + step_vs + ')]'

    if form.getvalue('doc2vec-python2') == 'True':
        doc2vec_windows_ = form.getvalue('doc2vec-ws')
    else:
        min_ws = form.getvalue('doc2vec-ws-min')
        max_ws = form.getvalue('doc2vec-ws-max')
        step_ws = form.getvalue('doc2vec-ws-step')
        doc2vec_windows_ = '[i for i in range(' + min_ws + ',' + max_ws + ',' + step_ws + ')]'

if 'pact' in vectorizers_:
    a = None
    a = None

f = open('config', 'w')

f.write("evaluate_:%s\n" % (evaluate_))
f.write("vectorize_:%s\n" % (vectorize_))
f.write("sample_:%s\n" % (sample_))
f.write("preprocess_:%s\n" % (preprocess_))
f.write("preprocess_tfidf:%s\n" % (preprocess_tfidf))
f.write("preprocess_doc2vec:%s\n" % (preprocess_doc2vec))
f.write("preprocessed_location:%s\n" % (preprocessed_location))
f.write("different_custering_data:%s\n" % (different_custering_data))
f.write("doc_sample_sizes:%s\n" % (doc_sample_sizes))
f.write("metric_:%s\n" % (dbscan_metric_))
f.write("clustering_vectorizing_combs:%s\n" % (clustering_vectorizing_combs))
f.write("kmeans_k_:%s\n" % (kmeans_k_))
f.write("minibatch_km_:%s\n" % (minibatch_km_))
f.write("dbscan_eps_:%s\n" % (dbscan_eps_))
f.write("dbscan_min_points_:%s\n" % (dbscan_min_points_))
f.write("agg_k_:%s\n" % (agg_k_))
f.write("agg_linkage_:%s\n" % (agg_linkage_))
f.write("tfidf_vector_sizes_:%s\n" % (tfidf_vector_sizes_))
f.write("tfidf_vector_sizes_pca_:%s\n" % (tfidf_vector_sizes_pca_))
f.write("doc2vec_windows_:%s\n" % (doc2vec_windows_))
f.write("doc2vec_sizes_:%s\n" % (doc2vec_sizes_))
f.write("n_clustering_processes:%s\n" % (n_clustering_processes))
f.write("n_evaluation_processes:%s\n" % (n_evaluation_processes))
f.write("max_sample_size_:%s\n" % (max_sample_size_))
f.write("min_samples_per_cluster_:%s\n" % (min_samples_per_cluster_))
f.write("max_sampling_iteration_:%s\n" % (max_sampling_iteration_))

if run_option == 'Launch script':
    # Code to run the script : On the server?
    0


print("Content-type:text/html\n\n")
print("<html>")
print("<head>")
print("<meta charset='UTF-8'> \n"
      "<meta name='viewport' content='width=device-width, initial-scale=1.0'> \n"
      "<!-- =========================== \n"
      "SITE TITLE \n"
      "=========================== --> \n"
      "<title>Project crowd</title> \n"
      "<!-- =========================== \n"
      "FAVICONS \n"
      "=========================== --> \n"
      "<link rel='icon' href='WebUI/img/logo.png'> \n"
      "<!-- =========================== \n"
      "STYLESHEETS \n"
      "=========================== --> \n"
      "<link rel='stylesheet' href='//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/css/bootstrap.min.css'> \n"
      "<link rel='stylesheet' href='UI/css/style.css'> \n"
      "<link rel='stylesheet' href='UI/css/responsive.css'> \n"
      "<!-- =========================== \n"
      "FONTS & ICONS \n"
      "=========================== --> \n"
      "<link rel='stylesheet' href='//fonts.googleapis.com/css?family=Kristi|Alegreya+Sans:300' type='text/css'> \n"
      "<link rel='stylesheet' href='//maxcdn.bootstrapcdn.com/font-awesome/4.2.0/css/font-awesome.min.css'> \n"
      "<!--[if IE]> \n"
      "<script src='https://cdn.jsdelivr.net/html5shiv/3.7.2/html5shiv.min.js'></script> \n"
      "<script src='https://cdn.jsdelivr.net/respond/1.4.2/respond.min.js'></script> \n"
      "<![endif]--> \n")
print("</head>")

print("<body>")
print("<div class='container'>")
print("<div class='row'>")
print("<h2>A file with the following configurations has been created: </h2>")
print("<div class='list-group-item'>")
print(" evaluate_ : %s <br/>" % (evaluate_))
print(" preprocess_ : %s <br/>" % (preprocess_))
print(" preprocess_tfidf : %s <br/>" % (preprocess_tfidf))
print(" preprocess_doc2vec : %s <br/>" % (preprocess_doc2vec))
print(" preprocessed_location : %s <br/>" % (preprocessed_location))
print(" different_custering_data : %s <br/>" % (different_custering_data))
print(" doc_sample_sizes : %s <br/> " % (doc_sample_sizes))
print(" dbscan_metric_ : %s <br/> " % (dbscan_metric_))
print(" clustering_vectorizing_combs : %s <br/> " % (clustering_vectorizing_combs))
print(" kmeans_k_ : %s <br/> " % (kmeans_k_))
print(" minibatch_km_ : %s <br/> " % (minibatch_km_))
print(" dbscan_eps_ : %s  <br/> " % (dbscan_eps_))
print(" dbscan_min_points_ : %s <br/> " % (dbscan_min_points_))
print(" agg_k_ : %s  <br/> " % (agg_k_))
print(" dbscan_min_points_ : %s <br/> " % (agg_linkage_))
print(" tfidf_vector_sizes_ : %s <br/> " % (tfidf_vector_sizes_))
print(" tfidf_vector_sizes_pca_ : %s <br/> " % (tfidf_vector_sizes_pca_))
print(" doc2vec_windows_ : %s <br/> " % (doc2vec_windows_))
print(" doc2vec_sizes_ : %s <br/> " % (doc2vec_sizes_))
print("</div>")
print("</div><br/>")
print("<div id='rerun' class='col-sm-11 text-right dl-share'>"
      "<input type='button' onclick='location.href=\"UI/index.html\";' class='a2a_dd btn btn-default' value='Back'/>"
      "</div>")
print("</div>")
print("</body>")
print("</html>")
