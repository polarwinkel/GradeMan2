class Polalert {
    constructor() {
        this.bgBox = document.createElement('div');
        this.bgBox.setAttribute('id', 'polalertBg');
        this.bgBox.style.display = 'none';
        this.bgBox.style.position = 'fixed';
        this.bgBox.style.z_index = '1';
        this.bgBox.style.left = '0';
        this.bgBox.style.top = '0';
        this.bgBox.style.height = '100%';
        this.bgBox.style.width = '100%';
        this.bgBox.style.overflow = 'auto'; // Enable scroll
        this.bgBox.style.background = 'rgba(0,0,0,0.5)';
        this.box = document.createElement('div');
        this.box.parent = this.bgBox;
        this.box.setAttribute('id', 'polalert');
        this.box.style.display = 'block';
        this.box.style.minHeight = '200px';
        this.box.style.width = '50%';
        this.box.style.minWidth = '300px';
        this.box.style.backgroundColor = 'rgba(200, 200, 200, 0.8)';
        this.box.style.backdropFilter = 'blur(5px)';
        this.box.style.boxShadow = '10px 10px 5px rgba(0,0,0,0.5)';
        this.box.style.borderRadius = '10px';
        this.box.style.marginLeft = '25%';
        this.box.style.marginTop = '100px';
        this.box.style.padding = '20px';
        this.box.style.textAlign = 'center';
        this.box.style.fontSize = '1.6rem';
        this.bgBox.appendChild(this.box);
        this.buttonOk = document.createElement('button');
        this.buttonOk.parent = this.box;
        this.buttonOk.setAttribute('id', 'polalertOk');
        this.buttonOk.style.width = '200px';
        this.buttonOk.style.backgroundColor = 'rgba(0, 200, 0, 0.8)';
        this.buttonOk.style.border = '5px solid silver';
        this.buttonOk.style.borderRadius = '10px';
        this.buttonOk.style.fontSize = '1.6rem';
        this.buttonOk.innerHTML = '<p>OK</p>';
        this.buttonNo = document.createElement('button');
        this.buttonNo.parent = this.box;
        this.buttonNo.setAttribute('id', 'polalertNo');
        this.buttonNo.style.width = '200px';
        this.buttonNo.style.backgroundColor = 'rgba(200, 0, 0, 0.8)';
        this.buttonNo.style.border = '5px solid silver';
        this.buttonNo.style.borderRadius = '10px';
        this.buttonNo.style.fontSize = '1.6rem';
        this.buttonNo.innerHTML = '<p>No</p>';
    }
    next() {
    }
    hello() {
        this.box.innerHTML = '<p>Hello World!</p>';
        this.box.appendChild(this.buttonOk);
        document.body.appendChild(this.bgBox);
        this.buttonOk.onclick = function () {
            var bg = document.getElementById('polalertBg');
            document.body.removeChild(bg);
        };
        this.bgBox.style.display = 'block';
    }
    message(msg) {
        this.box.style.backgroundColor = 'rgba(255, 255, 255, 0.7)';
        this.box.style.backdropFilter = 'blur(5px)';
        this.box.innerHTML = '<p>'+msg+'</p>';
        this.box.appendChild(this.buttonOk);
        document.body.appendChild(this.bgBox);
        this.buttonOk.onclick = function () {
            var bg = document.getElementById('polalertBg');
            document.body.removeChild(bg);
        };
        this.bgBox.style.display = 'block';
    }
    warning(warn) {
        this.box.style.backgroundColor = 'rgba(255, 180, 0, 0.7)';
        this.box.style.backdropFilter = 'blur(5px)';
        this.box.innerHTML = '<p>'+warn+'</p>';
        this.box.appendChild(this.buttonOk);
        document.body.appendChild(this.bgBox);
        this.buttonOk.onclick = function () {
            var bg = document.getElementById('polalertBg');
            document.body.removeChild(bg);
        };
        this.bgBox.style.display = 'block';
    }
    error(err) {
        this.box.style.backgroundColor = 'rgba(255, 50, 50, 0.7)';
        this.box.style.backdropFilter = 'blur(5px)';
        this.box.innerHTML = '<p>'+err+'</p>';
        this.box.appendChild(this.buttonOk);
        document.body.appendChild(this.bgBox);
        this.buttonOk.onclick = function () {
            var bg = document.getElementById('polalertBg');
            document.body.removeChild(bg);
        };
        this.bgBox.style.display = 'block';
    }
    boolean(msg, str='') {
        this.answer = null;
        this.box.innerHTML = '<p>'+msg+'</p>';
        this.box.appendChild(this.buttonOk);
        this.buttonOk.onclick = function () {
            var bg = document.getElementById('polalertBg');
            document.body.removeChild(bg);
            paOk(str);
        };
        this.box.appendChild(this.buttonNo);
        this.buttonNo.onclick = function () {
            var bg = document.getElementById('polalertBg');
            document.body.removeChild(bg);
            paNo(str);
        };
        document.body.appendChild(this.bgBox);
        this.bgBox.style.display = 'block';
        return[this.buttonOk, this.buttonNo];
    }
}
var pa = new Polalert();
