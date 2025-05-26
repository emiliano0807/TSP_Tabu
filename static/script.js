async function resolverRuta() {
  const res = await fetch('/resolver');
  const data = await res.json();

  const resultado = document.getElementById('resultado');
  resultado.innerHTML = `
    <h3>Ruta óptima:</h3>
    <p>${data.ruta.join(' → ')}</p>
    <p><strong>Distancia total:</strong> ${data.distancia} unidades</p>
  `;
}
