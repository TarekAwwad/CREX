import os
import re
import csv
import random
import gensim

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from multiprocessing import Pool
from sklearn import decomposition
from sklearn.externals import joblib
from stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim.models.doc2vec import TaggedDocument


# Tokenizer configurations
tokenizer = RegexpTokenizer(r'\w+')
en_stop = get_stop_words('en')
p_stemmer = PorterStemmer()


# read a csv file to a data array
def read_csv_file(file_url, sep, header):
    with open(file_url, 'r') as csvfile:
        data = list(csv.reader(csvfile, delimiter=sep))
    if header:
        return np.array(data[1:])
    else:
        return np.array(data)


# write a data array in a csv file
def write_csv_file(file_url, sep, data):
    with open(file_url, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=sep, quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            writer.writerow([row[i] for i in range(len(row))])
    return file_url


# folder name incrementer
def increment_folder_name(path):
    path = os.path.abspath(path)

    # if not os.path.exists(path):
    #     return path, '_'

    root, ext = os.path.splitext(os.path.expanduser(path))
    dir = os.path.dirname(root)
    fname = os.path.basename(root)
    candidate = fname + ext
    index = 0
    ls = set(os.listdir(dir))
    while candidate in ls:
        candidate = "{}_{}{}".format(fname, index, ext)
        index += 1
    return os.path.join(dir, candidate), candidate


# scorer test
def average_predicted_value(y, y_pred, **kwargs):
    return np.mean(np.array(y_pred)) - np.mean(y)


# Custom
def pick_line_by_id(file_url_list, id_list):
    for file_url in file_url_list:
        picked_line_temp = []
        file_pref = file_url.split('_')[0]
        with open(file_url, 'r') as csvfile:
            data = list(csv.reader(csvfile, delimiter="|"))[1:]
            for id in id_list:
                for line in data:
                    line_id_data = line[0].split('_')
                    if line_id_data[0] == file_pref and id == line_id_data:
                        picked_line_temp.append(line[1])

        write_csv_file(file_url.split('.')[0] + 'sampled.csv', picked_line_temp)

    return


# Tokenizer functions
def tok_stem_num(raw):
    # clean and tokenize document string
    idx = raw.split(',')[0]
    raw1 = raw.lower().split(',')[1:]

    # print(raw, '\n', idx, '\n', ' '.join(raw1))

    tokens = tokenizer.tokenize(' '.join(raw1))

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if i not in en_stop]

    # remove numbers
    number_tokens = [re.sub(r'[\d]', ' ', i) for i in stopped_tokens]
    number_tokens = ' '.join(number_tokens).split()

    # stemm
    stemmed_tokens = [p_stemmer.stem(i) for i in number_tokens]

    # remove short tokens
    length_tokens = [i for i in stemmed_tokens if len(i) > 1]

    td = gensim.utils.to_unicode(str.encode(' '.join(length_tokens))).split()

    # print(idx, td)

    return idx, td


# Parallel tokenizer
def tokenize_p(t_doc_list, t_output_data_folder, t_desc):
    p = Pool()
    t_doc = list(p.map(tok_stem_num, t_doc_list))
    p.close()

    f = open(t_output_data_folder + '/tokenized/' + t_desc + '_tokenized.txt', 'w+', encoding='utf-8')
    for idx, i in t_doc:
        f.write(str(idx) + str(i) + '\n')

    return t_doc


def get_doc_list_file(file_name):
    doc_list = []
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            print(line)
            doc_list.append(line)
    return doc_list


def get_doc_list_folder(folder_name):
    doc_list = []

    # Fetch all files in the folder
    file_list_raw = [name for name in os.listdir(folder_name) if name.endswith('.txt')]

    # Read all document from all files
    for file in file_list_raw:
        pre = file.split('_')[0]
        with open(folder_name + '/' + file, 'r', encoding='utf-8') as f:
            next(f)
            for line in f:
                doc_list.append(pre + '_' + line)

    # print('Found %s files and %s documents in %s\t ... \t' % (len(file_list_raw), len(doc_list), folder_name), end='')

    return doc_list


def get_doc(gd_folder_name, gd_output_data_folder):
    doc_list = get_doc_list_folder(gd_folder_name)

    taggeddoc = []

    texts = []
    for index, i in enumerate(doc_list):
        # For tagged doc
        wordslist = []
        tagslist = []

        # Remove short tokens
        length_tokens = tok_stem_num(i)

        # Add tokens to list
        texts.append(length_tokens)

        # Create tagged documents list
        td = TaggedDocument(gensim.utils.to_unicode(str.encode(' '.join(length_tokens))).split(), [str(index)])
        tagslist.append(str(index))
        wordslist.append(length_tokens)
        taggeddoc.append(td)

    joblib.dump(taggeddoc, gd_output_data_folder + '/vectorized/data_doc2vec', compress=1)

    return taggeddoc


# Fetches all tasks found in a folder and format them into tagged documents
def get_doc_p(gdp_folder_name, gdp_output_data_folder, for_="doc2vec"):
    doc_list = get_doc_list_folder(gdp_folder_name)
    taggeddoc = []
    task_ids = []
    doc2 = tokenize_p(doc_list, gdp_output_data_folder, str(1))

    if for_ == "doc2vec":
        for index, i in doc2:
            task_ids.append(str(index))
            td = TaggedDocument(i, [str(index)])
            taggeddoc.append(td)
        joblib.dump(taggeddoc, gdp_output_data_folder + '/vectorized/data_doc2vec', compress=1)

    if for_ == "tfidf":
        for index, i in doc2:
            task_ids.append(str(index))
            taggeddoc.append([' '.join(i), [index]])
        joblib.dump(taggeddoc, gdp_output_data_folder + '/vectorized/data_tfidf', compress=1)

    joblib.dump(task_ids, gdp_output_data_folder + '/vectorized/task_ids', compress=1)

    return taggeddoc


# Configurable plotting function - Unfinished
def plot_results(pr_r, pr_l, pr_output_data_folder, title, opt_='2d', data_col=2, annot_=True):
    sns.set_style("whitegrid")
    sns.color_palette("husl", 16)
    sns.set_palette("husl")
    sns.set(font_scale=0.8)
    markers = ['<', '>', '8', 's', 'o', 'v', '^', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']

    if opt_ == '2d':
        fig, ax1 = plt.subplots(1, 1)
        pr_r.sort(key=lambda x: x[0])
        x = [i[0] for i in pr_r]
        x_labels = range(min(x), max(x), round(max(x) / 20))
        y_labels = np.arange(0, 1.1, 0.1)

        for l in range(1, len(pr_l)):
            ax1.plot(x, [i[l] for i in pr_r], label=pr_l[l], marker=markers[l], markersize=6)

        plt.legend()
        plt.suptitle(title)

        plt.xlabel('Number of cluster')
        plt.xticks(x_labels)

        plt.ylabel('Score')
        plt.yticks(y_labels)

    if opt_ == '3d':
        # TODO FIX : not Totally OK
        fig = plt.figure()
        ax1 = fig.add_subplot(111, projection='3d')
        x = [i[0] for i in pr_r]
        y = [i[1] for i in pr_r]

        for l in range(2, len(pr_l) - 1):
            z = [i[l] for i in pr_r]
            ax1.scatter(x, y, z, marker=markers[l])

    if opt_ == 'heatmap':
        x = [float(i[0]) for i in pr_r]
        y = [float(i[1]) for i in pr_r]
        intensity = [float(i[data_col]) for i in pr_r]

        # seaborn heatmaps work better with pandas dataframe
        df = pd.DataFrame.from_dict(np.array([x, y, intensity]).T)

        x_value = pr_l[0]
        y_value = pr_l[1]
        z_value = pr_l[data_col]

        df.columns = [x_value, y_value, z_value]
        df[z_value] = pd.to_numeric(df[z_value])

        pivotted = df.pivot(x_value, y_value, z_value)
        sns.heatmap(pivotted, cmap='RdBu_r', annot=annot_, fmt='g', annot_kws={"size": 5}, linewidths=.5, cbar_kws={'label': z_value})
        plt.yticks(rotation=0)
        plt.xticks(rotation=90)

    plt.savefig(pr_output_data_folder + title, dpi=1000)
    return 0


# Plots data contained in a file
def plot_data_from_file(pdff_file, pdff_title, pdff_data_col, pdff_opt_='heatmap', sep_=' ', annot_=True):
    data = read_csv_file(pdff_file, sep_, False)
    header = data[0]
    data = data[1:]
    plot_results(data, header, '', pdff_title, opt_=pdff_opt_, data_col=pdff_data_col, annot_=annot_)


# Reduces dimension with PCA and plots word2vec models
def plot_words(w2v):
    words_np = []
    # A list of labels (words)
    words_label = []
    for word in w2v.vocab.keys():
        words_np.append(w2v[word])
        words_label.append(word)
    print('Added %s words. Shape %s' % (len(words_np), np.shape(words_np)))

    pca = decomposition.PCA(n_components=2)
    pca.fit(words_np)
    reduced = pca.transform(words_np)

    a = random.sample(list(reduced), 200)
    # a_dict = {key: value for (key, value) in a}

    # plt.plot(pca.explained_variance_ratio_)
    for index, vec in enumerate(a):
        # print ('%s %s'%(words_label[index],vec))
        # if 2000 > index > 1000:
        x, y = vec[0], vec[1]
        # print(words_label[index])
        plt.scatter(x, y)
        plt.annotate(words_label[index], xy=(x, y))
    plt.show()
