document.addEventListener('DOMContentLoaded', () => {
  fetch('/api/estadisticas')
    .then(r => r.json())
    .then(d => dibujarGraficos(d))
    .catch(() => alert('No se pudo cargar estadisticas'));
});

const nz = x => Number(x) || 0;

function dibujarGraficos(data) {
  // 1. línea
  Highcharts.chart('grafLineas', {
    title: { text: 'Actividades por día' },
    xAxis: { categories: data.line.map(p => p.dia) },
    series: [{ name: 'Actividades', data: data.line.map(p => p.total) }]
  });

  // 2. torta
  Highcharts.chart('grafTorta', {
    chart: { type: 'pie' },
    title: { text: 'Actividades por tipo' },
    series: [{
      name: 'Total',
      data: data.pie.map(p => ({ name: p.tema, y: p.total }))
    }]
  });

  // 3. barras apiladas (mañana / mediodía / tarde)
  Highcharts.chart('grafBarras', {
    chart: { type: 'column' },
    title: { text: 'Actividades por horario y mes' },
    xAxis: { categories: data.bar.map(b => b.mes) },
    yAxis: { min: 0, title: { text: 'Cantidad' } },
    series: [
      { name: 'Mañana',   data: data.bar.map(b => nz(b.manana)) },
      { name: 'Mediodía', data: data.bar.map(b => nz(b.mediodia)) },
      { name: 'Tarde',    data: data.bar.map(b => nz(b.tarde)) }
    ]
  });
}