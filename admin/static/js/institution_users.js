
const input = document.getElementById("username")
const role = document.getElementById("role")
const addUserForm = document.getElementById("addUserForm")

let selectedListItem = null;

async function loadUserList(id) {
    let url = '/institutions/' + id + '/users-not-in'
    try {
      // Realizar una solicitud GET al servidor para obtener la lista de usuarios
      const response = await fetch(url);

      // Verificar si la respuesta del servidor es exitosa (código de respuesta 200)
      if (!response.ok) {
        throw new Error('La solicitud no fue exitosa');
      }

      // Convertir la respuesta a JSON
      const data = await response.json();
      const userList = data.users;

      // Actualizar la lista en el DOM
      const userListContainer = document.getElementById("users-not-in-list"); // Agrega una clase a tu contenedor de lista
      userListContainer.innerHTML = ''; // Limpiar la lista existente

      // Recorrer la lista de usuarios y agregar elementos a la lista en el DOM
      userList.forEach(function (user) {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
          <div id=li-${user.username} class="flex items-center rounded p-3 space-x-4 my-2 hover:bg-indigo-400">
            <div class="flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                </svg>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate dark:text-white">
                ${user.username}
              </p>
              <p class="text-sm text-gray-500 truncate dark:text-gray-400">
                ${user.email}
              </p>
            </div>
          </div>
        `;
        listItem.addEventListener('click', function () {
            const selectedUser = user.username; 
            const newListItem = document.getElementById('li-' + selectedUser);
            
            document.getElementById('username').value = selectedUser;

            if (selectedListItem) {
              selectedListItem.classList.remove('bg-indigo-300');
            }
      
            // Agrega la clase bg-indigo-700 al nuevo elemento seleccionado
            newListItem.classList.add('bg-indigo-300');

            // Actualiza la variable global al nuevo elemento seleccionado
            selectedListItem = newListItem;

            
          });

        userListContainer.appendChild(listItem);
      });
    } catch (error) {
      // Manejar errores si la solicitud falla
      console.error('Error al cargar la lista de usuarios:', error);
    }
  }


 // addUserForm.addEventListener('submit', async function(event) {
//     event.preventDefault();
//     var id = this.getAttribute('data-id');
//     var url=`/institutions/${id}/add-user`;


//     const data = {
//         username: input.value,
//         role: role.value,
//       };


//     try {
//       const response = await fetch(url, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json', // Ajusta el tipo de contenido según tu API
//         },
//         body: JSON.stringify(data), // Convierte los datos a JSON antes de enviarlos
//       });
  
//       if (!response.ok) {
//         throw new Error(`Error en la solicitud: ${response.status}`);
//       }
  
//       // Si la solicitud fue exitosa, puedes manejar la respuesta aquí
//       const responseData = await response.json();
//       console.log('Respuesta del servidor:', responseData);

//     } catch (error) {
//       console.error('Error al enviar datos al servidor:', error);
//     }
// });