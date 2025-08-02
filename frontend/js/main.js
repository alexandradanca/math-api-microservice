// JavaScript logic extracted from index.html
const API = 'http://localhost:8000';
function showPage(page) {
    document.querySelectorAll('.page').forEach(p => p.style.display = 'none');
    document.getElementById('page-' + page).style.display = 'block';
}
function setActiveNav(page) {
    document.querySelectorAll('.sidebar nav a').forEach(a => a.classList.remove('active'));
    document.getElementById('nav-' + page).classList.add('active');
}
function navigate() {
    const hash = window.location.hash.replace('#', '') || 'power';
    showPage(hash);
    setActiveNav(hash);
    if(window.innerWidth <= 800) document.getElementById('sidebar').classList.remove('open');
}
window.addEventListener('hashchange', navigate);
window.addEventListener('DOMContentLoaded', navigate);
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('sidebarToggle').onclick = function() {
        document.getElementById('sidebar').classList.toggle('open');
    };
});
async function callPow() {
    const base = document.getElementById('pow-base').value;
    const exp = document.getElementById('pow-exp').value;
    const res = await fetch(`${API}/pow`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-api-key': 'secret123'
        },
        body: JSON.stringify({ base: Number(base), exp: Number(exp) })
    });
    const data = await res.json();
    document.getElementById('result-power').innerText = 'Result: ' + (data.result ?? data.message ?? 'Error');
}
async function callFib() {
    const n = document.getElementById('fib-n').value;
    const res = await fetch(`${API}/fibonacci`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-api-key': 'secret123'
        },
        body: JSON.stringify({ n: Number(n) })
    });
    const data = await res.json();
    document.getElementById('result-fibonacci').innerText = 'Result: ' + (data.result ?? data.message ?? 'Error');
}
async function callFact() {
    const n = document.getElementById('fact-n').value;
    const res = await fetch(`${API}/factorial`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-api-key': 'secret123'
        },
        body: JSON.stringify({ n: Number(n) })
    });
    const data = await res.json();
    document.getElementById('result-factorial').innerText = 'Result: ' + (data.result ?? data.message ?? 'Error');
}
