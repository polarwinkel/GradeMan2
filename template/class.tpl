<h1 id="title" onclick="location.reload()">{{ c['name'] }} {{ c['subject'] }}</h1>
<nav id="pagenav">
    <a onclick="show()">Anzeigen</a> | 
    <a onclick="edit()">Bearbeiten</a> | 
    <a onclick="showLessons()">Curriculum</a> | 
    <a onclick="showStudents()">Schüler</a> | 
    <a onclick="learnNames()">Namen lernen</a> | 
    <a onclick="showAchievements()">Leistungen</a>
</nav>
<div id="content">
    {{ memo }}
</div>
<script src="../static/getFormJson.js"></script>
<script>
var c = {{ cjson }};
var lShort = {{ lShortJson }};
var content = document.getElementById('content');

function mdtex2html(mdtex) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '../mdtex2html', false);
    xhr.setRequestHeader('Content-Type', 'application/mdtex');
    xhr.send(mdtex);
    return xhr.responseText;
}
function edit() {
    content.innerHTML = '\
        <input type="hidden" id="what" name="what" class="formdata" value="class" />\
        <input type="hidden" id="cid" name="cid" class="formdata" />\
        <div style="clear:both;"><label for="name">Name: </label><input type="text" name="name" id="name" class="formdata" required /></div>\
        <div style="clear:both;"><label for="subject">Fach: </label><input type="text" name="subject" id="subject" class="formdata" required /></div>\
        <div style="clear:both;"><label for="graduate">Oberstufe: </label><input type="checkbox" name="graduate" id="subject" class="formdata" /></div>\
        <div style="clear:both;"><label for="memo">Notizen: </label><textarea name="memo" id="memo" class="formdata"></textarea></div>\
        <input type="submit" value="Speichern" onclick="send()">\
    '
    document.getElementById('cid').value = c.cid;
    document.getElementById('name').value = c.name;
    document.getElementById('subject').value = c.subject;
    document.getElementById('memo').innerHTML = c.memo;
}
function show() {
    if (c.cid == '') {
        document.getElementById('title').innerHTML = 'Neue Klasse hinzufügen';
        edit();
    } else {
        out = mdtex2html(c.memo);
        out += '<h2>Stunden:</h2>\n<ul>\n';
        for (var i=0; i < lShort.length; i++) {
            out += '<li><a href="{{ relroot }}lesson/'+lShort[i].lid+'">'+lShort[i].date+': '+lShort[i].topic+'</a></li>\n';
        }
        out += '</ul>';
        content.innerHTML = out;
    }
}
show();

function send() {
    var xhr = new XMLHttpRequest();
    var formJson = getFormJson();
    if (formJson.cid=='') {
        xhr.open('POST', '../newDbEntry', false);
    } else {
        xhr.open('POST', '../updateDbEntry', false);
    }
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(formJson));
    if (formJson.cid=='') { // new
        if (isNaN(xhr.responseText)) {
            content.innerHTML = xhr.responseText;
        } else {
            window.location = xhr.responseText;
        }
    } else if (xhr.responseText = 'ok') {
        location.reload();
    } else {
        content.innerHTML = xhr.responseText;
    }
}

function showLessons() {
    var url = '../json/classLessons/'+c.cid;
    fetch(url).then(function(response) {
        if (response.ok) {
            return response.json();
        }
        else 
            throw new Error('ERROR: Students could not be fetched from server!');
    })
    .then(function(ljson) {
        out = '<h2>Stunden des Kurses</h2>\n<ul>';
        for (i=0; i<ljson.length; i++) {
            out += '\
                <li><a href="{{ relroot }}lesson/'+ljson[i].lid+'">\
                '+ljson[i].date+': '+ljson[i].topic+'</a><br />\
                '+ljson[i].memo+'</li>\n';
        }
        content.innerHTML = out+'</ul>';
    })
    .catch(function(err) {
        console.log(err);
    });
}
function showStudents() {
    var url = '../json/classStudents/'+c.cid;
    fetch(url).then(function(response) {
        if (response.ok) {
            return response.json();
        }
        else 
            throw new Error('ERROR: Students could not be fetched from server!');
    })
    .then(function(sjson) {
        out = '<h2>Alle Schüler</h2>\n';
        for (i=0; i<sjson.length; i++) {
            out += '\
                <div style="border: 1px solid rgba(127,127,127,0.2); float: left; text-align:center; width: 135px; height:225px; margin: 0.3rem;"><a href="../student/'+sjson[i].sid+'">\
                '+sjson[i].givenname+'<br />'+sjson[i].familyname+'</a><br />\
                <img src="../getStudentImg/small/'+sjson[i].sid+'" alt="'+sjson[i].givenname+'" /></div>';
        }
        content.innerHTML = out+'<div style="clear:both;"></div>';
    })
    .catch(function(err) {
        console.log(err);
    });
}
function learnNames() {
    var url = '../json/classStudents/'+c.cid;
    fetch(url).then(function(response) {
        if (response.ok) {
            return response.json();
        }
        else 
            throw new Error('ERROR: Students could not be fetched from server!');
    })
    .then(function(sjson) {
        out = '<h2>Namen lernen</h2>\n';
        var i = Math.floor(Math.random() * sjson.length);
        out += '\
                <p id="name" onclick="showName(\''+sjson[i].givenname+' '+sjson[i].familyname+'\')" style="display:inline-block; width:350px; float:right;"><a>Namen anzeigen</a></p>\
                <img src="../getStudentImg/'+sjson[i].sid+'" alt="'+sjson[i].givenname+'" style="display:block; width:350px; height:450px; margin:auto;"/>'
        content.innerHTML = out;
    })
    .catch(function(err) {
        console.log(err);
    });
}
function showName(name) {
    document.getElementById('name').innerHTML='<a>'+name+'</a>';
    document.getElementById('name').onclick=function(){learnNames()}; // TODO: don't reload all students if already loaded
}
function showAchievements() {
    content.innerHTML = 'TODO';
}
</script>
