const formNumberDisplay = document.getElementById('form-number-display');
let formNumber = null; // Store the form number here
let departamentos = [];
let ciudades = {};
let referidoId = 0;

 async function initializeFormPage(){
     formNumber = await fetchFormNumber();
      if (formNumber) {
            formNumberDisplay.textContent = `Formulario No. ${formNumber}`;
        } else {
             formNumberDisplay.textContent = 'Error al cargar el número de formulario';
        }

        const masterData = await fetchMasterData();

          if (masterData) {
              departamentos = masterData.departamentos;
             ciudades = masterData.ciudades;


              populateDepartmentDropdown('departamento', departamentos);
             //Initial setup of referred departments.
             const referedDepartments = document.querySelectorAll('[id^="departamento-referido-"]');
             referedDepartments.forEach(dropdown => {
                  populateDepartmentDropdown(dropdown.id, departamentos);
             });
          }
 }

function populateDepartmentDropdown(dropdownId, departamentos) {
       const dropdown = document.getElementById(dropdownId);
       dropdown.innerHTML = '<option value="">Seleccionar departamento</option>'; // Default option
         departamentos.forEach(dept => {
            const option = document.createElement('option');
             option.value = dept.id;
             option.textContent = dept.nombre;
             dropdown.appendChild(option);
         });
     }

     function populateCityDropdown(dropdownId, departmentId, cities) {
          const dropdown = document.getElementById(dropdownId);
          dropdown.innerHTML = '<option value="">Seleccionar municipio</option>';
         if (!departmentId || !cities[departmentId]) {
             return;
         }
         cities[departmentId].forEach(city => {
             const option = document.createElement('option');
             option.value = city.id;
             option.textContent = city.nombre;
             dropdown.appendChild(option);
         });
     }
      // Event listeners for department dropdowns
     document.getElementById('departamento').addEventListener('change', function() {
         populateCityDropdown('ciudad', this.value, ciudades);
     });


     function addReferido() {
         referidoId++;
         const referidosContainer = document.getElementById('referidos-container');

         const referidoDiv = document.createElement('div');
         referidoDiv.className = 'referido';
         referidoDiv.id = `referido-${referidoId}`;
         referidoDiv.innerHTML = `
             <div class="form-row">
                 <label for="nombre-referido-${referidoId}">Nombre</label>
                 <input type="text" id="nombre-referido-${referidoId}" name="nombre-referido[]">
             </div>
             <div class="form-row">
                 <label for="direccion-referido-${referidoId}">Dirección</label>
                 <input type="text" id="direccion-referido-${referidoId}" name="direccion-referido[]">
             </div>
             <div class="form-row">
                 <label for="telefono-referido-${referidoId}">Teléfono</label>
                 <input type="text" id="telefono-referido-${referidoId}" name="telefono-referido[]">
             </div>
             <div class="form-row">
                 <label for="departamento-referido-${referidoId}">Departamento</label>
                 <select id="departamento-referido-${referidoId}" name="departamento-referido[]"></select>
                 <label for="ciudad-referido-${referidoId}" style="width: auto;">Municipio / Ciudad</label>
                 <select id="ciudad-referido-${referidoId}" name="ciudad-referido[]"></select>
             </div>
             <div class="form-row">
                 <label for="relacion-cliente-${referidoId}">Relación con el cliente</label>
                 <select id="relacion-cliente-${referidoId}" name="relacion-cliente[]">
                     <option value="padre-madre">Padre/madre</option>
                     <option value="hermano">Hermano(a)</option>
                     <option value="hijo">Hijo(a)</option>
                     <option value="tio">Tío(a)</option>
                     <option value="primo">Primo(a)</option>
                     <option value="cunado">Cuñado(a)</option>
                     <option value="suegro">Suegro(a)</option>
                     <option value="ahijado">Ahijado(a)</option>
                     <option value="amigo-infancia">Amigo(a) de la infancia</option>
                     <option value="amigo-colegio">Amigo(a) del colegio</option>
                     <option value="amigo-trabajo">Amigo(a) del trabajo</option>
                     <option value="amigo-universidad">Amigo(a) de la universidad</option>
                     <option value="amigo-iglesia">Amigo(a) de la iglesia</option>
                     <option value="vecino">Vecino(a)</option>
                     <option value="padres-amigos-hijos">Padre/madre de amigos de sus hijos</option>
                     <option value="padrino-madrina">Padrino/madrina</option>
                 </select>
             </div>
             <div class="form-row">
                 <label for="credito-${referidoId}">Crédito</label>
                 <input type="radio" id="credito-si-${referidoId}" name="credito-${referidoId}" value="si">
                 <label for="credito-si-${referidoId}">Sí</label>
                 <input type="radio" id="credito-no-${referidoId}" name="credito-${referidoId}" value="no">
                 <label for="credito-no-${referidoId}">No</label>
             </div>
             <div class="form-row">
                 <label for="informacion-personal-${referidoId}">Información personal</label>
                 <input type="text" id="informacion-personal-${referidoId}" name="informacion-personal[]">
             </div>
             <div class="form-row">
                 <label>Trabajo</label>
                 <input type="radio" id="trabajo-dia-${referidoId}" name="trabajo-${referidoId}" value="dia">
                 <label for="trabajo-dia-${referidoId}">Día</label>
                 <input type="radio" id="trabajo-noche-${referidoId}" name="trabajo-${referidoId}" value="noche">
                 <label for="trabajo-noche-${referidoId}">Noche</label>
             </div>
             <div class="form-row">
                 <label>Vivienda</label>
                 <input type="radio" id="vivienda-dueno-${referidoId}" name="vivienda-${referidoId}" value="dueno">
                 <label for="vivienda-dueno-${referidoId}">Dueño</label>
                 <input type="radio" id="vivienda-renta-${referidoId}" name="vivienda-${referidoId}" value="renta">
                 <label for="vivienda-renta-${referidoId}">Renta</label>
             </div>
             <div class="form-row">
                 <label>Conoce Royal Prestige</label>
                 <input type="radio" id="conoce-si-${referidoId}" name="conoce-${referidoId}" value="si">
                 <label for="conoce-si-${referidoId}">Sí</label>
                 <input type="radio" id="conoce-no-${referidoId}" name="conoce-${referidoId}" value="no">
                 <label for="conoce-no-${referidoId}">No</label>
             </div>
             <div class="actions">
                 <button type="button" onclick="saveReferido(${referidoId})">Guardar</button>
                 <button type="button" onclick="editReferido(${referidoId})">Editar</button>
                 <button type="button" onclick="deleteReferido(${referidoId})">Borrar</button>
             </div>
         `;

         referidosContainer.appendChild(referidoDiv);

         const dropdown = document.getElementById(`departamento-referido-${referidoId}`);
         populateDepartmentDropdown(dropdown.id, departamentos);

         dropdown.addEventListener('change', function() {
             populateCityDropdown(`ciudad-referido-${referidoId}`, this.value, ciudades);
         });
     }


     function saveReferido(id) {
         const referidoDiv = document.getElementById(`referido-${id}`);
         const inputs = referidoDiv.querySelectorAll('input, select');
         inputs.forEach(input => input.disabled = true);
     }

     function editReferido(id) {
         const referidoDiv = document.getElementById(`referido-${id}`);
         const inputs = referidoDiv.querySelectorAll('input, select');
         inputs.forEach(input => input.disabled = false);
     }

     function deleteReferido(id) {
         const referidoDiv = document.getElementById(`referido-${id}`);
         referidoDiv.remove();
     }

     async function submitForm() {
         const formData = new FormData(document.getElementById('main-form'));
         const clienteData = {};
         // Extract Client Data
         clienteData.numero_documento = formData.get('numero-documento');
         clienteData.tipo_documento = formData.get('tipo-documento');
         clienteData.nombre_completo = formData.get('nombre-cliente');
         clienteData.departamento_id = parseInt(formData.get('departamento'));
         clienteData.ciudad_id = parseInt(formData.get('ciudad'));
         clienteData.direccion = formData.get('direccion');
         clienteData.telefono = formData.get('telefono');
         clienteData.horario = formData.get('horario');
         clienteData.nombre_distribuidor = formData.get('nombre-distribuidor');
         clienteData.telefono_distribuidor = formData.get('telefono-distribuidor');
         clienteData.promotor = formData.get('promotor');
         clienteData.telefono_promotor = formData.get('telefono-promotor');
          clienteData.fecha_inicio = formData.get('fecha-inicio');
           clienteData.fecha_vencimiento = formData.get('fecha-vencimiento');

           clienteData.id_formulario = formNumber; // Add the form number
         // Extract Referidos Data
         const referidos = [];
         const numReferidos = document.querySelectorAll('.referido').length;

         for (let i = 1; i <= numReferidos; i++) {
             const nombre = document.getElementById(`nombre-referido-${i}`).value;
             const direccion = document.getElementById(`direccion-referido-${i}`).value;
             const telefono = document.getElementById(`telefono-referido-${i}`).value;
             const departamento_id = parseInt(document.getElementById(`departamento-referido-${i}`).value);
             const ciudad_id = parseInt(document.getElementById(`ciudad-referido-${i}`).value);
             const relacion_cliente = document.getElementById(`relacion-cliente-${i}`).value;
              const credito = document.querySelector(`input[name="credito-${i}"]:checked`) ? document.querySelector(`input[name="credito-${i}"]:checked`).value: '';
             const informacion_personal = document.getElementById(`informacion-personal-${i}`).value;
             const trabajo = document.querySelector(`input[name="trabajo-${i}"]:checked`) ? document.querySelector(`input[name="trabajo-${i}"]:checked`).value: '';
             const vivienda = document.querySelector(`input[name="vivienda-${i}"]:checked`) ? document.querySelector(`input[name="vivienda-${i}"]:checked`).value: '';
             const conoce_royal = document.querySelector(`input[name="conoce-${i}"]:checked`) ? document.querySelector(`input[name="conoce-${i}"]:checked`).value: '';

             referidos.push({
                 nombre,
                 direccion,
                 telefono,
                 departamento_id,
                 ciudad_id,
                 relacion_cliente,
                 credito,
                 informacion_personal,
                 trabajo,
                 vivienda,
                 conoce_royal
             });
         }


            const clientResponseData = await submitFormData(clienteData)
              if (clientResponseData) {
                  for (const ref of referidos) {
                       ref.cliente_id = clientResponseData.id_formulario;
                  }

                   const submitReferredResult = await submitReferedData(referidos);

                    if (submitReferredResult){
                        alert('Formulario enviado con éxito!');
                     }else{
                        alert('Error al enviar referidos')
                     }
                 }else{
                   alert('Error al crear el cliente')
                 }
     }

initializeFormPage();