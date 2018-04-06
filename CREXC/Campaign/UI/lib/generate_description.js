 function create_desc(element, descritpion_data) {
     //     Data
     var data_array = Object.keys(descritpion_data).map(function (k) {
         return descritpion_data[k]
     });
     
     //      Logo and Title
     var element = document.getElementById(element);
     var intro_sec_logo = document.createElement("div");
     var intro_sec_logo_span = document.createElement("span");
     intro_sec_logo.setAttribute('class', 'col-sm-1')
     intro_sec_logo_span.setAttribute('class', 'secicon fa fa-handshake-o');
     intro_sec_logo.appendChild(intro_sec_logo_span);
     element.appendChild(intro_sec_logo);
     var intro_sec_content = document.createElement("div");
     intro_sec_content.setAttribute('class', 'col-sm-11');
     intro_sec_content.setAttribute('id', 'introduction_content');
     var intro_sec_content_title = document.createElement("h3");
     intro_sec_content_title.innerHTML = 'Introduction';
     intro_sec_content.appendChild(intro_sec_content_title);

     //     Sections and content
     for (count1 = 0; count1 < data_array.length; count1++) {
         if (data_array[count1] != "") {
             var desc_sec_title = document.createElement("h4");
             var desc_sec_title_son = document.createTextNode(Object.keys(descritpion_data)[count1]);
             var desc_sec_div = document.createElement("div");
             var desc_sec_p = document.createElement("p");
             var desc_sec_content = data_array[count1];
             desc_sec_div.setAttribute('class', 'abstract');
             desc_sec_title.appendChild(desc_sec_title_son);
             desc_sec_p.innerHTML = desc_sec_content;
             desc_sec_div.appendChild(desc_sec_p);
             intro_sec_content.appendChild(desc_sec_title);
             intro_sec_content.appendChild(desc_sec_div);
         }
     }
     element.appendChild(intro_sec_content);
 }