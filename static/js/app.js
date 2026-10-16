const $ = id => document.getElementById(id);
const brl = n => 'R$ ' + n.toFixed(2).replace('.', ',');
const num = v => parseFloat(String(v).replace(',', '.')) || 0;
const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
let prods = [], pedido = {}, editCod = null, delCod = null, modo = 'local';

/* ---- camada de dados: usa a API Flask; se ela não existir, guarda no navegador ---- */
const LS = 'cardapio.txt';
const seed = [{ c: 100, n: 'Pastel de carne', v: '9.50' }, { c: 101, n: 'X-Burguer da casa', v: '24.90' }, { c: 102, n: 'Porção de batata', v: '18.00' }, { c: 103, n: 'Suco de laranja', v: '8.00' }];
const lget = () => { try { const s = localStorage.getItem(LS); if (s) return JSON.parse(s) } catch (e) { } return seed.slice() };
const lput = l => { l.sort((a, b) => a.c - b.c); try { localStorage.setItem(LS, JSON.stringify(l)) } catch (e) { } };
const livre = l => { const s = new Set(l.map(p => p.c)); let c = 100; while (s.has(c)) c++; return c };
const dados = {
  async listar() { try { const r = await fetch('/api/produtos'); if (!r.ok) throw 0; modo = 'api'; return await r.json() } catch (e) { modo = 'local'; return lget() } },
  async salvar(cod, n, v) {
    if (modo === 'api') {
      const r = await fetch('/api/produtos' + (cod ? '/' + cod : ''), { method: cod ? 'PUT' : 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ n, v }) });
      const j = await r.json(); if (!r.ok) throw new Error(j.erro || 'Erro ao salvar.'); return
    }
    const l = lget(); if (cod) { const p = l.find(x => x.c === cod); p.n = n; p.v = v } else l.push({ c: livre(l), n, v }); lput(l)
  },
  async apagar(cod) {
    if (modo === 'api') { const r = await fetch('/api/produtos/' + cod, { method: 'DELETE' }); if (!r.ok) throw new Error('Erro ao apagar.'); return }
    lput(lget().filter(p => p.c !== cod))
  }
};
async function recarregar() { prods = await dados.listar(); renderAdm(); renderMenu(); renderTicket() }
function toast(t) { const e = $('toast'); e.textContent = t; e.classList.add('on'); clearTimeout(toast.t); toast.t = setTimeout(() => e.classList.remove('on'), 2200) }

/* ---- administrador ---- */
function renderAdm() {
  $('count').textContent = prods.length ? prods.length + (prods.length > 1 ? ' produtos no cardápio' : ' produto no cardápio') : 'Cardápio vazio';
  $('ledger').innerHTML = prods.length ? prods.map(p => `<div class="row"><span class="cod">${p.c}</span><span class="nm">${esc(p.n)}</span><span class="vl">${brl(num(p.v))}</span><span class="acts"><button class="btn sm" data-e="${p.c}">Alterar</button><button class="btn sm del" data-d="${p.c}">Apagar</button></span></div>`).join('') : '<div class="empty">Sem dados existentes. Use Cadastrar produto para começar.</div>'
}
$('ledger').onclick = e => {
  const b = e.target.closest('button'); if (!b) return;
  if (b.dataset.e) openForm(+b.dataset.e);
  if (b.dataset.d) { delCod = +b.dataset.d; $('delTxt').textContent = 'Você vai apagar "' + prods.find(p => p.c == delCod).n + '" do cardápio.'; $('dDel').showModal() }
};
$('novo').onclick = () => openForm(null);
function openForm(c) {
  editCod = c; const p = prods.find(x => x.c === c);
  $('fTitle').textContent = p ? 'Alterar produto' : 'Cadastrar produto';
  $('fSub').textContent = p ? 'Você está alterando o produto ' + p.n : 'O código é gerado automaticamente.';
  $('fCod').textContent = 'Código ' + (p ? p.c : livre(prods));
  $('fNome').value = p ? p.n : ''; $('fValor').value = p ? String(p.v).replace('.', ',') : ''; $('fErr').textContent = '';
  $('dForm').showModal(); $('fNome').focus()
}
$('fCancel').onclick = () => { $('dForm').close(); toast('Operação cancelada') };
$('f').onsubmit = async e => {
  e.preventDefault();
  const n = $('fNome').value.trim().replace(/;/g, ' '), v = $('fValor').value.trim();
  if (!n) { $('fErr').textContent = 'Informe o nome do produto.'; return }
  if (!/^\d+([.,]\d{1,2})?$/.test(v)) { $('fErr').textContent = 'Informe um valor em números, como 12,50.'; return }
  try { await dados.salvar(editCod, n, num(v).toFixed(2)) } catch (er) { $('fErr').textContent = er.message; return }
  $('dForm').close(); toast(editCod ? 'Produto alterado' : 'Produto cadastrado'); await recarregar()
};
$('delNo').onclick = () => $('dDel').close();
$('delYes').onclick = async () => {
  try { await dados.apagar(delCod) } catch (er) { toast(er.message); return }
  delete pedido[delCod]; $('dDel').close(); toast('Produto apagado'); await recarregar()
};

/* ---- operador ---- */
function renderMenu() {
  $('menu').innerHTML = prods.length ? prods.map(p => `<button class="item" data-c="${p.c}"><b>${esc(p.n)}</b><span>${p.c}<strong>${brl(num(p.v))}</strong></span></button>`).join('') : '<div class="empty">O cardápio está vazio. Cadastre produtos como Administrador.</div>'
}
$('menu').onclick = e => { const b = e.target.closest('.item'); if (b) add(+b.dataset.c) };
function add(c) { pedido[c] = (pedido[c] || 0) + 1; renderTicket() }
$('codeForm').onsubmit = e => {
  e.preventDefault(); const c = +$('codeIn').value.trim();
  if (prods.some(p => p.c === c)) { add(c); toast('Produto adicionado ao pedido') } else toast('Código inválido. Tente novamente.');
  $('codeIn').value = ''; $('codeIn').focus()
};
function renderTicket() {
  const ks = Object.keys(pedido).map(Number).filter(c => pedido[c] > 0 && prods.some(p => p.c === c));
  const hora = new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
  const t = $('ticket');
  if (!ks.length) { t.innerHTML = `<h3>Comanda</h3><div class="meta">${hora} · balcão</div><p style="color:#6b5e58">Toque em um produto para adicionar ao pedido.</p>`; return }
  let total = 0;
  const lines = ks.map(c => {
    const p = prods.find(x => x.c === c), q = pedido[c], s = num(p.v) * q; total += s;
    return `<div class="ln"><span class="q"><button data-m="${c}" aria-label="Remover um ${esc(p.n)}">−</button>${q}<button data-p="${c}" aria-label="Adicionar um ${esc(p.n)}">+</button></span><span>${esc(p.n)}</span><span>${brl(s)}</span></div>`
  }).join('');
  t.innerHTML = `<h3>Comanda</h3><div class="meta">${hora} · balcão</div>${lines}<div class="tot"><span>Total</span><span>${brl(total)}</span></div><button class="btn pri" id="fecha">Fechar pedido</button><button class="btn" id="limpa">Limpar</button>`
}
$('ticket').onclick = e => {
  const b = e.target.closest('button'); if (!b) return;
  if (b.dataset.p) add(+b.dataset.p);
  if (b.dataset.m) { const c = +b.dataset.m; pedido[c]--; if (pedido[c] <= 0) delete pedido[c]; renderTicket() }
  if (b.id === 'limpa') { pedido = {}; renderTicket() }
  if (b.id === 'fecha') {
    const t = $('ticket'); let total = 0;
    const li = Object.keys(pedido).map(Number).filter(c => pedido[c] > 0 && prods.some(p => p.c === c)).map(c => { const p = prods.find(x => x.c === c), s = num(p.v) * pedido[c]; total += s; return `<li>${pedido[c]}× ${esc(p.n)} (código ${p.c}) — ${brl(s)}</li>` }).join('');
    t.classList.add('tear'); setTimeout(() => { pedido = {}; t.classList.remove('tear'); t.innerHTML = `<h3>Pedidos do cliente</h3><div class="sum"><ul>${li}</ul><div class="tot"><span>Total</span><span>${brl(total)}</span></div></div><div class="thanks"><b>Obrigado pela preferência!</b></div><button class="btn pri" id="novoPed">Novo pedido</button>` }, 650)
  }
  if (b.id === 'novoPed') renderTicket()
};

/* ---- menu inicial: 1 Administrador, 2 Operador, 0 Sair ---- */
function tela(n) {
  ['Start', 'Adm', 'Op', 'Bye'].forEach(k => $('v' + k).hidden = k !== n); $('sair').hidden = !(n === 'Adm' || n === 'Op');
  if (n === 'Op') { const h = new Date().getHours(); $('saud').textContent = (h < 12 ? 'Bom dia' : h < 18 ? 'Boa tarde' : 'Boa noite') + ', caro cliente! O que deseja comprar?' }
}
function ir(g) { if (g === 'adm') { tela('Adm'); toast('Entrou como Administrador') } else if (g === 'op') { pedido = {}; tela('Op'); renderTicket(); toast('Entrou como Operador') } else tela('Bye') }
document.querySelector('.start').onclick = e => { const b = e.target.closest('[data-go]'); if (b) ir(b.dataset.go) };
$('sair').onclick = () => { const adm = !$('vAdm').hidden; tela('Start'); toast(adm ? 'Saindo do menu Administrador' : 'Saindo do menu Operador') };
$('volta').onclick = () => tela('Start');
document.addEventListener('keydown', e => { if ($('vStart').hidden || document.querySelector('dialog[open]') || e.ctrlKey || e.metaKey) return; const m = { '1': 'adm', '2': 'op', '0': 'sair' }[e.key]; if (m) ir(m) });
recarregar();