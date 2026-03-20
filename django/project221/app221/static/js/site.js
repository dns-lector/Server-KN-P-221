console.log("Script works")
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById("query-button");
    if(btn) {
        btn.addEventListener('click', onSendQueryClick);
    }
});

function onSendQueryClick() {
    const inp = document.getElementById("query-data");
    if(!inp) {
        throw "#query-data not found";
    }
    let url = window.location.href;
    url = url.split('?')[0];
    url += "?x=" + encodeURIComponent(inp.value);
    window.location = url;
}