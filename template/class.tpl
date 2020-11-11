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
<style>
    table#achievements {
        border:1px solid #888;
        width:100%;
        border-collapse: collapse;
    }
    table#achievements tr { border: 1px dashed #888; }
    table#achievements th {
        border-right:1px solid #888; 
        border-left:1px solid #888;
        line-height: 90%;
    }
    table#achievements td {
        border-right:1px solid #888; 
        border-left:1px solid #888;
    }
</style>
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
    var url = '../json/classAttendances/'+c.cid;
    fetch(url).then(function(response) {
        if (response.ok) {
            return response.json();
        }
        else 
            throw new Error('ERROR: Attendances could not be fetched from server!');
    })
    .then(function(ajson) {
        content.innerHTML = 'Die Leistungsübersicht wird geladen...';
        
        head = '';
        for (var i=0; i<ajson.students.length; i++) {
            head += '<th><a href="../student/'+ajson.students[i].sid+'">';
            for (var j=0; j<ajson.students[i].givenname.length; j++) {
                head += ajson.students[i].givenname.charAt(j)+'<br />';
            }
            head += '</a></th>';
        }
        head += '</tr>';
        
        special = '';
        normal = '';
        checks = '';
        sMissedLessons = new Array(ajson.students.length).fill(0);
        sUnexcused = new Array(ajson.students.length).fill(0);
        sNoHomework = new Array(ajson.students.length).fill(0);
        sPerformance = new Array(ajson.students.length).fill(0);
        sPerformanceN = new Array(ajson.students.length).fill(0);
        sParticipation = new Array(ajson.students.length).fill(0);
        sParticipationN = new Array(ajson.students.length).fill(0);
        for (var i=0; i<ajson.attendances.length; i++) {
            if (ajson.attendances[i].lid == lShort[i].lid) {
                count = lShort[i].count;
                if (!isNaN(parseFloat(count)) && isFinite(count) && (parseFloat(count)>0)) {
                    // normal lesson
                    normal += '<tr><td><a href="../lesson/'+lShort[i].lid+'">'+lShort[i].date+'</a></td>\n';
                    normal += '<td>'+lShort[i].count+'</td>\n';
                    checks += '<tr><td><a href="../lesson/'+lShort[i].lid+'">'+lShort[i].date+'</a></td>\n';
                    checks += '<td>'+lShort[i].count+'</td>\n';
                    for (var j=0; j<ajson.students.length; j++) {
                        var sid = ajson.students[j].sid;
                        // create rows for performance:
                        if (ajson.attendances[i][sid] != {} && ajson.attendances[i][sid].performance != null) {
                            normal += '<td>'+ajson.attendances[i][sid].performance+'<br />';
                            if (!isNaN(parseFloat(ajson.attendances[i][sid].performance))) {
                                sPerformance[j] = sPerformance[j] + (parseFloat(ajson.attendances[i][sid].performance)*parseFloat(count));
                                sPerformanceN[j] = sPerformanceN[j] + parseFloat(count);
                            }
                            normal += ajson.attendances[i][sid].participation+'</td>';
                            if (!isNaN(parseFloat(ajson.attendances[i][sid].participation))) {
                                sParticipation[j] = sParticipation[j] + (parseFloat(ajson.attendances[i][sid].participation)*parseFloat(count));
                                sParticipationN[j] = sParticipationN[j] + parseFloat(count);
                            }
                        } else {
                            normal += '<td>&varnothing;</td>';
                        }
                        // create rows for checkes values (i.e. attendances):
                        checks += '<td>';
                        if (ajson.attendances[i][sid].attendant=='False') {
                            sMissedLessons[j] += parseFloat(count);
                            if (ajson.attendances[i][sid].excused=='False') {
                                checks += '<span style="color:red;">&#9744;</span><br />';
                                sUnexcused[j] += parseFloat(count);
                            } else {
                                checks += '<span style="color:green;">&#9744;</span><br />';
                            }
                        } else {
                            checks += '&#9745;<br />';
                        }
                        if (ajson.attendances[i][sid].homework=='False') {
                            checks += '<span style="color:red;">&#9744;</span>';
                            sNoHomework[j] = sNoHomework[j] + 1;
                        } else {
                            checks += '&#9745;';
                        }
                        checks += '</ td>';
                    }
                    normal += '</tr>\n';
                    checks += '</tr>\n';
                }
                else {
                    // special lesson, like a test or a count of 0
                    special += '<tr><td><a href="../lesson/'+lShort[i].lid+'">'+lShort[i].date+'</a></td>\n';
                    special += '<td>'+lShort[i].count+'</td>\n';
                    for (var j=0; j<ajson.students.length; j++) {
                        var sid = ajson.students[j].sid;
                        if (ajson.attendances[i][sid] != {}) {
                            special += '<td>'+ajson.attendances[i][sid].performance+'<br />';
                            special += ajson.attendances[i][sid].participation+'</td>';
                        } else {
                            special += '<td>&varnothing;</td>';
                        }
                    }
                    special += '</tr>\n';
                }
            } else {
                console.log('ERROR: Inkonsistent Data!');
            }
        }
        
        out = '<h2>Leistungsübersicht</h2>\n';
        // total:
        out += '<h3>Gesamt</h3>\n';
        out += '<table id="achievements"><tr><th></th><th>F</th>\n';
        out += head;
        out += '<tr><td>Fehlstunden</td><td></td>\n';
        for (var j=0; j<ajson.students.length; j++) {
            out += '<td>';
            out += (sMissedLessons[j]);
            out += '</td>\n';
        }
        out += '</tr>\n';
        out += '<tr><td>Unentschuldigt</td><td></td>\n';
        for (var j=0; j<ajson.students.length; j++) {
            out += '<td>';
            out += (sUnexcused[j]);
            out += '</td>\n';
        }
        out += '</tr>\n';
        out += '<tr><td>keine Hausaufgaben</td><td></td>\n';
        for (var j=0; j<ajson.students.length; j++) {
            out += '<td>';
            out += (sNoHomework[j]);
            out += '</td>\n';
        }
        out += '</tr>\n';
        out += '<tr><td>Fachlich</td><td></td>\n';
        console.log(sPerformanceN);
        for (var j=0; j<ajson.students.length; j++) {
            out += '<td>';
            if (sPerformanceN[j] > 0) {
                out += (sPerformance[j]/sPerformanceN[j]).toFixed(1);
            } else {
                out += '-';
            }
            out += '</td>\n';
        }
        out += '</tr>\n';
        out += '<tr><td>Mitarbeit</td><td></td>\n';
        for (var j=0; j<ajson.students.length; j++) {
            out += '<td>';
            if (sParticipationN[j] > 0) {
                out += (sParticipation[j]/sParticipationN[j]).toFixed(1);
            } else {
                out += '-';
            }
            out += '</td>\n';
        }
        out += '</tr></table>\n';
        out += '<p><i><b>Hinweis:</b> Es werden für die Gesamtberechnung nur reguläre Stunden berücksichtigt.</i></p>';
        // special lessons:
        out += '<h3>Sonderstunden</h3>\n';
        out += '<table id="achievements"><tr><th>Datum</th><th>F</th>\n';
        out += head;
        out += special;
        out += '</tr></table>\n';
        // normal lessons:
        out += '<h3>reguläre Stunden</h3>\n';
        out += '<table id="achievements"><tr><th>Datum</th><th>F</th>\n';
        out += head;
        out += normal;
        out += '</tr></table>\n';
        // checkmarks:
        out += '<h3>Anwesenheiten / keine Hausaufgaben</h3>\n';
        out += '<table id="achievements"><tr><th>Datum</th><th>F</th>\n';
        out += head;
        out += checks;
        out += '</tr></table>\n';
        out += '<p><i><b>Legende: </b>Erster Kasten: Anwesenheit, <span style="color:green;">&#9744;</span>/<span style="color:red;">&#9744;</span> heißt entschuldigt/unentschuldigt; zweiter Kasten: Hausaufgaben</i></p>';
        content.innerHTML = out;
    })
    .catch(function(err) {
        console.log(err);
    });
}
</script>
