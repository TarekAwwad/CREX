
# CREX : CReate, Enrich, eXtend for crowdsourcing evaluation datasets

CREX (CReate, Enrich, eXtend) is a framework allowing the creation the extension and the enrichment of crowdsourcing datasets such as CrowdED. CREX allows a clustering based tasks selection and the generation of crowdsourcing campaign sites. Code is in Python for the computational parts and in Javascript for the campaign generation tool.

## Getting started
#### 1. Platform installation :
To start using the components of Project_Crowd start by cloning the project using:

```
git clone https://github.com/Project-Crowd/CREX.git
```

Note : Each directory in Project_Crowd is a standalone structure and can be downloaded and run separately

#### 2. Dependencies :
The code is developped in [Python](https://www.python.org/) v3.5.2. The following packages are needed:

1. scikit-learn : http://scikit-learn.org/stable/ (clustering and evaluation measures)
2. pandas : http://pandas.pydata.org/ (data structure and matrix handling)
3. scipy : https://www.scipy.org/ (scientific computing library)
4. numpy : http://www.numpy.org/ (scientific computing library)
5. seaborn : https://seaborn.pydata.org/ (data visualization)
6. nltk : https://www.nltk.org/ (natural language processing)
7. gensim : https://radimrehurek.com/gensim/ (doc2vec implementation)
8. termcolor : https://pypi.python.org/pypi/termcolor (visual console output)

To install all dependencies at once run the command:
```
cd CREX
pip3 install -r dependencies
```
## Project Structure
```
CREX
|-- CREXC : contains the code for the campaign generation modules
|   |-- CREX_C.py : The main module of CREXC
|   |-- config : The configuration file of CREXC
|   `-- Campaign : The campaign site data and structure
|	   |-- PrivateConfig : contains the private config of the database
|	   `-- UI : contains the user interface elements and data of the campaign site
|-- CREXD : contains the code for the computational core of CREX.
|   |-- VM.py : The vectorizing Module
|   |-- CM.py : The Clustering Module
|   |-- SM.py : The Sampling Module
|   |-- EM.py : The Evaluation Module
|   |-- CREX_D.py : The main module of CREXD
|   |-- Tools.py : Divers tools for data manipulation
|   |-- main_config : The level 1 configurations of CREXD
|   |-- more_config : The level 2 configurations of CREXD
`-- UI :  contains the user interface elements and data of the configuration panel
`-- TestData : Test data for the modules
|    `-- 20news : A subset of the 20News data set to test the clustering
|    `-- TaskCorpus : A subset of the task corpus to test CREXD (end-to-end)
|    `-- Test_campain_generation : a sample task input file to test CREXC
`-- dependencies : The python library dependencies list    
```



## Tutorial
To configure the modules of CREX a web configuration panel is provided here [CREX configuration panel](https://project-crowd.eu/)
### CREXD
**Step 1: Configure -** CREXD consists of standalone modules. They can be used together or separately to achieve different clustering, vectorizing, sampling and task selection steps. In order to use one or more module of CREX at a time, the [CREXD configuration panel](https://project-crowd.eu/CREX-D.html) can be used.  

Here is a list of the configurable parameters of CREXD:

|parameter name| values | description |
| ------------- |:-------------:|-----|
preprocess_| [True/False]| preprocess the data or not, i.e., tokenize/stemm/train the vectorizer models. If False a pre-processed data folder should be given.|
vectorize_| [True/False]| compute the feature vectors or not, e.g., TFIDF transform. If False a pre-processed data folder should be given.|
|cluster_| [True/False]| run CM or not.|
|sample_| [True/False]| run SM or not.|
|evaluate_| [True/False]| run EM or not.|
|distance_metric_| [euclidean/cosine]| distance metric to be used by CM.|
|doc_sample_sizes| [array of size 1]**| e.g. [1000] If a large corpus is used to train the vectorizers, a subsample of this corpus can be vectorized and clustered if needed |
|preprocess_tfidf| [True/False]| whether to train the TFIDF vectorizer or not|
|preprocess_doc2vec| [True/False]| whether to train the Doc2Vec vectorizer or not|
|different_custering_data|[True/False]| whether to use a corpus different from the one used for training the models or not|
|n_clustering_processes| [integer]| (range depends on your computer). Number of processes for the parallel execution of the clustering|
|n_evaluation_processes|[integer]| (range depends on your computer). Number of processes for the parallel execution of the evaluation|
|kmeans_k_|[array of values/PARI]*| number of cluster for Kmeans. |
|minibatch_km_|[0/INTEGER]| if O minibatch is not used, else minibatch is run with the given batch size|
|dbscan_min_points_|[array of values/PARI]*| the minimum point parameter of DBSCAN|
|dbscan_eps_|[array of values/PARI]*| the EPSILON parameter of DBSCAN|
|agg_k_|[array of values/PARI]*| number of cluster for the agglomerative clustering.|
|agg_linkage_|['ward', 'complete', 'average']| the linkage parameter of the agglomerative clustering.|
|doc2vec_sizes_|[array of size 1]**| size of produced Doc2vec vectors|
|doc2vec_windows_|[array of size 1]**| size of used Doc2vec window|
|tfidf_vector_sizes_|[array of size 1]** |size of produced TFIDF vectors|
|tfidf_pca_|[True/False]| whether to use PCA dimension reduction or not|
|tfidf_vector_sizes_pca_|[array of size 1]| size of the PCA vector|
|sampling_fitness|[rmse/minmax]| the objective function of the dampling algorithm|
|max_sample_size_|[INTEGER]| size of output sample ("S" in the draft)|
|min_samples_per_cluster_|[INTEGER]| minimum sample size per cluster ("th" in the draft)|
|max_sampling_iteration_|[INTEGER]| maximum number of itterations ("itt" in the draft)|
|eva_measures|[array of ('hcv'/'sil'/'coc')]| the evaluation measres to compute by the EM |
|eva_vectorizing_models|['tfidf'/'doc2vec']| the vectorizing modules to evaluate|
|eva_clustering_models|['kmeans'/'agg'/'dbscan']| the clustering modules to evaluate|
|result_folder|[PATH string]| a path to the output folder|
|raw_data_folder|[PATH string]| a path to the input data folder|
|preprocessed_location|[PATH string]| a path to the preprocessed data folder|
|raw_clustering_data_folder|[PATH string]| a path to the data to cluster if (different_custering_data is True)|
|clustering_vectorizing_combs|[array of ('clustModel_vectModel')]| e.g. ['kmeans_tfidf', 'dbscan_doc2vec'] tells the VM and CM what models to train |
```
PARI = python array range initialization e.g [i for i in range(1,2,3)]
* the algorithm is run len(array) times.
** (array is used to allow future implementation of multi config study)
```
#### For the following configurations detailed information can be found in the [Sklearn](http://scikit-learn.org/stable/) library
|parameter name| values |
| ------------- |:-------------:|
kmeans_init|['kmeans++'/'random']
kmeans_n_init|INTEGER
kmeans_n_job|INTEGER
kmeans_max_iter|INTEGER
kmeans_verbose|INTEGER
dbscan_algorithm|['auto'/'brute']
dbscan_leaf_size|None
dbscan_p|INTEGER
#### For the following configurations detailed information can be found in the [Gensim](https://radimrehurek.com/gensim/) library
|parameter name| values |
| ------------- |:-------------:|
doc2vec_dm|INTEGER
doc2vec_alpha|FLOAT
doc2vec_min_alpha|FLOAT
doc2vec_min_count|INTEGER
doc2vec_iter|INTEGER
doc2vec_negative|INTEGER


**Step 2: Run -**
The configuration panel allows you to download 2 configuration files : main_config and more_config. After downloading these file launch the following command in your terminal in order to launch CREXD:

```
> python3 CREX_D.py [PATH/TO/]main_sconfig [PATH/TO/]more_config
```

### CREXC
**Step 1: Run -**
CREXC allows to format your raw data csv file to be used by the campaign site. In order to structure these raw data, use the [CREXC configuration panel](http://project-crowd.eu/CREX-C.html). It consists of a configuration generation tool that takes the users data description and generate a structured output of them.

**Step 2: Run -**
The configuration panel allows you to download 2 configuration files : main_config and more_config. After downloading these file launch the following command in your terminal in order to launch CREXD:

```
> python3 CREX_C.py [PATH/TO/]data.csv [PATH/TO/]config
```
## References

Temporarily private Figshare, DOI and reference:
- URL: https://figshare.com/s/ca41a59f73c092385fc3
- Reference to cite:
	- [1] Tarek Awwad, Nadia Bennani, Veronika Rehn-Sonigo, Lionel Brunie and Harald Kosch CrowdED and CREX : Towards 		Easy Crowdsourcing Quality Control Evaluation ADBIS 2019, Bled - Slovenia

	- [2]Tarek AWWAD.. 2018. CREX : CReate, Enrich, eXtend for crowdsourcing evaluation datasets. 		
