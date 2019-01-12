locationObject = {}

baseUrl = 'http:127.0.0.1:5000/api/v2/'

function locationSearch() {
    input = document.getElementsByName('location')[0]
    options = {
        componentRestrictions: {country: 'ke'}
    }

    autocomplete = new google.maps.places.Autocomplete(input, options);
    
    var autocomplete = new google.maps.places.Autocomplete(input, options);
    google.maps.event.addListener(autocomplete, 'place_changed', function(){
        place = autocomplete.getPlace();
        locationObject.lat = place.geometry.location.lat()
        locationObject.lng = place.geometry.location.lng()
        locationObject.city = place.formatted_address

        console.log(locationObject)
    })
}

/**
 * 
 * @param {*} table 
 * @param {*} columns 
 * @param {*} collection 
 * 
 */
function renderTableContent(table, columns, collection) {
    table = document.getElementById(table)
    counter = 1
    for(item of collection) {
        
        row = table.tBodies[0].insertRow(-1)
        row.classList.add("font-monseratt", "fs-sm", "grey-light")

        columns.map(i => {
            tCell = row.insertCell(-1)

            tCell.innerHTML = item[i]

            if (i == 'id') {
                tCell.innerHTML = counter
                counter++
            }

            if (i == 'location') {
                tCell.innerHTML = item[i].city
            }
        })

        tControls = row.insertCell(-1)
        tControls.innerHTML = `<div class="flex">
            <span class="px-sm">
                <a class="pointer" onclick="viewRecord(${item.id})"><i class="fas fa-eye"></i></a>
            </span>
            <span class="px-sm">
                <a class="pointer" onclick="editRecord(${item.id})"><i class="fas fa-edit"></i></a>
            </span>
            <span class="px-sm">
                <a class="pointer" onclick="deleteRecord(${item.id})"><i class="fas fa-trash"></i></a>
            </span>
            </div>` 
    }
} 

function authUser() {
    return JSON.parse(localStorage.getItem('auth_user'))
}

function userProfile() {
    get(baseUrl + 'auth/user/profile')
    .then(response => response.json())
    .then(data => {
        console.log(data)
        localStorage.setItem('auth_user', JSON.stringify(data))
        document.getElementById('name').innerHTML = data.firstname + ' ' + data.lastname
        document.getElementById('email').innerHTML = data.email
        document.getElementById('user_role').innerHTML = data.isAdmin? 'Admin' : 'User'
    })
    .catch(errors => {
        console.log(errors)
    })
}

function viewRecord(id) {
    console.log("view record", id)

    get(baseUrl + `incidents/${id}`)
    .then(response => response.json())
    .then(data => {
        console.log(data.data)
        localStorage.setItem('current_incident', JSON.stringify(data.data))
        window.location = 'view_record.html'
    })
}

function editRecord(id) {
    console.log("edit record", id)

    get(baseUrl + `incidents/${id}`)
    .then(response => response.json())
    .then(data => {
        localStorage.setItem('current_incident', JSON.stringify(data.data))
        window.location = 'edit_record.html'
    })
}

function deleteRecord(id) {
    console.log("delete record", id)

    deleteData(baseUrl + `incidents/${id}`)
    .then(response => response.json())
    .then(data => {
        window.location = 'dashboard.html'
    }).catch(error => {
        console.log(error)
    })
}

function getHeaders() {
    return {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
    }
}

async function get(url) {
    const response = await fetch(url, {
        method: 'get',
        headers:getHeaders()
    });

    if (!response.ok) {
        throw Error(response.statusText);
    }
    return response;
}


async function deleteData(url) {
    const response = await fetch(url, {
        method: 'delete',
        headers:getHeaders()
    });

    if (!response.ok) {
        throw Error(response.statusText);
    }
    return response;
}

async function postData(url, data) {
    const response = await fetch(url, {
        method: 'post',
        body: JSON.stringify(data),
        headers: getHeaders()
    });
    if (!response.ok) {
        throw Error(response.statusText);
    }
    return response;
}


async function patch(url, data) {
    const response = await fetch(url, {
        method: 'patch',
        body: JSON.stringify(data),
        headers: getHeaders()
    });
    if (!response.ok) {
        throw Error(response.statusText);
    }
    return response;
}


