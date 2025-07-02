async function cargar() {
  const res = await fetch('/api/activities/finished');
  const data = await res.json();
  render(data);
}

async function evaluar(id, nota) {
  const res = await fetch(`/api/activities/${id}/notes`, {
    method : 'POST',
    headers: {'Content-Type': 'application/json'},
    body   : JSON.stringify({valor: nota})
  });
  if (!res.ok) return alert('Error: ' + res.status);
  const act = await res.json(); // respuesta con DTO actualizado
  const fila = document.querySelector(`tr[data-id="${id}"]`);
  fila.querySelector('.promedio').textContent = act.notaPromedio ?? '-';
}

function render(list) {
  const tbody = document.querySelector('#tabla tbody');
  tbody.innerHTML = '';
  list.forEach(a => {
    tbody.insertAdjacentHTML('beforeend', `
      <tr data-id="${a.id}">
        <td>${a.fechaInicio}</td>
        <td>${a.sector}</td>
        <td>${a.nombre}</td>
        <td>${a.tema}</td>
        <td class="promedio">${a.notaPromedio ?? '-'}</td>
        <td><button data-id="${a.id}">evaluar</button></td>
      </tr>`);
  });
}

document.addEventListener('click', async e => {
  if (e.target.matches('button[data-id]')) {
    const id   = e.target.dataset.id;
    const nota = Number(prompt('Ingresa nota 1-7'));
    if (!Number.isInteger(nota) || nota < 1 || nota > 7)
      return alert('Inválido');
    await evaluar(id, nota);
  }
});

cargar();
