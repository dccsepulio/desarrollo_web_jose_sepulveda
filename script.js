/* script.js */

// Datos ficticios de comunas según región
const comunasPorRegion = {
    "Metropolitana": ["Santiago", "Ñuñoa", "Providencia", "La Florida", "Puente Alto"],
    "Valparaíso": ["Valparaíso", "Viña del Mar", "Quilpué"],
    "Biobío": ["Concepción", "Talcahuano", "Chillán"],
    "Araucania": ["Angol", "Temuco", "Pucón"]
  };
  
  // Cargar comunas al cambiar región
  function cargarComunas() {
    const region = document.getElementById("region").value;
    const comunaSelect = document.getElementById("comuna");
    comunaSelect.innerHTML = "<option value=''>Seleccione una comuna</option>";
    
    if (region && comunasPorRegion[region]) {
      comunasPorRegion[region].forEach((comuna) => {
        const option = document.createElement("option");
        option.value = comuna;
        option.textContent = comuna;
        comunaSelect.appendChild(option);
      });
    }
  }
  
  // Mostrar input de contacto asociado
  function mostrarInputContacto(select) {
    const input = select.nextElementSibling;
    if (select.value !== "") {
      input.style.display = "inline-block";
    } else {
      input.style.display = "none";
      input.value = "";
    }
  }

  // Agregar otro bloque de contacto
  function agregarOtroContacto() {
    const container = document.getElementById("contactosContainer");
    const numContactos = container.querySelectorAll(".contacto").length;
    if (numContactos >= 5) {
      alert("No puede ingresar más de 5 contactos de forma simultanea.");
      return;
    }

    const nuevo = container.firstElementChild.cloneNode(true);
    nuevo.querySelector('select').value = "";
    const input = nuevo.querySelector('input');
    input.value = "";
    input.style.display = "none";
    container.appendChild(nuevo);
  }
  
  // Mostrar/ocultar campo "otro tema"
  function mostrarOtroTema() {
    const tema = document.getElementById("tema").value;
    const campoOtroTema = document.getElementById("campoOtroTema");
  
    if (tema === "otro") {
      campoOtroTema.style.display = "block";
    } else {
      campoOtroTema.style.display = "none";
    }
  }
  
  // Validar cantidad máxima de fotos
  function validarFotos() {
    const contenedorFotos = document.getElementById("contenedorFotos");
    const totalInputs = document.querySelectorAll("input[type='file']").length;
    
    if (totalInputs > 5) {
      alert("No se pueden agregar más de 5 fotos.");
      // Eliminar el último input agregado
      contenedorFotos.removeChild(contenedorFotos.lastChild);
    }
  }
  
  // Agregar otro input de tipo "file"
  function agregarOtraFoto() {
    const contenedorFotos = document.getElementById("contenedorFotos");
    const nuevoInput = document.createElement("input");
    nuevoInput.type = "file";
    nuevoInput.name = "fotoActividad";
    nuevoInput.accept = "image/*";
    nuevoInput.onchange = validarFotos;
    
    contenedorFotos.appendChild(nuevoInput);
    validarFotos();
  }
  
  // Validaciones del formulario
  function validarFormulario(event) {
    event.preventDefault(); // Evita el envío automático del formulario
    
    // Obtener valores
    const region = document.getElementById("region").value.trim();
    const comuna = document.getElementById("comuna").value.trim();
    const nombreOrganizador = document.getElementById("nombreOrganizador").value.trim();
    const emailOrganizador = document.getElementById("emailOrganizador").value.trim();
    const celularOrganizador = document.getElementById("celularOrganizador").value.trim();
    const contactarPor = document.getElementById("contactarPor").value.trim();
    const idContacto = document.getElementById("idContacto").value.trim();
    const inicio = document.getElementById("inicio").value.trim();
    const termino = document.getElementById("termino").value.trim();
    const tema = document.getElementById("tema").value.trim();
    const otroTemaTxt = document.getElementById("otroTemaTxt").value.trim();
  
    // Validar campos obligatorios
    if (!region) {
      alert("Debe seleccionar una región.");
      return false;
    }
  
    if (!comuna) {
      alert("Debe seleccionar una comuna.");
      return false;
    }
  
    if (!nombreOrganizador) {
      alert("El nombre del organizador es obligatorio.");
      return false;
    }
    if (nombreOrganizador.length > 200) {
      alert("El nombre del organizador no puede superar 200 caracteres.");
      return false;
    }
  
    if (!emailOrganizador) {
      alert("El email es obligatorio.");
      return false;
    }
    // Validar formato de email básico
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(emailOrganizador)) {
      alert("Formato de email no válido.");
      return false;
    }
    if (emailOrganizador.length > 100) {
      alert("El email no puede superar 100 caracteres.");
      return false;
    }
  
    // Validar celular (opcional, pero si existe debe cumplir formato)
    if (celularOrganizador) {
      const celularRegex = /^\+\d{1,3}\.\d{7,10}$/; 
      if (!celularRegex.test(celularOrganizador)) {
        alert("El formato del celular debe ser +NNN.NNNNNNNN (N=0-9).");
        return false;
      }
    }
  
    // Validar múltiples contactos (opcional, máx 5)
    const contactos = document.querySelectorAll("#contactosContainer .contacto");
    if (contactos.length > 5) {
      alert("No puede ingresar más de 5 contactos de forma simultanea.");
      return false;
    }
    for (const contacto of contactos) {
      const tipo = contacto.querySelector("select").value;
      const id = contacto.querySelector("input").value.trim();

      if (tipo && (id.length < 4 || id.length > 50)) {
        alert("El ID/URL de contacto debe tener entre 4 y 50 caracteres.");
        return false;
      }
    }
  
    // Validar inicio (obligatorio)
    if (!inicio) {
      alert("Debe ingresar fecha y hora de inicio.");
      return false;
    }
 
    if (termino) {
      if (termino <= inicio) {
        alert("La fecha/hora de término debe ser mayor a la de inicio.");
        return false;
      }
    }
  
    // Validar tema
    if (!tema) {
      alert("Debe seleccionar un tema.");
      return false;
    }
    if (tema === "otro") {
      if (otroTemaTxt.length < 3 || otroTemaTxt.length > 15) {
        alert("La descripción del tema (otro) debe tener entre 3 y 15 caracteres.");
        return false;
      }
    }
  
    // Validar fotos
    const inputsFile = document.querySelectorAll("input[type='file']");
    if (inputsFile.length === 0) {
      alert("Debe agregar al menos 1 foto.");
      return false;
    }
    // Cada input debe tener al menos un archivo seleccionado
    let fotosSeleccionadas = 0;
    inputsFile.forEach((input) => {
      if (input.files.length > 0) {
        fotosSeleccionadas += input.files.length;
      }
    });
    if (fotosSeleccionadas === 0) {
      alert("Debe seleccionar al menos 1 foto.");
      return false;
    }
    if (fotosSeleccionadas > 5) {
      alert("No puede agregar más de 5 fotos en total.");
      return false;
    }
  
    // Confirmación
    const respuesta = confirm("¿Está seguro que desea agregar esta actividad?");
    if (respuesta) {
      alert("Hemos recibido su información, muchas gracias y suerte en su actividad.");
      // Redirigir a portada o mostrar mensaje final
      window.location.href = "index.html";
    } else {
      alert("Envio cancelado.");
      // Cancelar envío, quedarse en el formulario
      return false;
    }
  }
  
  // Mostrar foto en grande
  function mostrarFotoGrande(src) {
    const overlay = document.getElementById("overlayFoto");
    const overlayContent = document.getElementById("overlayContent");
  
    const oldImg = overlayContent.querySelector("img");
    if (oldImg) {
      overlayContent.removeChild(oldImg);
    }
  
    const nuevaImg = document.createElement("img");
    nuevaImg.width = 800;
    nuevaImg.height = 600;
    nuevaImg.alt = "Foto ampliada";
    nuevaImg.src = src;
  
    overlayContent.insertBefore(nuevaImg, overlayContent.firstChild);
  
    overlay.style.display = "block";
  }
  
  
  function cerrarFotoGrande() {
    const overlay = document.getElementById("overlayFoto");
    overlay.style.display = "none";
  }
  