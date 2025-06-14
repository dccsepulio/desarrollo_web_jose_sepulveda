(() => {
  const tag   = document.getElementById('comentarios-script');
  if (!tag) return;

  const actividadId     = tag.dataset.actividad;
  const ul              = document.getElementById('listaComentarios');
  const form            = document.getElementById('formComentario');

  const sanitize = s => {
    const div = document.createElement('div');
    div.innerText = s;
    return div.innerHTML;
  };

  /* ---- leer y dibujar ---- */
  function cargar() {
    fetch(`/api/actividad/${actividadId}/comentarios`)
      .then(r => r.json())
      .then(lista => {
        ul.innerHTML = '';
        if (lista.length === 0) {
          ul.innerHTML = '<li>Sin comentarios</li>';
          return;
        }
        for (const c of lista) {
          const li = document.createElement('li');
          li.innerHTML = `<strong>${sanitize(c.nombre)}</strong>
                          (${c.fecha}): ${sanitize(c.texto)}`;
          ul.appendChild(li);
        }
      });
  }
  cargar();

  /* ---- alta vía AJAX ---- */
  form.addEventListener('submit', evt => {
    evt.preventDefault();
    const data = new FormData(form);      // incluye csrf_token
    fetch(`/api/actividad/${actividadId}/comentarios`, {
      method: 'POST', body: data
    })
    .then(r => r.ok ? r.json() : r.json().then(e => Promise.reject(e)))
    .then(() => { form.reset(); cargar(); })
    .catch(e => alert(e.errors ? JSON.stringify(e.errors) : 'Error al guardar'));
  });
})();