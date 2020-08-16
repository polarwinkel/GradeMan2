<h1>Cheatsheet <code>mdTeX</code></h1>
<h2>Sandbox</h1>
<textarea oninput="preview()" id="mdTeXCode"" rows="5" cols="72">
</textarea><br />
<button type="button" onclick="render()">Rendern</button>
<h3>Rendering</h3>
<div id="mathmlView" style="border:1px solid black;"></div>
<h3>Rendered Code</h3>
<textarea oninput="preview()" id="renderedCode"" rows="5" cols="72">
</textarea><br />
<h2>Snippets</h2>
<table>
    <tr>
        <th>Operator/Zeichen</th>
        <th>Beispiel</th>
        <th>Code</th>
    </tr>
    <tr>
        <td>Überschrift</td>
        <td><h4>Überschrift 4</h4></td>
        <td><code>#### Überschrift 4</code></td>
    </tr>
    <tr>
        <td>Aufzählung</td>
        <td>
            <ol>
                <li>Punkt 1<br/>zweizeilig</li>
                <li>Punkt 2</li>
            </ol>
        </td>
        <td><pre><code>
            1. Punkt 1
                zweizeilig
            1. Punkt 2
        </code></pre></td>
    </tr>
    <tr>
        <td>Bulletpoints</td>
        <td>
            <ul>
                <li>Punkt 1</li>
                <li>Punkt 2</li>
            </ul>
        </td>
        <td><pre><code>
            - Punkt 1
            - Punkt 2
        </code></pre></td>
    </tr>
    <tr>
        <td>(inline-) Bruch</td>
        <td><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mfrac><mrow><mi>a</mi></mrow><mrow><mi>b</mi></mrow></mfrac></mrow></math></td>
        <td><code>$\frac{a}{b}$</code></td>
    </tr>
    <tr>
        <td>Wurzel</td>
        <td><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><msqrt><mrow><mi>a</mi></mrow></msqrt></mrow></math></td>
        <td><code>$\sqrt{a}$</code></td>
    </tr>
    <tr>
        <td>Mal-Punkt</td>
        <td><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mi>a</mi><mo>&#x022C5;</mo><mi>b</mi></mrow></math></td>
        <td><code>$a \cdot b$</code></td>
    </tr>
    <tr>
        <td>Grad Celsius</td>
        <td><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><msup><mn>42</mn><mo>&#x02218;</mo></msup><mi>C</mi></mrow></math></td>
        <td><code>$42^\circ C$</code></td>
    </tr>
    <tr>
        <td>Block-Formel</td>
        <td><math xmlns="http://www.w3.org/1998/Math/MathML"><mrow><mi>f</mi><mo>&#x00028;</mo><mi>x</mi><mo>&#x00029;</mo><mo>&#x02248;</mo><mi>.</mi><mi>.</mi><mi>.</mi></mrow></math></td>
        <td><code>$$f(x)\approx ...$$</code></td>
    </tr>
</table>

<script>
    function mdtex2html(mdtex) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "mdtex2html", false);
        xhr.setRequestHeader("Content-Type", "application/mdtex");
        xhr.send(mdtex);
        return xhr.responseText;
    }
    function render() {
        mdtex = document.getElementById("mdTeXCode").value;
        html = mdtex2html(mdtex);
        document.getElementById("mathmlView").innerHTML = html;
        document.getElementById("renderedCode").value = html;
    }
</script>
