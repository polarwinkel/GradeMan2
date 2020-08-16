<h1 id="title" onclick="location.reload()">{{ s['givenname'] }} {{ s['familyname'] }}</h1>
<nav id="pagenav">
    <a onclick="edit()">Bearbeiten</a>
</nav>
<div id="content">
    <p>Notizen:</p>
    <div style="width:100%; border:1px solid black;">
        {{ memo }}
    </div>
    {% if img == '' %}
        <p>[kein Bild Vorhanden]</p>
        <p><a href="../setStudentImg/{{ s['sid'] }}">Bild hinzufügen</a></p>
    {% else %}
        <img src="data:image/jpeg;base64,{{ img }}"/>
        <p><a href="../setStudentImg/{{ s['sid'] }}">Bild aktualisieren</a></p>
    {% endif %}
    {% if s['gender'] == 'male' %}
        <p>Geschlecht: &#9794;</p>
    {% elif s['gender'] == 'female' %}
        <p>Geschlecht: &#9792;</p>
    {% elif s['gender'] == 'other' %}
        <p>Geschlecht: &#9893;</p>
    {% else %}
        <p>Geschlecht: unbekannt</p>
    {% endif %}
    <p>
        Klassen:<ul>
        {% for c in sclasses %}
            <li><a href="../class/{{ c['cid'] }}">{{ c['name'] }}</a></li>
        {% endfor %}
        </ul>
    </p>
</div>
<script>
var s = {{ sjson }};

function edit() {
    content = '\
        <input type="hidden" id="what" name="what" class="formdata" value="student" />\
        <input type="hidden" id="sid" name="sid" class="formdata" />\
        <div style="clear:both;"><label for="givenname">Vorname: </label><input type="text" name="givenname" id="givenname" class="formdata" required /></div>\
        <div style="clear:both;"><label for="familyname">Nachname: </label><input type="text" name="familyname" id="familyname" class="formdata" required /></div>\
        <div style="clear:both;"><label for="gender">Geschlecht: </label><select id="gender" name="gender" class="formdata">\
            <option value="None" id="None">unbekannt</option>\
            <option value="male" id="male">männlich</option>\
            <option value="female" id="female">weiblich</option>\
            <option value="other" id="other">andere</option>\
        </select></div>\
        <div style="clear:both;"><label for="memo">Notizen: </label><textarea name="memo" id="memo" class="formdata"></textarea></div>\
        <p style="clear:both;">\
        {% for c in classes %}\
            <label for="cid{{ c["cid"] }}">{{ c["name"] }}</label>\
            {% if c in sclasses %}\
                <input type="checkbox" id="cid{{ c["cid"] }}" name="cids" class="formdata" value="{{ c["cid"] }}" checked /><br />\n\
            {% else %}\
                <input type="checkbox" id="cid{{ c["cid"] }}" name="cids" class="formdata" value="{{ c["cid"] }}" /><br />\n\
            {% endif %}\
        {% endfor %}\
        </p>\
        <div style="clear:both; text-align:center;">\
        </div>\
        <input type="submit" value="Speichern" onclick="send()">\
    '
    document.getElementById('content').innerHTML = content;
    document.getElementById('sid').value = s.sid;
    document.getElementById('givenname').value = s.givenname;
    document.getElementById('familyname').value = s.familyname;
    document.getElementById('memo').innerHTML = s.memo;
    if (s['gender'] != '') {
        document.getElementById(s['gender']).selected = true;
    }
}
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
function send() {
    var xhr = new XMLHttpRequest();
    var formJson = getFormJson();
    if (formJson.sid=='') {
        xhr.open('POST', '../newDbEntry', false);
    } else {
        xhr.open('POST', '../updateDbEntry', false);
    }
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(formJson));
    if (formJson.sid=='') { // new
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

if (s.sid == '') {
    document.getElementById('title').innerHTML = 'Neuen Schüler hinzufügen';
    edit();
}
</script>
