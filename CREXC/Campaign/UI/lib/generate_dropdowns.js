function create_ddl(el, data){

    var data_array = Object.keys(data).map(function(k) { return data[k] });
    var element = document.getElementById(el);

    for(count1 = 0; count1 < data_array.length; count1++){

//      structure
        var div_sec = document.createElement("div");
        var div_sec_1 = document.createElement("div");
        var div_sec_2 = document.createElement("div");
        var span_sec = document.createElement("span");
        var span_err_sec = document.createElement("span");
        var label_sec = document.createTextNode(data_array[count1].text);
        var select_sec = document.createElement("select");
        var options = data_array[count1].content;

//      create default option - disabled
        var option_sec = document.createElement("option");
        var son = document.createTextNode("choose one");
        option_sec.setAttribute('disabled', 'disabled');
        option_sec.setAttribute('selected', 'true');

        option_sec.appendChild(son);
        select_sec.appendChild(option_sec);

        var data_array_sub = Object.keys(options).map(function(k) { return options[k] });
        for(count = 0; count < data_array_sub.length; count++){
            var option_sec = document.createElement("option");
            var son = document.createTextNode(data_array_sub[count]);
            option_sec.setAttribute('value', data_array_sub[count]);
            option_sec.appendChild(son);
            select_sec.appendChild(option_sec);
        }

//      attributes and styling
        div_sec.setAttribute('class', 'row');
        div_sec_1.setAttribute('class', 'col-md-8');
        div_sec_2.setAttribute('class', 'col-md-4');
        span_err_sec.setAttribute('id', 'error_' + data_array[count1].name);
        span_err_sec.setAttribute('class', 'nb');
        span_sec.setAttribute('class', 'fa fa-angle-right');
        select_sec.setAttribute('class', 'pull-right input-medium');
        select_sec.setAttribute('name', data_array[count1].name);

//      building
        div_sec_1.appendChild(span_sec);
        div_sec_1.appendChild(label_sec);
        div_sec_1.appendChild(span_err_sec);
        div_sec_2.appendChild(select_sec);
        div_sec.appendChild(div_sec_1);
        div_sec.appendChild(div_sec_2);
        element.appendChild(div_sec);
        element.appendChild(document.createElement("br"));
    }
}