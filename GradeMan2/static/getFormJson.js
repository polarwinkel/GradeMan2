function getFormJson() {
    var out = {};
    var form = document.getElementsByClassName('formdata');
    for (var i=0, item; item = form[i]; i++) {
        if (out.hasOwnProperty(item.name)) { // key exists
            if (!Array.isArray(out[item.name])) { // convert to array
                out[item.name] = [out[item.name]]
            }
            if (item.type != 'checkbox'){
                out[item.name].push(item.value);
            } else {
                if (item.checked) {
                    out[item.name].push(item.value)
                } else {
                    out[item.name].push('False')
                }
            }
        } else {
            if (item.type != 'checkbox'){
                out[item.name] = item.value;
            } else {
                if (item.checked) {
                    out[item.name] = item.value;
                } else {
                    out[item.name] = 'False';
                }
            }
        }
    }
    return out;
}
