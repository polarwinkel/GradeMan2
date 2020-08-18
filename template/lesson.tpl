<h1 id="title"></h1>
<nav id="pagenav">
</nav>
<div id="content">
</div>
<script src="../static/getFormJson.js"></script>
<script src="{{ relroot }}static/polalert.js"></script>
<script>
var l = {{ ljson }};
var c = {{ cjson }};

title = document.getElementById('title');
pagenav = document.getElementById('pagenav');
content = document.getElementById('content');

function mdtex2html(mdtex) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "{{ relroot }}mdtex2html", false);
    xhr.setRequestHeader("Content-Type", "application/mdtex");
    xhr.send(mdtex);
    return xhr.responseText;
}

function show() {
    var out = '<h2>'+l.topic+'</h2>';
    out += '<p class="date">'+l.date+'</p>\n';
    out += '<p>Notizen:</p>\n<div class="border">'+mdtex2html(l.memo)+'</div>\n';
    out += '<p>Details:</p>\n<div class="border">'+mdtex2html(l.details)+'</div>\n';
    content.innerHTML = out;
}
function edit() {
    content.innerHTML = '\
        <input type="hidden" id="what" name="what" class="formdata" value="lesson" />\
        <input type="hidden" id="lid" name="lid" class="formdata" />\
        <div style="clear:both;"><label for="date">Datum: </label><input type="date" name="date" id="date" class="formdata" required /></div>\
        <div style="clear:both;"><label for="cid">Klasse: </label><select name="cid" id="cid" class="formdata smallSelect" required></select></div>\
        <div style="clear:both;"><label for="topic">Thema: </label><input type="text" name="topic" id="topic" class="formdata" /></div>\
        <div style="clear:both;"><label for="count">Faktor: </label><select name="count" id="count" class="formdata smallSelect"></select></div>\
        <div style="clear:both;"><label for="memo">Notizen: </label><textarea name="memo" id="memo" class="formdata"></textarea></div>\
        <div style="clear:both;"><label for="details">Details: </label><textarea name="details" id="details" class="formdata"></textarea></div>\
        <div style="clear:both;"><input type="submit" value="Speichern" onclick="send()"></div>\
    '
    document.getElementById('lid').value = l.lid;
    document.getElementById('date').value = l.date;
    var cid = document.getElementById('cid');
    for (var i=0; i < c.length; i++) {
        if (c[i].cid == l.cid) {
            cid[c[i].cid] = new Option(c[i].name+' '+c[i].subject, c[i].cid, true, true);
        } else {
            cid[c[i].cid] = new Option(c[i].name+' '+c[i].subject, c[i].cid, );
        }
        console.log(i);
    }
    document.getElementById('topic').value = l.topic;
    var count = document.getElementById('count')
    var options = ['1', '2', '3', '4', '5', '25%', '33%', '50%'];
    options.forEach(function(element,key) {
        if (element == l.count) {
            count[key] = new Option(element, element, true, true);
        } else {
            count[key] = new Option(element, element);
        }
    });
    document.getElementById('memo').value = l.memo;
    document.getElementById('details').value = l.details;
}
function send() {
    var xhr = new XMLHttpRequest();
    var formJson = getFormJson();
    if (formJson.lid=='') {
        xhr.open('POST', '../newDbEntry', false);
    } else {
        xhr.open('PUT', '../updateDbEntry', false);
    }
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(formJson));
    if (formJson.lid=='') { // new
        if (isNaN(xhr.responseText)) {
            document.getElementById('content').innerHTML = xhr.responseText;
        } else {
            window.location = xhr.responseText;
        }
    } else if (xhr.responseText = 'ok') {
        location.reload();
    } else {
        document.getElementById('content').innerHTML = xhr.responseText;
    }
}
// attendances:
function showAttendances() {
    var url = '../json/lessonAttendances/'+l.lid;
    fetch(url).then(function(response) {
        if (response.ok) {
            return response.json();
        }
        else 
            throw new Error('ERROR: Attendances could not be fetched from server!');
    })
    .then(function(aa) {
        renderAttendances(aa);
    })
    .catch(function(err) {
        console.log(err);
    });
}
function renderAttendances(aa) {
    out = '<h2>Teilnahmen</h2>\n';
    out = '<p id="showImages"><a onclick="showImages()">Bilder einblenden</a></p>\n';
    out += '<input type="hidden" id="what" name="what" class="formdata" value="attendances" />';
    out += '<div class="student"><div style="float:left; width:12rem; max-width:100%; font-weight:bold;">Vorname Nachname</div>\n';
    out += '<div style="float:left; width:1.5rem; font-weight:bold;">A</div>\n';
    out += '<div style="float:left; width:1.5rem; font-weight:bold;">E</div>\n';
    out += '<div style="float:left; width:1.5rem; font-weight:bold;">H</div>\n';
    out += '<div style="float:left; width:2rem; font-weight:bold;">F</div>\n';
    out += '<div style="float:left; width:2rem; font-weight:bold;">M</div>\n';
    out += '<div style="float:left; font-weight:bold;">Bemerkung</div><br /></div><hr style="clear:both;"/>\n';
    for (var i=0; i<aa.length; i++) {
        console.log(aa[i]);
        out += '<div class="img" id="'+aa[i].sid+'" style="float:left;"></div>\n<div class="student">\n';
        out += '<input type="hidden" id="lid" name="lid" class="formdata" value="'+aa[i].lid+'" />';
        out += '<input type="hidden" id="sid" name="sid" class="formdata" value="'+aa[i].sid+'" />';
        out += '<div style="float:left; width:12rem; max-width:100%%;">'+'<a href="../student/'+aa[i].sid+'">\
                '+aa[i].givenname+' '+aa[i].familyname+'</a></div>\n';
        if (aa[i].attendant == 'False') 
            out += '<div style="float:left; width:1.5rem;"><input type="checkbox" name="attendant" id="attendant" class="formdata" value="True" /></div>\n';
        else
            out += '<div style="float:left; width:1.5rem;"><input type="checkbox" name="attendant" id="attendant" class="formdata" value="True" checked /></div>\n';
        if (aa[i].excused == 'True')
            out += '<div style="float:left; width:1.5rem;"><input type="checkbox" name="excused" id="excused" class="formdata" value="True" checked /></div>\n';
        else
            out += '<div style="float:left; width:1.5rem;"><input type="checkbox" name="excused" id="excused" class="formdata" value="True" /></div>\n';
        if (aa[i].homework == 'False')
            out += '<div style="float:left; width:1.5rem;"><input type="checkbox" name="homework" id="homework" class="formdata" value="True" /></div>\n';
        else
            out += '<div style="float:left; width:1.5rem;"><input type="checkbox" name="homework" id="homework" class="formdata" value="True" checked /></div>\n';
        // performance:
        out += '<select style="width:2rem;" name="performance" id="performance" class="formdata">\n';
        out += '<option value="-">-</option>';
        for (var j=1; j<=6; j++) {
            if (aa[i].performance == j)
                out += '<option value="'+j+'" selected>'+j+'</option>';
            else
                out += '<option value="'+j+'">'+j+'</option>';
        }
        out += '</select>\n'
        // participation:
        out += '<select style="width:2rem;" name="participation" id="participation" class="formdata">\n';
        out += '<option value="-">-</option>';
        for (var j=1; j<=6; j++) {
            if (aa[i].participation == j)
                out += '<option value="'+j+'" selected>'+j+'</option>';
            else
                out += '<option value="'+j+'">'+j+'</option>';
        }
        out += '</select>\n'
        out += '<input type="text" name="memo" id="memo" class="formdata" value="'+aa[i].memo+'" style="width:30rem; max-width:100%%;"/><br />\n';
        out += '</div>\n<hr style="clear:both;" />\n';
    }
    out += '<div>TODO: Notenrange entsprechend Kursoption (Oberstufe!)</div>\n';
    out += '<button onclick="saveAttendances()" style="clear:both;">Speichern</button><br />\n';
    out += '<p>Legende: A=Anwesend, E=Entschuldigt, H=Hausaufgabe, F=Fachliche Leistung, M=Mitarbeit</p>\n';
    content.innerHTML = out;
}
function saveAttendances() {
    var xhr = new XMLHttpRequest();
    var formJson = getFormJson();
    xhr.open('PUT', '../updateDbEntry', false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(formJson));
    if (xhr.responseText = 'ok') {
        pa.message('Erfolgreich gespeichert!');
        showAttendances();
    } else {
        document.getElementById('content').innerHTML = xhr.responseText;
    }

}
function showImages() {
    var imgs = document.getElementsByClassName('img');
    for (var i=0, item; item = imgs[i]; i++) {
        item.innerHTML = '<img src="../getStudentImg/small/'+item.id+'"/>'
    }
    document.getElementById('showImages').innerHTML = '';
    students = document.getElementsByClassName('student');
    for (var i=0, item; item = students[i]; i++) {
        item.style.marginLeft = '75px';
    }
    memos = document.getElementsByName('memo');
    for (var i=0, item; item = memos[i]; i++) {
        item.style.width = '100%';
    }
}
// start-stuff:
if (l.lid == '') {
    title.innerHTML = 'Neue Stunde hinzufügen';
    edit();
} else {
    for (var i = 0; i < c.length; i++) {
        if (c[i].cid == l.cid) {
            var cl = c[i];
        }
    }
    title.innerHTML = 'Stunde von: '+cl.name+' '+cl.subject;
    pagenav.innerHTML = '\
        <a onclick="show()">Anzeigen</a> | \
        <a onclick="edit()">Bearbeiten</a> | \
        <a onclick="showAttendances()">Teilnahmen</a> | \
        <a href="../class/'+cl.cid+'">&rarr; '+cl.name+' '+cl.subject+'</a>';
    show();
}    

</script>
