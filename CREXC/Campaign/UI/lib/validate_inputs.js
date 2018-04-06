//Check if all fields aer filled and return a warning message for empty fields
function validateForm() {
    //    Fetch all inputs fiuelds
    var inputs = document.getElementsByTagName('input');
    var selects = document.getElementsByTagName('select');
    var fields = []


    //    Store all fields - except the form submit input - in an array
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].getAttribute('name') !== 'submit') {
            fields.push(inputs[i].getAttribute('name'));
        }
    }

    for (var j = 0; j < selects.length; j++) {
        fields.push(selects[j].getAttribute('name'));
    }

    var proceed = true;

    //    Check the if the fields are empty (or contain default values)
    var missing = 0;
    for (var i = 0; i < fields.length; i++) {


        var x = document.forms[0][fields[i]].value;
        var element = document.getElementById("error_" + fields[i]);

        if (x === "choose one" || x === "") {
            element.innerHTML = " This must be filled out";
            missing = missing + 1;
            proceed = false;
        }
        else {
            element.innerHTML = "";
        }

    }

    if (missing > 0) {
        alert("Please fill in all task, many answers are missing");
    }

    var element_cod = document.getElementById("codec");

    if (element_cod) {
        if (!element_cod.checked) {
            var element_cod_err = document.getElementById("error_codec");

            console.log(element_cod);
            element_cod_err.innerHTML = " This must be filled out";
            proceed = false;
        }
    }
    return proceed;
}

//Check if the contributor ID and its confirmation are identical
function validateID() {
    var cid = document.forms[0]['cid'].value;
    var ccid = document.forms[0]['ccid'].value;
    var ccid_err = document.getElementById("error_ccid");
    var proceed = true;
    if (cid != ccid) {
        ccid_err.innerHTML = "ID does not match";
        proceed = false;
    }
    return proceed;
}
