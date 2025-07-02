/* script.js */

(() => {
  document.addEventListener('DOMContentLoaded', () => {
    /* 1. Regiones → Comunas */
    const regionSel = document.getElementById('region');
    const comunaSel = document.getElementById('comuna');

    const cargarComunas = () => {
      const id = regionSel.value;
      comunaSel.innerHTML =
        id ? '<option value="">Cargando…</option>'
           : '<option value="">Seleccione una comuna</option>';

      if (!id) return;

      fetch(`/api/comunas?region_id=${id}`)
        .then(r => r.ok ? r.json() : [])
        .then(lista => {
          comunaSel.innerHTML =
            '<option value="">Seleccione una comuna</option>';
          lista.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c.id;
            opt.textContent = c.nombre;
            comunaSel.appendChild(opt);
          });
        })
        .catch(() => {
          comunaSel.innerHTML =
            '<option value="">Error al cargar comunas</option>';
        });
    };

    if (regionSel) {
      regionSel.addEventListener('change', cargarComunas);
      if (regionSel.value) cargarComunas();      // para recargas con datos
    }

    /* 2. Contactos dinámicos */
    const contactosDiv = document.getElementById('contactosContainer');

    document.getElementById('btnAddContacto')?.addEventListener('click', () => {
      if (!contactosDiv) return;
      const bloques = contactosDiv.querySelectorAll('.contacto');
      if (bloques.length >= 5) {
        alert('No puede ingresar más de 5 contactos.');
        return;
      }
      const nuevo = bloques[0].cloneNode(true);
      const sel   = nuevo.querySelector('select');
      const inp   = nuevo.querySelector('input');
      sel.value   = '';
      inp.value   = '';
      inp.style.display = 'none';
      contactosDiv.appendChild(nuevo);
    });

    contactosDiv?.addEventListener('change', e => {
      if (e.target.tagName === 'SELECT') mostrarInputContacto(e.target);
    });

    contactosDiv?.addEventListener('click', e => {
      if (e.target.classList.contains('rem')) {
        const blk = e.target.closest('.contacto');
        if (blk && contactosDiv.childElementCount > 1) blk.remove();
      }
    });

    /* 3. Tema “otro” */
    document.getElementById('temas')
      ?.addEventListener('change', () => {
        const sel     = document.getElementById('temas');
        const visible = Array.from(sel.selectedOptions)
                            .some(o => o.value === 'otro');
        document.getElementById('campoOtroTema').style.display =
            visible ? 'block' : 'none';
      });

    if (document.getElementById('temas')) {
      const ev = new Event('change');
      document.getElementById('temas').dispatchEvent(ev);
    }

    /* 4. Fotos (máx 5 inputs / archivos) */
    document.getElementById('fotoActividad')
      ?.addEventListener('change', validarFotos);

    document.getElementById('btnAddFoto')
      ?.addEventListener('click', agregarOtraFoto);

    document.addEventListener('DOMContentLoaded', function() {
      const btnAddFoto = document.getElementById('btnAddFoto');
      const uploadArea = document.getElementById('upload-area');
      const contenedorPrevisualizacion = document.getElementById('contenedorPrevisualizacion');
      let fileCount = 1;
      const maxFiles = 5;

      // Función para crear un nuevo campo de archivo
      function createFileInput() {
          if (fileCount >= maxFiles) {
              alert('Máximo ' + maxFiles + ' fotos permitidas');
              return;
          }

          const wrapper = document.createElement('div');
          wrapper.className = 'file-input-wrapper';
          
          const input = document.createElement('input');
          input.type = 'file';
          input.name = 'fotoActividad[]';
          input.className = 'foto-actividad';
          input.accept = 'image/*';
          
          const removeBtn = document.createElement('button');
          removeBtn.type = 'button';
          removeBtn.className = 'btn-remove-foto';
          removeBtn.innerHTML = '×';
          removeBtn.onclick = function() {
              wrapper.remove();
              fileCount--;
          };

          // Mostrar previsualización cuando se selecciona un archivo
          input.onchange = function(e) {
              if (this.files && this.files[0]) {
                  showPreview(this.files[0]);
              }
          };

          wrapper.appendChild(input);
          wrapper.appendChild(removeBtn);
          
          // Insertar el nuevo campo antes del botón "Agregar otra foto"
          uploadArea.insertBefore(wrapper, btnAddFoto.parentNode.insertBefore(wrapper, btnAddFoto));
          fileCount++;
      }

      // Función para mostrar previsualización de imágenes
      function showPreview(file) {
          const reader = new FileReader();
          reader.onload = function(e) {
              const img = document.createElement('img');
              img.src = e.target.result;
              img.className = 'preview-image';
              contenedorPrevisualizacion.appendChild(img);
          };
          reader.readAsDataURL(file);
      }

      // Configurar el primer campo de archivo
      document.querySelector('.foto-actividad').onchange = function(e) {
          if (this.files && this.files[0]) {
              showPreview(this.files[0]);
          }
      };

      // Evento para el botón "Agregar otra foto"
      btnAddFoto.onclick = createFileInput;
    });
    /* 5. Validación y confirmación de envío */
    const formActividad = document.getElementById('formActividad');   // ← ponle este id en la plantilla si aún no lo tiene
    formActividad?.addEventListener('submit', evt => {
      if (!validarFormulario()) { evt.preventDefault(); return; }
      if (!confirm('¿Está seguro que desea agregar esta actividad?')) {
        evt.preventDefault();
      }
    });
  });

  // Helpers UI

  function mostrarInputContacto(selectEl) {
    const input = selectEl.nextElementSibling;
    if (!input) return;
    if (selectEl.value) {
      input.style.display = 'inline-block';
    } else {
      input.value = '';
      input.style.display = 'none';
    }
  }

  function agregarOtraFoto() {
    const cont = document.getElementById('contenedorFotos');
    if (!cont) return;

    const totalInputs = cont.querySelectorAll("input[type='file'][name='fotos']").length + 1;
    if (totalInputs >= 5) {
      alert('No se pueden subir más de 5 fotos.');
      return;
    }
    const nuevo = document.createElement('input');
    nuevo.type  = 'file';
    nuevo.name  = 'fotos';
    nuevo.accept = 'image/*';
    nuevo.addEventListener('change', validarFotos);
    cont.appendChild(nuevo);
  }

  function validarFotos() {
    const fileInputs = document.querySelectorAll("input[type='file'][name='fotos']");
    let totalArchivos = 0;
    fileInputs.forEach(i => (totalArchivos += i.files.length));
    if (totalArchivos > 5) {
      alert('Máx 5 archivos en total.');
      this.value = '';
    }
  }

  // Validación global

  function validarFormulario() {
    const val = id => (document.getElementById(id)?.value || '').trim();

    // Region / Comuna
    if (document.getElementById('region') && !val('region')) { alert('Debe seleccionar una región.'); return false; }
    if (document.getElementById('comuna') && !val('comuna')) { alert('Debe seleccionar una comuna.'); return false; }

    // Organizador
    const nom = val('nombre');
    if (!nom) { alert('El nombre del organizador es obligatorio.'); return false; }
    if (nom.length > 200) { alert('Máx 200 caracteres en nombre.'); return false; }

    // Email
    const email = val('email');
    if (!email) { alert('El email es obligatorio.'); return false; }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      alert('Formato de email no válido.'); return false;
    }
    if (email.length > 100) { alert('Email demasiado largo.'); return false; }

    // Celular opcional
    const cel = val('celular');
    if (cel && !/^\+\d{1,3}\.\d{7,10}$/.test(cel)) {
      alert('Formato de celular inválido.'); return false;
    }

    // Contactos
    const bloques = document.querySelectorAll('#contactosContainer .contacto');
    if (bloques.length > 5) { alert('No más de 5 contactos.'); return false; }
    for (const b of bloques) {
      const tipo = b.querySelector('select')?.value;
      const idct = (b.querySelector('input')?.value || '').trim();
      if (tipo && (idct.length < 4 || idct.length > 50)) {
        alert('Cada ID/URL de contacto debe tener entre 4 y 50 caracteres.');
        return false;
      }
    }

    // Fechas
    const ini = val('inicio');
    if (!ini) { alert('Fecha/hora de inicio obligatoria.'); return false; }
    const fin = val('termino');
    if (fin && fin <= ini) {
      alert('La fecha/hora de término debe ser posterior al inicio.');
      return false;
    }

    // Temas
    const selTemas = document.getElementById('temas');
    const temasElegidos = Array.from(selTemas.selectedOptions)
                              .map(o => o.value);

    if (temasElegidos.length === 0) {
      alert('Debe seleccionar al menos un tema.');
      return false;
    }
    if (temasElegidos.includes('otro')) {
      const glosa = val('glosa_otro');
      if (glosa.length < 3 || glosa.length > 15) {
        alert('La glosa del tema «otro» debe tener 3–15 caracteres.');
        return false;
      }
    }

    // Fotos
    const fileInputs = document.querySelectorAll("input[type='file'][name='fotos']");
    let totalFotos = 0;
    fileInputs.forEach(i => (totalFotos += i.files.length));
    if (totalFotos < 1) { alert('Debe subir al menos 1 foto.'); return false; }
    if (totalFotos > 5) { alert('No puede subir más de 5 fotos.'); return false; }

    return true;
  }
})();