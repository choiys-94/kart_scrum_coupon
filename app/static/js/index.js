

var load = false;
var cur_lang;
var cur;
var cur_class;
var org_content;
var prev_lang = "python";

function lang_select() {
    cur_lang = "python";
    cur = document.querySelector("code");
    cur_class = cur.className;
    if(cur_class.indexOf("python") >= 0) {
        cur_lang = "python"; 
    }
    else {
        cur_lang = "javascript";
    }
    return cur_lang;
}

function save_code(content, lang) {
    if(content === undefined) {
        cur = document.querySelector("code");
        content = cur.innerHTML;
    }
    if(lang === undefined) {
        cur_lang = lang_select();
    }
    else{
        cur_lang = lang
    }

    let http = new XMLHttpRequest();
    let req = new Object();
    req.lang = cur_lang;
    req.content = content;
    req.org_content = document.querySelector("code").textContent;
    http.onreadystatechange = () => {
        if(http.readyState === XMLHttpRequest.DONE) {
            if(http.status === 200) {
                let res = http.response;
                if(res.status !== "success") {
                    alert("error!");
                }
            }
        }
    }
    http.open("POST", "/code/savecode", true);
    http.responseType = "json";
    http.setRequestHeader("Content-Type", "application/json")
    http.send(JSON.stringify(req));
}

function load_code() {
    cur_lang = lang_select();
    let http = new XMLHttpRequest();
    let req = new Object();
    req.lang = cur_lang;
    http.onreadystatechange = () => {
        if(http.readyState === XMLHttpRequest.DONE) {
            if(http.status === 200) {
                let res = http.response;
                if(res.status !== "success") {
                    alert("error!");
                    return
                }
                cur.innerHTML = res.data;
                load = true;
            }
        }
    }
    http.open("POST", "/code/loadcode", true);
    http.responseType = "json";
    http.setRequestHeader("Content-Type", "application/json")
    http.send(JSON.stringify(req));
}

// load source code when start
setTimeout(function() {
    load_code();
}, 1000);

// save source code every 20s
setInterval(function() {
    if(load === false) {
        return;
    }
    save_code(cur.innerHTML);
}, 20000);

function language_toggle(current) {
    if(current){
        let content = document.querySelector("code").innerHTML;
        let cur_lang = current.querySelector("input").id;
        let code = document.getElementsByTagName("code")[0];
        if(cur_lang.indexOf("opt_python") === 0){
            code.className = "language-python";
            if(prev_lang === "javascript")
                save_code(content, "javascript");

            prev_lang = "python";
        }
        else{
            code.className = "language-javascript";
            if(prev_lang === "python")
                save_code(content, "python");
                
            prev_lang = "javascript";
        }
        load_code().then(Prism.highlightElement(code));
    }
}

function frida_run() {
    save_code(cur.innerHTML);
    
    let http = new XMLHttpRequest();
    http.onreadystatechange = () => {
        if(http.readyState === XMLHttpRequest.DONE) {
            if(http.status === 200) {
                let res = http.response;
                if(res.status !== "success") {
                    alert("error!");
                    return
                }
                console.log(res.data);
            }
        }
    }
    http.open("POST", "/frida/run", true);
    http.responseType = "json";
    http.setRequestHeader("Content-Type", "application/json")
    http.send();
}