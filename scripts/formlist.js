async function searchForm() {
  const searchDocumentNumber = document.getElementById('search-document-number').value.trim();
  const formTableBody = document.getElementById('form-table-body');
  formTableBody.innerHTML = "";  // Clear previous results

   let searchResult = await searchForms(searchDocumentNumber || null);

    if (searchResult) {
        let forms;
        if (searchDocumentNumber){
           forms = searchResult.clientes || [];
        }else {
            formTableBody.innerHTML = '<tr><td colspan="3">No se encontraron formularios.</td></tr>';
              return;
        }
       if (forms.length === 0 ) {
           formTableBody.innerHTML = '<tr><td colspan="3">No se encontraron formularios.</td></tr>';
              return;
          }
      forms.forEach(form => {
          const row = formTableBody.insertRow();
          row.insertCell().textContent = form.id_formulario;
          row.insertCell().textContent = form.nombre_completo;

            const actionsCell = row.insertCell();

             const viewButton = document.createElement('button');
              viewButton.textContent = 'Ver detalles';
              viewButton.className = 'form-detail-button';
              viewButton.onclick = () => handleViewFormDetails(form.id_formulario);
              actionsCell.appendChild(viewButton);


             const deleteButton = document.createElement('button');
              deleteButton.textContent = 'Borrar';
              deleteButton.className = 'form-delete-button';
              deleteButton.onclick = () => handleDeleteForm(form.id_formulario);
             actionsCell.appendChild(deleteButton);
      });
   } else {
     formTableBody.innerHTML = '<tr><td colspan="3">Error al cargar formularios.</td></tr>';
   }
}

async function handleViewFormDetails(id_formulario) {
  try {
      const response = await fetch(`${API_BASE_URL}/clientes/${id_formulario}`, {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json',
          },
      });

      if (!response.ok) {
          const message = await response.json();
          throw new Error(`Error retrieving form details, status: ${response.status}, message: ${message.message}`);
      }

      const searchResult = await response.json();

      if (searchResult && searchResult.cliente) {
          const form = searchResult.cliente;
          const referidos = form.referidos || [];

          const formDetails = `
              <h2>Detalles del Formulario ${form.id_formulario}</h2>
              <p><strong>Nombre Cliente:</strong> ${form.nombre_completo}</p>
              <p><strong>Número de documento:</strong> ${form.numero_documento}</p>
              <p><strong>Departamento:</strong> ${form.departamento_id}</p>
              <p><strong>Ciudad:</strong> ${form.ciudad_id}</p>
              <p><strong>Teléfono:</strong> ${form.telefono}</p>
              <p><strong>Promotor:</strong> ${form.promotor}</p>
              <h3>Referidos:</h3>
              ${referidos.map(referido => `
                  <div class="referido">
                      <p><strong>Nombre:</strong> ${referido.nombre}</p>
                      <p><strong>Teléfono:</strong> ${referido.telefono}</p>
                      <p><strong>Departamento:</strong> ${referido.departamento_id}</p>
                      <p><strong>Ciudad:</strong> ${referido.ciudad_id}</p>
                      <p><strong>Relación con el cliente:</strong> ${referido.relacion_cliente}</p>
                  </div>
              `).join('')}
          `;

          // Crear modal para mostrar los detalles
          const modal = document.createElement('div');
          modal.style.cssText = `
              position: fixed;
              top: 50%;
              left: 50%;
              transform: translate(-50%, -50%);
              background: white;
              padding: 20px;
              border: 1px solid #ddd;
              box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
              z-index: 1000;
              max-height: 80vh;
              overflow-y: auto;
              width: 80%;
              max-width: 700px;
          `;
          modal.innerHTML = formDetails;

          // Botón para cerrar el modal
          const closeButton = document.createElement('button');
          closeButton.textContent = 'Cerrar';
          closeButton.onclick = () => modal.remove();
          modal.appendChild(closeButton);

          document.body.appendChild(modal);
      } else {
          alert('Error obteniendo el detalle del formulario');
      }
  } catch (error) {
      console.error('Error en la consulta del formulario:', error);
      alert('Hubo un error al obtener los detalles del formulario.');
  }
}


async function handleDeleteForm(id_formulario) {
  if (confirm('¿Está seguro de que desea borrar este formulario?')) {
   const deleteResult = await deleteForm(id_formulario);
     if (deleteResult){
          alert('Formulario borrado correctamente')
           searchForm(); // Refresh the list after delete
     }else{
       alert('Error al borrar el formulario')
    }
  }
}