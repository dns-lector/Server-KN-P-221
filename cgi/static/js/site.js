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
});

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
                //     : `Bearer ${token}`
                   : `Bearer eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.QWxhZGRpbjpvcGVuIHNlc2FtZQ=.t0VAp--8WIiYLE7WPKuLf24yNimhJIdH4MzhcIBYIkg=`  // inv padding in payload
                

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
Д.З. Додати до сторінки з випробуванням АРІ автентифікації
поле з інформацією про заголовок токена, що приходить у відповідь

 eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJzdWIiOiAiMjk2YzdmMDctYmExYS0xMWYwLTgzYjYtNjI1MTc2MDA1OTZjIiwgImlzcyI6ICJTZXJ2ZXItS04tUC0yMjEiLCAiYXVkIjogImFkbWluIiwgImlhdCI6IDE3NjY0MTE2MjUuNTM3NTQ2LCAibmFtZSI6ICJEZWZhdWx0IEFkbWluaXN0cmF0b3IiLCAiZW1haWwiOiAiY2hhbmdlLm1lQGZha2UubmV0In0=.KLdjS77gTm4G2f_1VWY61I3ILMJHTNgID0FB3wUn4jQ=


*/