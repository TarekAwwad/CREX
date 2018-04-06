 function create_header(element, page_title) {
     var element = document.getElementById(element);
     
     //     Logo and title 
     var header_logo_title_div = document.createElement("div");
     header_logo_title_div.setAttribute('id', 'header-logo-title');
     header_logo_title_div.setAttribute('class', 'col-sm-4');
     
     var header_logo_div = document.createElement("div");
     header_logo_div.setAttribute('class', 'col-sm-6');
     
     var header_logo_img = document.createElement("img");
     header_logo_img.setAttribute('class', 'propic');
     header_logo_img.setAttribute('src', 'img/logo.png');
     
     var header_title_div = document.createElement("div");
     header_title_div.setAttribute('class', 'col-sm-6');
     
     var header_logo_text_1 = document.createElement("h1");
     header_logo_text_1.innerHTML = "Project";
     
     var header_logo_text_2 = document.createElement("h1");
     header_logo_text_2.innerHTML = "Crowd";

     var header_logo_text_3 = document.createTextNode("An Extended Crowdsourcing Campaign");
    
     var header_contact_div = document.createElement("div");
     header_contact_div.setAttribute('class', 'col-sm-6');
     header_contact_div.innerHTML = '<header><a href="mailto:email@company.com">contact us</a></header>';

     header_logo_div.appendChild(header_logo_img);
     header_title_div.appendChild(header_logo_text_1);
     header_title_div.appendChild(header_logo_text_2);   
     header_title_div.appendChild(header_logo_text_3);
     header_logo_title_div.appendChild(header_logo_div);
     header_logo_title_div.appendChild(header_title_div);
     header_logo_title_div.appendChild(header_contact_div);

     element.appendChild(header_logo_title_div);
     
     //     Spacer
     var header_spacer_div = document.createElement("div");
     header_spacer_div.setAttribute('id', 'header-contact');
     header_spacer_div.setAttribute('class', 'col-sm-4');
     
     element.appendChild(header_spacer_div);
     
     //    Acknowledgement and Contact
     var header_contact_ack_div = document.createElement("div");
     header_contact_ack_div.setAttribute('id', 'header-contact');
     header_contact_ack_div.setAttribute('class', 'col-sm-4');
     
     // var header_ack_div = document.createElement("div");
     // header_ack_div.setAttribute('class', 'row');
     // header_ack_div.innerHTML = '<header><p> This work is part of a research project taking place in the <a href="https://liris.cnrs.fr/">LIRIS</a> laboratory of <a href="https://insa-lyon.fr">INSA Lyon</a> and the <a href="http://www.fim.uni-passau.de/en/distributed-information-systems/">DIMIS</a> chair at <a href="https://www.uni-passau.de/en/">Universität Passau</a> within the <a href="http://irixys.org/">IRIXYS</a> research and innovation center.<br> </p></header>';

     var header_page_title_div = document.createElement("div");
     header_page_title_div.setAttribute('class', 'row');
     header_page_title_div.innerHTML = '<header><h3>' + page_title +  '</h3></header>';

     header_contact_ack_div.appendChild(header_page_title_div);
//     header_contact_ack_div.appendChild(header_contact_div);
    element.appendChild(header_contact_ack_div);
 }
