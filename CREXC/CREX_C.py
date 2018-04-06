import sys
import csv
import operator


# Function to prepend/change the header line in the task file
def line_prepender(filename, linea, change_header):
    with open(filename, 'r+') as f:
        content = f.readlines()
        contenta = ''
        for line in content[change_header:]:
            contenta = contenta + line

    with open(filename, 'w') as f:
        f.write(linea.rstrip('\r\n') + '\n' + contenta)


# Prepare the header of the task scv file
def prepare_task_files(in_file, configuration, change_header):
    # Create structures to store the header tags
    multi_level_tags_val_tt = list()
    multi_level_tags_val_mm = list()
    multi_level_tags_val_ft = list()
    multi_level_tags_val_ = dict()

    # Create the dictionary to store the configurations
    config = dict()

    # Parse the configuration file
    with open(configuration, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            temp = line.split(sep='|')
            config[temp[0]] = temp[1]
    f.close()

    attribute_list = list()

    # Get positions for :
    #  HIT name
    attribute_list.append(['name', int(config['ques-name-col'])])
    #  HIT id
    attribute_list.append(['id', int(config['ques-id-col'])])
    #  HIT text
    attribute_list.append(['text', int(config['ques-text-col'])])
    #  HIT order
    attribute_list.append(['order', int(config['ques-text-col'])])

    # HIT images
    for i in range(int(config['image'])):
        multi_level_tags_val_mm.append('mm' + str(i))
        attribute_list.append(['mm' + str(i), int(config['image-' + str(i)])])

    # HIT textual entries
    for i in range(int(config['text'])):
        multi_level_tags_val_tt.append('tt' + str(i))
        attribute_list.append(['tt' + str(i), int(config['text-' + str(i)])])

    # HIT open answer questions
    for i in range(int(config['oaq'])):
        multi_level_tags_val_ft.append('ft' + str(i))
        attribute_list.append(['ft' + str(i), int(config['oaq-' + str(i)])])

    # HIT MCQs
    for i in range(int(config['mcq'])):
        attribute_list.append(['op' + str(i) + 't', int(config['mcq-' + str(i)])])
        op_temp = ['op' + str(i) + 't']
        for k in range(int(config['mcq-' + str(i) + '-o'])):
            op_temp.append('op' + str(i) + str(k))
            attribute_list.append(['op' + str(i) + str(k), int(config['mcq-' + str(i)]) + k + 1])
        multi_level_tags_val_['op' + str(i)] = op_temp

    sorted_attribute_list = sorted(attribute_list, key=operator.itemgetter(1))
    line_prepender(in_file, '|'.join([s[0] for s in sorted_attribute_list]), change_header)

    # Get task name
    tid_ = config['task-id']

    # Get task label : A general purpose field
    type_ = config['task-label']

    return tid_, type_, multi_level_tags_val_tt, multi_level_tags_val_mm, multi_level_tags_val_ft, multi_level_tags_val_, sorted_attribute_list


def generate_task_desc_file(configuration, res):
    gtd_tid_ = res[0]
    out_file = "./Campaign/UI/res/task_" + gtd_tid_ + "_desc.js"

    # Create the dictionary to store the configurations
    config = dict()

    # Parse the configuration file
    with open(configuration, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            temp = line.split(sep='|')
            config[temp[0]] = temp[1]
    f.close()

    config = {"Description": config['desc-main-content'], "Instructions": config['inst-main-content'],
              "Examples": config['exam-main-content'], "Notes": config['note-main-content']}

    a = []

    for key in config.keys():
        a.append('"' + key + '":"' + config[key] + '"')

    a_ = 'var task_description_data = {' + ','.join(a) + '}'

    out_file_ = open(out_file, "w")
    out_file_.write(a_)


def generate_task_hits_file(in_file, res):
    gtf_tid_ = res[0]
    gtf_type_ = res[1]
    multi_level_tags_val_tt = res[2]
    multi_level_tags_val_mm = res[3]
    multi_level_tags_val_ft = res[4]
    multi_level_tags_val_ = res[5]
    tags = ['name', 'id', 'order', 'text']

    a = []
    with open(in_file) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|', quoting=csv.QUOTE_NONE)
        for row in reader:
            main_ = '"' + row['name'] + '" :{' + ','.join(
                ['"' + tag + '":"' + row[tag] + '"' for tag in tags]) + ","
            tt = '"tt" : {' + ','.join(['"' + tag + '":"' + row[tag] + '"' for tag in multi_level_tags_val_tt]) + '},'
            mm = '"mm" : {' + ','.join(['"' + tag + '":"' + row[tag] + '"' for tag in multi_level_tags_val_mm]) + '},'
            ft = '"ft" : {' + ','.join(['"' + tag + '":"' + row[tag] + '"' for tag in multi_level_tags_val_ft]) + '},'
            op = []
            for key in multi_level_tags_val_.keys():
                op.append('"' + key + '"' + ':{' + ','.join(
                    ['"' + tag + '":"' + row[tag] + '"' for tag in multi_level_tags_val_[key]]) + '}')
            opf = '"op" : {' + ','.join(op) + '}'

            a.append(main_ + mm + tt + ft + opf + '}')

    a = 'var task_data = { "id" : "' + gtf_tid_ + '", "type" : "' + gtf_type_ + '",' + ','.join(a) + '}'

    out_file = "./Campaign/UI/res/task_" + gtf_tid_ + "_auto.js"

    out_file_ = open(out_file, "w")
    out_file_.write(a)


def main(args):
    res = prepare_task_files(args[0], args[1], 1)
    generate_task_hits_file(args[0], res)
    generate_task_desc_file(args[1], res)


if __name__ == "__main__":
    main(sys.argv)
