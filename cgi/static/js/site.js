document.addEventListener('DOMContentLoaded', () => {
    initApiTests();
});

function initApiTests() {
    const apiNames = ["user"];
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
    if(td) {
        fetch(`/${apiName}`, {
            method: apiMethod.toUpperCase(),
            headers: {
                "Access-Control-Allow-Origin": "cgi221.loc",
                "My-Custom-Header": "My Value",
                "Authorization": "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="   // приклад з RFC7617 (Aladdin:open sesame)
            }
        }).then(r => {
            if(r.ok) {
               r.json().then(j => td.innerHTML = `<pre>${JSON.stringify(j, null, 4)}</pre>` );
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
Д.З. Створити АРІ для сервісу замовлень /order :
створити АРІ-контролер з повним переліком методів (get, post, put, patch, delete)
створити тестовий контролер, що виводить кнопки для тестів кожного з методів
реалізувати та перевірити роботу кнопок, на даному етапі обмежитись 
 виведенням назви АРІ (order) та методу, яким буде надіслано запит

*/