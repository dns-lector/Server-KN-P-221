class Base64 {
    static #textEncoder = new TextEncoder();
    static #textDecoder = new TextDecoder();

    // https://datatracker.ietf.org/doc/html/rfc4648#section-4
    static encode = (str) => btoa(String.fromCharCode(...Base64.#textEncoder.encode(str)));
    static decode = (str) => Base64.#textDecoder.decode(Uint8Array.from(atob(str), c => c.charCodeAt(0)));
    
    // https://datatracker.ietf.org/doc/html/rfc4648#section-5
    static encodeUrl = (str) => this.encode(str).replace(/\+/g, '-').replace(/\//g, '_'); //.replace(/=+$/, '');
    static decodeUrl = (str) => this.decode(str.replace(/\-/g, '+').replace(/\_/g, '/'));

    static jwtEncodeBody = (header, payload) => this.encodeUrl(JSON.stringify(header)) + '.' + this.encodeUrl(JSON.stringify(payload));
    static jwtDecodePayload = (jwt) => JSON.parse(this.decodeUrl(jwt.split('.')[1]));
}

document.addEventListener('DOMContentLoaded', () => {
    initApiTests();
    for(let btn of document.querySelectorAll("[data-token]")) {
        btn.addEventListener('click', selfTestButtonClick);
    }
    const allBtn = document.getElementById("run-all-tests");
    if(allBtn) allBtn.addEventListener("click", runAllTestsClicked);
});

function runAllTestsClicked() {
    for(let btn of document.querySelectorAll("[data-token]")) {
        btn.click();
    }
}

function selfTestButtonClick(e) {
    const token = e.target.closest("[data-token]").getAttribute("data-token");
    const tr = e.target.closest("[data-test]");
    const res = tr.querySelector("[data-result]");
    const dtl = tr.querySelector("[data-details]");
    fetch(`/discount`, {
        method: "GET",
        headers: {
            "Authorization": token
        }
    }).then(r => {
        const cls = r.status == 200 ? "test-ok" : "test-fail";
        dtl.innerHTML = `<span class="${cls}">HTTP status: <b>${r.status}</b></span><br/>`;
        return r.json();
    }).then(j => {
        let expected = dtl.getAttribute("data-isok");
        let cls = j.status.isOk.toString() == expected ? "test-ok" : "test-fail";
        dtl.innerHTML += `<span class="${cls}" title="expected code: ${expected}">REST isOk: <b>${j.status.isOk}</b></span><br/>`;
    
        expected = dtl.getAttribute("data-code");
        cls = j.status.code == expected ? "test-ok" : "test-fail";
        dtl.innerHTML += `<span class="${cls}" title="expected code: ${expected}">REST status: <b>${j.status.code}</b></span><br/>`;
    
        expected = dtl.getAttribute("data-message");
        cls = j.status.message == expected ? "test-ok" : "test-fail";
        dtl.innerHTML += `<span class="${cls}" title="expected message: ${expected}">REST message: <b>${j.status.message}</b></span><br/>`;
    
        expected = dtl.getAttribute("data-data");
        cls = j.data == expected ? "test-ok" : "test-fail";
        dtl.innerHTML += `<span class="${cls}" title="expected data: ${expected}">REST data: <b>${j.data}</b></span><br/>`;
    
    });
    
}

function initApiTests() {
    const apiNames = ["user", "discount"];
    const apiMethods = ["get", "post"];
    for(let apiName of apiNames) {
        for(let apiMethod of apiMethods) {
            let btnId = `api-${apiName}-${apiMethod}-btn`;
            let btn = document.getElementById(btnId);
            if(btn) {
                btn.addEventListener('click', apiTestBtnClick);
            }
        }
    }
    document.querySelector('[data-id="api-discount-get-btn"]').addEventListener('click', apiPathBtnClick);

}
function apiPathBtnClick(e) {
    const [prefix, apiName, apiMethod, _] = e.target.getAttribute("data-id").split('-');
    const path = e.target.getAttribute("data-path");
    const resId = `${prefix}-${apiName}-${apiMethod}-result`;
    const td = document.querySelector(`[data-id="${resId}"]`);
    const tokenElem = document.getElementById("token");
    const token = tokenElem ? tokenElem.innerText : null;
    if(td) {
        fetch(`/${apiName}${path}`, {
            method: apiMethod.toUpperCase(),
            headers: {
                "Access-Control-Allow-Origin": "cgi221.loc",
                "My-Custom-Header": "My Value",
                "Authorization": token == null || token.length == 0
                    ? "Basic YWRtaW46YWRtaW4="
                    : `Bearer ${token}`
                    }
        }).then(r => {
            if(r.ok) {
                r.json().then(j => {
                    td.innerHTML = `<pre>${JSON.stringify(j, null, 4)}</pre>`;
                    if(j.meta.dataType == "token") {
                        document.getElementById("token").innerText = j.data;
                        const payload = JSON.parse( Base64.decodeUrl( j.data.split('.')[1] ) );
                        document.getElementById("token-payload").innerHTML = `<pre>${JSON.stringify(payload, null, 4)}</pre>`;
                    }
                });
            }
            else {
                r.text().then(t => td.innerText = t);
            }
        });
    }
    else {
        throw "Container not found: " + resId;
    }
}


function apiTestBtnClick(e) {
    const [prefix, apiName, apiMethod, _] = e.target.id.split('-');
    const resId = `${prefix}-${apiName}-${apiMethod}-result`;
    const td = document.getElementById(resId);
    const tokenElem = document.getElementById("token");
    const token = tokenElem ? tokenElem.innerText : null;
    if(td) {
        fetch(`/${apiName}`, {
            method: apiMethod.toUpperCase(),
            headers: {
                "Access-Control-Allow-Origin": "cgi221.loc",
                "My-Custom-Header": "My Value",
                "Authorization": token == null || token.length == 0
                    ? "Basic YWRtaW46YWRtaW4="
                    : `Bearer ${token}`
                //    : `Bearer `
                //    : `Bearer `
                //    : `Bearer `
                //    : `Bearer eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJzdWIiOiAiMjk2YzdmMDctYmExYS0xMWYwLTgzYjYtNjI1MTc2MDA1OTZjIiwgImlzcyI6ICJTZXJ2ZXItS04tUC0yMjEiLCAiYXVkIjogImFkbWluIiwgImlhdCI6IDE3NjY0ODMyNDIuODQ2MzM2LCAibmFtZSI6ICJEZWZhdWx0IEFkbWluaXN0cmF0b3IiLCAiZW1haWwiOiAiY2hhbmdlLm1lQGZha2UubmV0In0=.s-i8D1SaFmBOFChFyUzBL3RoM-sRsjpTcApSs7HxcNE=`   // max time exceeded
                //    : `Bearer eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJzdWIiOiAiMjk2YzdmMDctYmExYS0xMWYwLTgzYjYtNjI1MTc2MDA1OTZjIiwgImlzcyI6ICJTZXJ2ZXItS04tUC0yMjEiLCAiYXVkIjogImFkbWluIiwgImV4cCI6IDE3NjY1ODE3MDkuNDIyMjMsICJuYW1lIjogIkRlZmF1bHQgQWRtaW5pc3RyYXRvciIsICJlbWFpbCI6ICJjaGFuZ2UubWVAZmFrZS5uZXQifQ==.R3xWirh5p5ZP2J0HjdLhIEMI8IFYLvRHS5QZOSkFCLA=`  // expired
                //    : `Bearer eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJzdWIiOiAiMjk2YzdmMDctYmExYS0xMWYwLTgzYjYtNjI1MTc2MDA1OTZjIiwgImlzcyI6ICJTZXJ2ZXItS04tUC0yMjEiLCAiYXVkIjogImFkbWluIiwgIm5iZiI6ICJxd2UiLCAibmFtZSI6ICJEZWZhdWx0IEFkbWluaXN0cmF0b3IiLCAiZW1haWwiOiAiY2hhbmdlLm1lQGZha2UubmV0In0=.WTc4iZABha5WhPIVgqA3WmYrIINiWbGI2Jb4bmYvIvw=`  // "nbf": "qwe"
                //    : `Bearer eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJzdWIiOiAiMjk2YzdmMDctYmExYS0xMWYwLTgzYjYtNjI1MTc2MDA1OTZjIiwgImlzcyI6ICJTZXJ2ZXItS04tUC0yMjEiLCAiYXVkIjogImFkbWluIiwgIm5iZiI6IDI3NjY1ODAxNzUuOTYzNzk1NywgIm5hbWUiOiAiRGVmYXVsdCBBZG1pbmlzdHJhdG9yIiwgImVtYWlsIjogImNoYW5nZS5tZUBmYWtlLm5ldCJ9.SBJBN907KpskihGeQH0_dr5ja5BSxAbNnHEGySnvAZY=`  // nbf violation
                //    : `Bearer eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJzdWIiOiAiMjk2YzdmMDctYmExYS0xMWYwLTgzYjYtNjI1MTc2MDA1OTZjIiwgImlzcyI6ICJTZXJ2ZXItS04tUC0yMjEiLCAiYXVkIjogImFkbWluIiwgIm5hbWUiOiAiRGVmYXVsdCBBZG1pbmlzdHJhdG9yIiwgImVtYWlsIjogImNoYW5nZS5tZUBmYWtlLm5ldCJ9.tnCQYYPFRqbBhr0KGxzjwu4MYR9Nepp8MSpl94kRHLA=`  // no time fields
                //    : `Bearer eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.QWxhZGRpbjpvcGVuIHNlc2FtZQ=.t0VAp--8WIiYLE7WPKuLf24yNimhJIdH4MzhcIBYIkg=`  // inv padding in payload
                

                //    : `Bearer eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJzdWIiOiAiMjk2YzdmMDctYmExYS0xMWYwLTgzYjYtNjI1MTc2MDA1OTZjIiwgImlzcyI6ICJTZXJ2ZXItS04tUC0yMjEiLCAiYXVkIjogImFkbWluIiwgImlhdCI6IDE3NjY0OTcwMjguMzYyNjY4LCAibmFtZSI6ICJEZWZhdWx0IEFkbWluaXN0cmF0b3IiLCAiZW1haWwiOiAiY2hhbmdlLm1lQGZha2UubmV0In0=.exbzzOlFhoqGr1h0s9t26Pa9AX8reGvUR5MqZdGfzDg=`  // inv signature
                //    : `Bearer eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJzd.WIiO.iAiMjk`  // inv parts count                                                                                                                                                                                                           c3xGMQEj7aIRnhxEN7M7lAJ1-GRBoFrCea9Phj1NCXg=                                                    
                //    : `Bearer eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJzdWIiOiAiMjk`  // inv parts count
                //    : `Bearer eyJ0eXAiOiJKV1QiLCAiYWxnIjoiSFMyNTUifQ==.eyJzdWIiOiA`  // inv 'alg' field
                //    : `Bearer eyJ0eXAiOiJKV1QiLCAiYWxnMSI6IkhTMjU1In0=.eyJzdWIiOiA`  // no 'alg' field
                //    : `Bearer eyJ0eXAiOiIxMjMifQ==.eyJzdWIiOiA`  // inv 'typ' field
                //    : `Bearer eyJ0dHAiOiIxMjMifQ==.eyJzdWIiOiA`  // no 'typ' field
                //    : `Bearer WzEsMiwzXQ==.eyJzdWIiOiA`  // non-object (array)
                //    : `Bearer MiszPTU=.eyJzdWIiOiA`  // non-json
                //    : `Bearer 000000000000.eyJzdWIiOiA`  // utf-8 error
                //    : `Bearer QWxhZGRpbjpvcGVuIHNlc2FtZQ=.eyJzdWIiOiA`  // padding error
                // "Authorization": "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="   // приклад з RFC7617 (Aladdin:open sesame)
            }
        }).then(r => {
            if(r.ok) {
                r.json().then(j => {
                    td.innerHTML = `<pre>${JSON.stringify(j, null, 4)}</pre>`;
                    if(j.meta.dataType == "token") {
                        document.getElementById("token").innerText = j.data;
                        const payload = JSON.parse( Base64.decodeUrl( j.data.split('.')[1] ) );
                        document.getElementById("token-payload").innerHTML = `<pre>${JSON.stringify(payload, null, 4)}</pre>`;
                    }
                });
            }
            else {
                r.text().then(t => td.innerText = t);
            }
        });
    }
    else {
        throw "Container not found: " + resId;
    }
}
/*
Д.З. Завершити роботу над сторінкою з випробуванням АРІ автентифікації
Головна задача: вивести загальний пісумок всіх тестів (по їх завершенню)

 eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJzdWIiOiAiMjk2YzdmMDctYmExYS0xMWYwLTgzYjYtNjI1MTc2MDA1OTZjIiwgImlzcyI6ICJTZXJ2ZXItS04tUC0yMjEiLCAiYXVkIjogImFkbWluIiwgImlhdCI6IDE3NjY0MTE2MjUuNTM3NTQ2LCAibmFtZSI6ICJEZWZhdWx0IEFkbWluaXN0cmF0b3IiLCAiZW1haWwiOiAiY2hhbmdlLm1lQGZha2UubmV0In0=.KLdjS77gTm4G2f_1VWY61I3ILMJHTNgID0FB3wUn4jQ=


*/