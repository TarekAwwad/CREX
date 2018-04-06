function create_task(el, data) {
    var data_array = Object.keys(data).map(function (k) {
        return data[k]
    });
    var element = document.getElementById(el);
    var task_type = data_array[0].type
    for (count1 = 2; count1 < data_array.length; count1++) {
        var row_div = document.createElement("div");
        row_div.setAttribute('class', 'row');

        //      HIT title
        var hit_title = document.createElement("div");
        hit_title.setAttribute('class', 'col-md-2 list-group-item list-group-item-custom');
        hit_title.innerHTML = '<div class="col-md-3"><span class="subsecicon fa fa-puzzle-piece"></span> </div><div class="col-md-9">' + data_array[count1].name + '</div>';
        row_div.appendChild(hit_title);

        var hit_content = document.createElement("div");

        //      HIT content - generic order
        if (data_array[count1].order !== "") {
            hit_content.setAttribute('class', 'col-md-12 list-group-item');
            hit_content.innerHTML = '<div class="row"><div class="col-md-1"></div>' + '<div class="col-md-10"> <h4>' + data_array[count1].order + '</h4></div></div><div class="col-md-1"></div>';
            hit_content.appendChild(document.createElement("br"));
        }

        //      HIT content - tweet
        if (data_array[count1].tt !== "") {
            var hit_content_tweets = document.createElement("div");
            hit_content_tweets.setAttribute('class', 'row');
            var tweets = data_array[count1].tt;
            var data_array_tt = Object.keys(tweets).map(function (k) {
                return tweets[k]
            });
            var temp_ = '';
            for (count_i = 0; count_i < data_array_tt.length; count_i++) {
                temp_ = temp_ + '<div class="row"><div class="col-md-2"></div><div class="col-md-8 list-group-item list-group-item-info hit-content-text"> ' + data_array_tt[count_i] + '</div></div></br>';
            }
            temp_ = temp_ + '</div>';
            hit_content_tweets.innerHTML = temp_;
            hit_content.appendChild(hit_content_tweets);
            hit_content.appendChild(document.createElement("br"));
        }

        //      HIT content - images
        if (data_array[count1].mm !== "") {
            var hit_content_images = document.createElement("div");
            hit_content_images.setAttribute('class', 'row');
            var images = data_array[count1].mm;
            var data_array_img = Object.keys(images).map(function (k) {
                return images[k]
            });

            var img_col_width = Math.ceil(8 / data_array_img.length);
            var img_col_offset = Math.floor((12 - img_col_width) / data_array_img.length);

            temp_ = '<div class="row"><div class="col-md-' + img_col_offset + '"></div>';
            for (count_i = 0; count_i < data_array_img.length; count_i++) {
                temp_ = temp_ + '<div class="col-md-' + img_col_width + '"><div class="style_prevu_kit"><img src="' + data_array_img[count_i] + ' "></div></div>';
            }
            temp_ = temp_ + '<div class="col-md-2"></div></div>';
            hit_content_images.innerHTML = temp_;
            hit_content.appendChild(hit_content_images);
            hit_content.appendChild(document.createElement("br"));
        }

        //      HIT content - question
        if (data_array[count1].text !== "") {
            var hit_content_question = document.createElement("div");
            hit_content_question.setAttribute('class', 'row');
            hit_content_question.innerHTML = '<div class="col-md-1"></div><div class="col-md-10"><h4>' + data_array[count1].text + '</h4><hr></div><div class="col-md-1"></div>';
            hit_content.appendChild(hit_content_question);
        }

        //      HIT content - options
        if (data_array[count1].op !== "") {
            options_quest = data_array[count1].op;
            var data_array_ops = Object.keys(options_quest).map(function (k) {
                return options_quest[k]
            });

            for (var count_i = 0; count_i < data_array_ops.length; count_i++) {

                if (data_array_ops[count_i] !== "") {
                    var hit_content_op = document.createElement("div");
                    //            hit_content_op.setAttribute('class', 'row');
                    var options = data_array_ops[count_i];

                    var data_array_op = Object.keys(options).map(function (k) {
                        return options[k]
                    });

                    var hit_content_op_text = document.createElement("div");
                    hit_content_op_text.setAttribute('class', 'row');
                    hit_content_op_text.innerHTML = '<div class="col-md-1"></div><div class="col-md-10"><h4>' + options["op-text"] + '</h4></div><div class="col-md-1"></div>'
                    hit_content_op.appendChild(hit_content_op_text);
                    hit_content_op.appendChild(document.createElement("br"));

                    var col_number = Math.ceil(data_array_op.length / 6);
                    var col_width = Math.ceil(12 / col_number);

                    temp_ = '<div class="row"><div class="col-md-1"></div><div class="col-md-10">'
                        + '<span class="nb" id="error_'
                        + data.id + '_' + data_array[count1].id + '_op' + count_i
                        + '"></span>';

                    for (var i = 0; i < col_number; i++) {
                        temp_ = temp_ + '<div class="col-md-' + col_width + '">';

                        for (var count_o = i * 6; count_o < i * 6 + 6 && count_o < data_array_op.length - 1; count_o++) {
                            temp_ = temp_ + '<div class="hit-content-text-op"><input type="radio" name="'
                                + data.id + '_' + data_array[count1].id + '_op' + count_i
                                + '" value="' + count_o + '"> &nbsp;' + options[count_o]
                                + '</div>';
                        }
                        temp_ = temp_ + '</div>';
                    }
                    temp_ = temp_ + '</div><div class="col-md-1"></div></div>';

                    hit_content_op.innerHTML = hit_content_op.innerHTML + temp_;
                    hit_content.appendChild(hit_content_op);
                    hit_content.appendChild(document.createElement("br"));
                }

            }
        }

        //      HIT content - text
        if (data_array[count1].ft !== "") {
            var hit_content_ft = document.createElement("div");
            hit_content_ft.setAttribute('class', 'row');
            var ft = data_array[count1].ft;
            var data_array_ft = Object.keys(ft).map(function (k) {
                return ft[k]
            });
            temp_ = '<div class="col-md-1"></div><div class="col-md-10">';
            for (count_t = 0; count_t < data_array_ft.length; count_t++) {
                temp_ = temp_ + '<div class="row"><div class="col-md-12"><h4>'
                    + ft.ft0 + '</h4></div><div class="col-md-12"><input class="input-large" type="text" placeholder="answer here" name="'
                    + data.id + '_' + data_array[count1].id + '_ft_' + count_t + '">'
                    + '<span class="nb" id="error_'
                    + data.id + '_' + data_array[count1].id + '_ft_' + count_t
                    + '"></span></div></div><br>';
            }
            temp_ = temp_ + '</div><div class="col-md-1"></div>';

            hit_content_ft.innerHTML = temp_;
            hit_content.appendChild(hit_content_ft);
            hit_content.appendChild(document.createElement("br"));
        }

        //      Append contents to the task container
        row_div.appendChild(hit_content);
        element.appendChild(row_div);
        element.appendChild(document.createElement("br"));
    }
}