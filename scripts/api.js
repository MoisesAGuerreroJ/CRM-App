const API_BASE_URL = 'http://localhost:5000';

async function fetchFormNumber() {
  try {
       const response = await fetch(`${API_BASE_URL}/form_number`);
       if (!response.ok) {
         throw new Error(`HTTP error! Status: ${response.status}`);
     }
        const data = await response.json();
        return data.form_number;
   } catch (error) {
       console.error('Error fetching form number:', error);
        return null;
     }
   }


async function fetchMasterData() {
           try {
               const response = await fetch(`${API_BASE_URL}/departamentos`);
                if (!response.ok){
                     throw new Error(`HTTP error! Status: ${response.status}`);
                }
               const data = await response.json();
               const departamentos =  data.departamentos;

               const citiesResponse = await fetch(`${API_BASE_URL}/ciudades`);
                 if (!citiesResponse.ok){
                     throw new Error(`HTTP error! Status: ${citiesResponse.status}`);
                }
               const citiesData = await citiesResponse.json();
               const ciudades = citiesData.ciudades;

               return {departamentos, ciudades};

           } catch (error) {
               console.error('Error fetching master data:', error);
                return null;
           }
}
async function submitFormData(clienteData){
    try {
           const response = await fetch(`${API_BASE_URL}/clientes`, {
               method: 'POST',
               headers: {
                  'Content-Type': 'application/json',
               },
               body: JSON.stringify(clienteData),
              });

             if (!response.ok) {
                  const errorData = await response.json();
                  console.error('Error al crear el cliente:', errorData);
                  return null;
              }
              const clienteResponseData = await response.json();
              return clienteResponseData;
           } catch (error) {
               console.error('Error en el envío del formulario:', error);
                return null;
           }
}

async function submitReferedData(referidos) {
   try {
        for (const ref of referidos) {
                  const refResponse = await fetch(`${API_BASE_URL}/referidos`, {
                        method: 'POST',
                        headers: {
                           'Content-Type': 'application/json',
                        },
                      body: JSON.stringify(ref),
                    });
                     if (!refResponse.ok) {
                        const errorData = await refResponse.json();
                         console.error('Error adding referido:', errorData);
                          return null;
                     } else {
                        const refResponseData = await refResponse.json();
                         console.log("Referido agregado con exito:", refResponseData);
                       }
               }
              return true;
        }
          catch (error) {
                 console.error('Error en el envío del formulario:', error);
                  return null;
           }

}

async function searchForms(documentNumber = null) {
   try {
        let url = `${API_BASE_URL}/clientes`;
        if (documentNumber){
            url = `${API_BASE_URL}/clientes/documento/${documentNumber}`
        }

           const response = await fetch(url, {
               method: 'GET',
               headers: {
                   'Content-Type': 'application/json',
               },
           });

           if (!response.ok) {
               const message = await response.json();
               throw new Error (`Error retrieving forms, status: ${response.status}, message: ${message.message}`)

           }
           const data = await response.json();
           return data;
       } catch (error) {
           console.error('Error en la búsqueda de formularios:', error);
            return null;
       }

}
async function deleteForm(id_formulario) {
   try {
       const response = await fetch(`${API_BASE_URL}/clientes/${id_formulario}`, {
           method: 'DELETE',
           headers: {
               'Content-Type': 'application/json',
           },
       });
       if (!response.ok) {
            const message = await response.json();
            throw new Error(`Error deleting form, status: ${response.status}, message: ${message.message}`)
       }
       const data = await response.json();
       return data;
   } catch (error) {
       console.error('Error deleting form:', error);
      return null
   }
}