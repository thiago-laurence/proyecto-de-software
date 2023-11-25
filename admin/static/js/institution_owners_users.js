let selectedListItem = null;

const searchInput = document.getElementById('duenio')
searchInput.addEventListener('keyup', () => {
  loadUserList(searchInput.value)
})

async function loadUserList(query) {
    let url = '/users/all-users/' + `?q=${query}`;
    
    if (query == ''){
        const container = document.getElementById("container-list");
        const userListContainer = document.getElementById("list-users");
        container.classList.add('hidden')    
        while (userListContainer.firstChild) {
            userListContainer.removeChild(userListContainer.firstChild);
        }
    }else{
        try{
            const response = await fetch(url);

            if (!response.ok) {
                throw new Error('La solicitud no fue exitosa');
            }

            const userList = await response.json();
            const container = document.getElementById("container-list");
            container.classList.remove('hidden')

            const userListContainer = document.getElementById("list-users");
            userListContainer.innerHTML = '';

            if (userList.length > 0){
                userList.forEach(function (user) {
                    const optionItem = document.createElement('li');
                    optionItem.setAttribute('value', user);
                    optionItem.innerHTML = `
                        <div id=user-${user} class="pl-8 pr-2 py-2 my-1 border-2 rounded-lg border-indigo-300 relative cursor-pointer bg-indigo-100 hover:bg-indigo-400 hover:text-gray-900">
                            <svg class="absolute w-4 h-4 left-2 top-3 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>
                            </svg>
                            ${user}
                        </div>`;
                    optionItem.addEventListener('click', function () {
                        const selectedUser = user; 
                        const newListItem = document.getElementById('user-' + selectedUser);
                        
                        document.getElementById('duenio').value = selectedUser;
            
                        if (selectedListItem) {
                            selectedListItem.classList.remove('bg-indigo-400');
                            newListItem.classList.remove('text-gray-900');
                        }
                    
                        newListItem.classList.add('bg-indigo-400');
                        newListItem.classList.add('text-gray-900');
            
                        selectedListItem = newListItem;    
                    });
                    userListContainer.appendChild(optionItem);
                });
            }else{
                while (userListContainer.firstChild) {
                    userListContainer.removeChild(userListContainer.firstChild);
                }
                const optionItem = document.createElement('li');
                optionItem.setAttribute('value', '');
                optionItem.innerHTML = `
                    <div class="pl-8 pr-2 py-2 border-2 rounded-lg border-indigo-500 relative cursor-pointer bg-red-100 text-gray-900">
                        <b>No existen usuarios coincidentes con la busqueda</b>
                    </div>`;
                userListContainer.appendChild(optionItem);
            }
        } catch (error) {
        console.error('Error al cargar la lista de usuarios:', error);
        }
    }
}