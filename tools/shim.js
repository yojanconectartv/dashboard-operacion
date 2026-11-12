/* Capa mínima que imita la API "dash" del dashboard para la versión web pública.
   Carga los datos de data/<id>.json y vuelve a dibujar cuando cambian los filtros. */
(function () {
  const IDS = ['resumen', 'tecnicos', 'carpetas', 'diario', 'supervisiones', 'sup_tipo', 'fact_tecnicos', 'fact_carpetas', 'carpeta_tecnicos', 'fact_carpeta_tecnicos', 'metas'];
  const store = {}; const calcs = {}; const subs = [];
  let params = {sup: 'Todos', mes: null};
  IDS.forEach((id) => { store[id] = {status: 'loading', data: []}; });
  let scheduled = false;
  function fire() {
    if (scheduled) return; scheduled = true;
    requestAnimationFrame(() => { scheduled = false; subs.forEach((fn) => { try { fn(); } catch (e) { console.error(e); } }); });
  }
  function calcResult(id) {
    const c = calcs[id];
    const ins = c.inputs.map((i) => api.data(i));
    if (ins.some((x) => x.status === 'error')) return {status: 'error', data: []};
    if (ins.some((x) => x.status !== 'ok')) return {status: 'loading', data: []};
    try { return {status: 'ok', data: c.fn(...ins.map((x) => x.data))}; } catch (e) { console.error(e); return {status: 'error', data: []}; }
  }
  const api = {
    data(id) {
      if (calcs[id]) return calcResult(id);
      const d = store[id];
      if (!d) return {status: 'missing', data: [], columns: [], meta: []};
      return {status: d.status, data: d.data, columns: d.data.length ? Object.keys(d.data[0]) : [], meta: [], refreshing: false};
    },
    onData(fn) { subs.push(fn); try { fn(); } catch (e) { console.error(e); } },
    calc(id, def) { calcs[id] = def; },
    loader() {},
    params() { return Object.assign({}, params); },
    setParams(p) { params = Object.assign({}, params, p); fire(); },
    resetParams() { params = {sup: 'Todos', mes: null}; fire(); },
    setLink() {},
    refresh() {},
    colors: ['#009ccc', '#003c64', '#5fc7e8', '#6b6b6b', '#2f8f75', '#eeb48c', '#7f77dd', '#aab4bb'],
  };
  window.dash = api;
  const v = (window.DASH_VERSION || Date.now());
  IDS.forEach((id) => {
    fetch('data/' + id + '.json?v=' + v).then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then((rows) => { store[id] = {status: 'ok', data: Array.isArray(rows) ? rows : []}; fire(); })
      .catch(() => { store[id] = {status: 'error', data: []}; fire(); });
  });
})();
