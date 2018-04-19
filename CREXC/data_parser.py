import csv
import operator
import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder


# read a csv file to a data array
def read_csv_file(file_url, sep, header):
    with open(file_url, 'r') as csvfile:
        data_ = list(csv.reader(csvfile, delimiter=sep))
    if header:
        return np.array(data_[1:]), data_[0]
    else:
        return np.array(data_)


# Takes the raw contribution file (contribution_ID, ..., time_for_set ) and an output file
# For each worker write times into out_file (worker_ID, time_set1, ... time_setn, avg_time, min_time, max_time, median)
def parallelize_time_per_set(in_file, out_file):
    # Read the contribution into a dataframe
    task_data = pd.read_csv(in_file, sep=",", quotechar='"', header=0).drop_duplicates(['worker_ID', 'task_ID'],
                                                                                       keep='first')

    # Get only the needed columns
    time_data = task_data[['task_ID', 'worker_ID', 'time_to_complete']]

    # Drop duplicate lines (in case they existe for sme reason)
    time_data_nd = time_data.drop_duplicates(['worker_ID', 'task_ID'], keep='first', inplace=False)

    # Index the dataframe by worker_ID
    time_data_nd = time_data_nd.set_index('worker_ID')

    # Create a new dataframe to hold the output data. One column for workerd ID and one column per task set
    data_nd = pd.DataFrame(index=time_data.worker_ID.unique(), columns=time_data.task_ID.unique())
    data_nd.index.name = 'worker_ID'

    # Fill in the time (line[1]) per worker (index) per task set (line[0])
    for index, line in time_data_nd.iterrows():
        data_nd[line[0]][index] = int(line[1])

    # Add time statistic columns
    data_nd['average_time_cont'] = data_nd.mean(axis=1)
    data_nd['min'] = data_nd.min(axis=1)
    data_nd['max'] = data_nd.max(axis=1)
    data_nd['median'] = data_nd.median(axis=1)
    data_nd['count'] = data_nd.count(axis=1) - 4

    # Ignore some invalid time measurements
    data_nd[data_nd < 0] = np.nan

    # Open out_file to write results
    f = open(out_file, 'w')
    f.write('worker_ID,' + ','.join(list(data_nd)) + '\n')

    for index, line in data_nd.iterrows():
        f.write(index + ',' + ','.join([str(el) for el in line]) + '\n')

    return out_file


# Takes a contribution file in_file, and output file out_file and a file with translation from str to numerical task IDs
# Translate the str task IDs into numerical IDs and write new data into out_file. If mcq only MCQ questions are written
def translate_task_ids(in_file, out_file, dict_file, mcq):
    # Read the list of IDs and create a dictionary for easier access
    list_ids_ = read_csv_file(dict_file, ',', True)[0]
    dict_ids = dict()
    for row in list_ids_:
        dict_ids[row[0]] = row[1]

    # Read the contribution file
    task_data = read_csv_file(in_file, ',', True)[0]

    # Open out_file to write results and write the headers
    f = open(out_file, 'w')
    f.write('worker_ID,task_ID,contribution' + '\n')

    # Re-write the lines of in_file while changing the task_IDs into its numerical equivalent from the ID dictionary
    if mcq:
        for line in task_data:
            if line[1] != 'codec' and 'ft' not in line[1]:
                f.write(','.join([line[0], dict_ids[line[1]], line[2]]) + '\n')

    return out_file


# Takes a file with translation from str to numerical task IDs
# Return a set of tasks set IDs (sets are inferred from str IDs built like : setID_hitID_questionID)
def parse_task_set_id(dict_file):
    # Read in_file
    list_ids_ = read_csv_file(dict_file, ',', True)[0]
    a = []

    # The first three characters of the numerical ID are the identifier of each task set
    for row in list_ids_:
        a.append(row[1][:3])

    return np.unique(a)


# Takes a contribution file in_file, an output file prefix, and a file with translation from str to numerical task IDs
# Splits in_file into multiple files containing the contributions for one task set each
def file_per_task_set(in_file, out_file, dict_file):
    # get the task sets IDs
    ids_ = parse_task_set_id(dict_file)

    # Read the contribution file
    data_ = read_csv_file(in_file, ',', True)[0]

    # Shuffle the data : TODO: WHY DID I DO THIS?
    np.random.shuffle(data_)

    # for each task set
    for id_ in ids_:
        # Open a new file to write the task set contributions:
        f = open(out_file + id_ + '.csv', 'w')

        # Write the rows of the current task set into the output file
        for row in data_:
            if row[1][:3] == id_:
                f.write(','.join(row) + '\n')
        f.close()

    return out_file


# Takes the raw contribution file (contribution_ID, ..., Worker_ID, set_ID, answers_for_set ) and an output file
# Writes into out_file the contribution in serial manner
def serialize_data(in_file, out_file):
    # Read the contributions
    task_data, headers = read_csv_file(in_file, ',', True)

    # Open out_file to write results
    f = open(out_file, 'w')
    f.write(','.join(['worker_ID', 'task_ID', 'contribution']) + '\n')

    # for each line i.e. set of contributions
    for line in task_data:
        # remove the unnecessary brackets and split the set of contributions
        data_task_line_content_entries = line[4].strip('{}').split('---')

        # For each task answer entry
        for data_task_line_content_entry in data_task_line_content_entries:
            # split the entry into question_ID and contribution
            cont_ = data_task_line_content_entry.split(':')

            # write line (worker_ID, task_ID, contribution)
            f.write(','.join([line[2], cont_[0], cont_[1]]) + '\n')

    return out_file


# Takes the raw feature file in_file and an output path out_file_index
# Split in_file features into 4 files: declarative profile, self evaluation, time to fill profile and campaign version
def slice_profile(in_file, out_file_index):
    obj_df = pd.read_csv(in_file, sep=",", quotechar='"', header=0).drop_duplicates('worker_ID', keep='first')

    # Profiles to be created and their features
    file_indices = {
        'decl': ['Age', 'Gender', 'Education_l', 'Education_d', 'Work_experience', 'Work_domain', 'Country',
                 'Language_n', 'Language_o', 'Interests_1', 'Interests_2', 'Full_time_worker'],
        'self': ['V_1', 'V_2', 'V_3', 'V_4', 'V_5', 'V_6', 'V_7'],
        'version': ['Version'],
        'time_p': ['Time_to_complete']}

    # Drop lines containing nan
    obj_df = obj_df.dropna()

    # Change index to worker ids
    obj_df = obj_df.set_index('worker_ID')

    # For each profile type
    for file_index in file_indices:
        # Create an output file and write header into it
        f = open(out_file_index + file_index + '.csv', 'w')
        f.write('worker_ID,' + ','.join(file_indices[file_index]) + '\n')

        # Extract needed features from the input file and write them to the output file
        for index, line in obj_df[file_indices[file_index]].iterrows():
            line = [str(i) for i in line]
            line_new = '"' + index + '","' + '","'.join(line) + '"\n'
            f.write(line_new)

        f.close()

    return obj_df


# Takes a feature in_file and an output file out_file
# Returns a dataframe with label encoded features and write data into out_file
def categorical_to_numeric_sk(in_file, out_file):
    # Read a worker feature file
    obj_df = pd.read_csv(in_file, sep=",", quotechar='"', header=0)

    # Drop lines containing nan
    obj_df = obj_df.dropna()

    # Change index to worker ids
    obj_df = obj_df.set_index('worker_ID')

    # Initialize the label encoder
    lb_make = LabelEncoder()

    # Fit the encoder for each feature and transform all values
    for feature in list(obj_df):
        obj_df[feature] = lb_make.fit_transform(obj_df[feature])

    # Open out_file to write results and write headers into it
    f = open(out_file, 'w')
    f.write('worker_ID,' + ','.join(list(obj_df)) + '\n')

    # Write the encoded profile into the output file
    for index, line in obj_df.iterrows():
        line = [str(i) for i in line]
        line_new = '' + index + ',' + ','.join(line) + '\n'
        f.write(line_new)

    return obj_df


# Takes an in_file of ratings (worker_ID, rating_) multiple rows i.e. rating for each worker and an output file out_file
# Writes into out_file parallel ratings i.e. (worker_ID, rating_1,... ,rating_7, average_rating, median_rating)
def parallelize_profile_ratings(in_file, out_file):
    # Read the serial rating file into a dataframe
    ratings_df = pd.read_csv(in_file, sep=",", quotechar='"', header=0, dtype={'rating_': object})

    # Index the dataframe by the worker_ID
    ratings_df = ratings_df.set_index('worker_ID')

    # Get the rating column (in case the raw rating file is used other column exist and must be ignored)
    ratings_df = ratings_df[['rating_']]

    # Get the list of unique workers
    indices = list(ratings_df.index.unique())

    # Open out_file to write results and write the headers into it
    f = open(out_file, 'w')
    f.write('worker_ID,r_1,r_2,r_3,r_4,r_5,r_6,r_7,average_rating,median\n')

    # For each worker
    for i in indices:
        # Get the first 7 ratings (the minimum number of rating for each profile)
        tmp_str = list((ratings_df['rating_'][i])[:7])
        tmp_ = [int(rating) for rating in tmp_str]

        # Write the ratings into one row of the output file with their average and median
        f.write(i + ',' + ','.join(tmp_str) + ',' + str(np.mean(tmp_)) + ',' + str(np.median(tmp_)) + '\n')

    return out_file


# Takes a contribution files (worker_ID, task_ID, contribution)
# returns a list of list [[task_ID, cont_worker_1, ..., cont_worker_n]] (n is variable for each task)
def parallelize_task_contributions(in_file):
    # Read the contribution into a dataframe
    contributions_ = pd.read_csv(in_file, sep=",", quotechar='"', header=0,
                                 dtype={'worker_ID': object, 'task_ID': object, 'contributions': object})

    # Drop duplicate lines (in case they existe for sme reason)
    contributions_.drop_duplicates(['worker_ID', 'task_ID'], keep='first')

    # Set task_ID as index to the dataframe
    contributions_ = contributions_.set_index('task_ID')

    # Get the unique task ID
    indices = list(contributions_.index.unique())

    # For each task
    contributions_parallel = list()
    for i in indices:
        # Append the task ID and all the answers for the surrent task into a list
        contributions_parallel_tmp = list()
        contributions_parallel_tmp.append(i)
        for j in list(contributions_['contribution'][i]):
            contributions_parallel_tmp.append(j)

        # Append the list to the output
        contributions_parallel.append(contributions_parallel_tmp)

    return contributions_parallel


# Takes a contribution files (worker_ID, task_ID, contribution) and an output file file out_file
# Computes majority voting for all tasks and writes data in an output file TODO: ADD TIE BREAKER
def majority_voting(in_file, out_file):
    conts = pd.DataFrame(parallelize_task_contributions(in_file))
    conts = conts.set_index(0)
    elected = {}

    for index, cont in conts.iterrows():
        count_answer_occ = cont.value_counts()
        elected_answer = count_answer_occ.idxmax()
        elected[index] = int(elected_answer)

    # Open out_file to write results
    f = open(out_file, 'w')
    data, header = read_csv_file(in_file, ',', True)
    f.write(','.join(header) + ',\n')

    for line in data:
        try:
            f.write(','.join([str(i) for i in line]) + ',' + str(elected[line[1]]) + '\n')
        except KeyError:
            print(line[1])

    return elected


# Takes an in_file indexed by worker_ID and a list of workers to filter from the file
# Write the filtered rows of in_file into out_file
def wirte_worker_filtered(in_workers, in_file, out_file):
    # Read the worker profile into a data frame
    workers = pd.read_csv(in_file, sep=',', header=0)

    # Index the dataframe by worker_ID
    workers = workers.set_index('worker_ID')

    # Get the needed sub dataframe i.e. the profile of worker in the in_workers list
    workers_filtered = workers.loc[in_workers]

    # Open out_file to write results and write headers into it
    f = open(out_file, 'w')
    f.write('worker_ID,' + ','.join(list(workers)) + '\n')

    # For each worker in the given list
    for index, line in workers_filtered.iterrows():
        # get and rewrite the data row
        f.write(str(index) + ',' + ','.join([str(i) for i in line]) + '\n')

    f.close()


# Takes a list of workers to filter, a feature in_file index by worker_ID and a criteria config_dict.
# Returns the list of workers with features respecting the criteria
def select_workers_by_criterium(in_worker_list, in_file, config_dict):
    # Build the operator dictionary
    operators = {'>': operator.gt, '>=': operator.ge, '<': operator.lt, '<=': operator.le}

    # Read the worker profiles from file
    workers = pd.read_csv(in_file, sep=',', header=0)

    # Index the data frame by worker_ID
    workers = workers.set_index('worker_ID')
    workers_filtered = workers

    # For each criterium
    for config_ in config_dict:
        # Select workers whose profile features respect the criterium
        op = config_dict[config_][0]
        workers_filtered = workers_filtered.loc[workers_filtered.index[operators[op](workers_filtered[config_],
                                                                                     config_dict[config_][1])]]

    # build the ID list of the filtered workers
    fitered_ = set(list(workers_filtered.index)).intersection(set(in_worker_list))

    return fitered_


# Takes a feature in_file index by worker_ID, a criteria config_dict and path configuration for read write.
# Returns the list of workers with features respecting the criteria and write data in output files (per feature type)
def select_workers_by_criteria(in_worker_file, criteria, prefix_pro_workers, prefix_pro_workers_filtered):
    # Read the worker file into worker_ID indexed dataframe and get the index list
    workers = list(pd.read_csv(in_worker_file, sep=',', header=0).set_index('worker_ID').index)

    # For each profile type run the filtering on the worker list filtered in a previous iteration
    for criterium_key, criterium in criteria.items():
        workers = select_workers_by_criterium(workers, prefix_pro_workers + criterium_key, criterium)

    print(len(workers))

    # Write the filtered worker profiles into appropriate files
    criteria_list = list(criteria.keys())
    criteria_list.append('Workers_decl_e.csv')
    criteria_list.append('Workers_self.csv')

    for criterium_key in criteria_list:
        wirte_worker_filtered(workers, prefix_pro_workers + criterium_key, prefix_pro_workers_filtered + criterium_key)

    return workers


# Takes a contribution_file, a worker list and an output out_file path
# Returns a dataframe containing the contributions of the worker list.  Data are writen in an out_file
def select_contributions_by_worker_list(contribution_file, in_workers_list, out_file):
    # Read the contribution file data as str
    contributions = pd.read_csv(contribution_file, sep=',', header=0,
                                dtype={'worker_ID': object, 'task_ID': object, 'contributions': object}) \
        .set_index('worker_ID')

    # Get the sub dataframe of filtered workers
    contributions_filtered = contributions.loc[in_workers_list]

    # Open out_file to write results and write headers into it
    f = open(out_file, 'w')
    f.write('worker_ID,' + ','.join(list(contributions)) + '\n')

    # Wirte the contributions into the output file
    for index, line in contributions_filtered.iterrows():
        f.write(str(index) + ',' + ','.join([str(i) for i in line]) + '\n')

    f.close()

    return contributions_filtered


# Parses the raw data and produces:
# Workers_self.csv : the self evaluation profile of the workers
# Workers_decl_e.csv : the declarative profile of the workers
# Workers_decl_e.csv : the declarative profile of the workers - label encoded
# Workers_time_p.csv : the time to fill the profile per worekr (used for filtering)
# Workers_decl_r_p.csv : the rating for each worker profile; declarative + self (used for filtering)
# worker_time_cont.csv : The times of completing each task set for each worker
# Contributions_serialized.csv : Contribution per worker per task question (structured str IDs)
# Contributions_serialized_translated.csv : Contribution per worker per task question (Numerical IDs)
# Contributions_serialized_translated_mv.csv : Contribution per worker per task question with computed majority voting
def prepare_all_data():
    # --- Where are the raw data files (CrowdED)
    prefix_raw = '/CrowdED/Core'  # Path to CrowdED core

    # --- Where to read/write parsed (unfiltered) data
    prefix_pro_cont = '/All/Contributions/'
    prefix_pro_workers = '/All/Workers/'

    # --- Where to read/write the filtered data
    prefix_pro_cont_filtered = '/Filtered_timeP_timeC_Rating/Contributions/'
    prefix_pro_workers_filtered = '/Filtered_timeP_timeC_Rating/Workers/'

    # --- prepare contributions : serialize, translate to numerical IDs, compute labels using MV
    serialize_data(prefix_raw + 'Contributions.csv', prefix_pro_cont + 'Contributions_serialized.csv')
    translate_task_ids(prefix_pro_cont + 'Contributions_serialized.csv',
                       prefix_pro_cont + 'Contributions_serialized_translated.csv', 'new/taskIds', True)
    majority_voting(prefix_pro_cont + 'Contributions_serialized_translated.csv',
                    prefix_pro_cont + 'Contributions_serialized_translated_mv.csv')

    # --- prepare worker profiles: split into declarative, self eval, time, and version and encode decl profile
    slice_profile(prefix_raw + 'workers.csv', prefix_pro_workers + 'Workers_')
    categorical_to_numeric_sk(prefix_pro_workers + 'Workers_decl.csv', prefix_pro_workers + 'Workers_decl_e.csv')
    parallelize_time_per_set(prefix_raw + 'Contributions.csv', prefix_pro_workers + 'worker_time_cont.csv')

    # --- prepare ratings
    parallelize_profile_ratings(prefix_raw + 'Ratings.csv', prefix_pro_workers + 'Workers_decl_r_p.csv')

    # --- filter workers by criteria:
    criteria = {
        'worker_time_cont.csv': {'median': ['>=', 300], 'min': ['>=', 60], 'count': ['>=', 4]},
        'Workers_decl_r_p.csv': {'average_rating': ['>=', 0]},
        'Workers_time_p.csv': {'Time_to_complete': ['>=', 0]}
    }

    filtered = select_workers_by_criteria(prefix_raw + 'Ratings.csv', criteria, prefix_pro_workers,
                                          prefix_pro_workers_filtered)

    # --- filter contributions by workers:
    select_contributions_by_worker_list(prefix_pro_cont + 'Contributions_serialized_translated.csv', filtered,
                                        prefix_pro_cont_filtered + 'Contributions_serialized_translated_filtered.csv')

    # --- Recompute majority voting for the filtered contributions
    majority_voting(prefix_pro_cont_filtered + 'Contributions_serialized_translated_filtered.csv',
                    prefix_pro_cont_filtered + 'Contributions_serialized_translated_filtered_mv.csv')

    file_per_task_set(prefix_pro_cont + 'Contributions_serialized_translated_mv.csv',
                      prefix_pro_cont + 'ByTaskSet/Contributions_serialized_translated_filtered', 'new/taskIds')


if __name__ == '__main__':
    prepare_all_data()
