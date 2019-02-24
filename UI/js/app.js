
let locationObject = {}

let baseUrl = 'http://localhost:5000/api/v2/'

function locationSearch () {
  let input = document.getElementsByName('location')[0]
  let options = {
    componentRestrictions: { country: 'ke' }
  }

  let autocomplete = new google.maps.places.Autocomplete(input, options)
  google.maps.event.addListener(autocomplete, 'place_changed', function () {
    let place = autocomplete.getPlace()
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
function renderTableContent (table, columns, collection) {
  table = document.getElementById(table)
  let counter = 1
  for (var item of collection) {
    let row = table.tBodies[0].insertRow(-1)
    row.classList.add('font-monseratt', 'fs-sm', 'grey-light')

    columns.map(i => {
      let tCell = row.insertCell(-1)

      tCell.innerHTML = item[i]

      if (i === 'id') {
        tCell.innerHTML = counter
        counter++
      }

      if (i === 'location') {
        tCell.innerHTML = item[i].city
      }

      if (i === 'roles') {
        tCell.innerHTML = item.isAdmin ? 'Admin' : 'User'
      }
    })

    let tControls = row.insertCell(-1)
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

function redirectIfAuth () {
  if (authUser()) {
    window.location.href = 'dashboard.html'
  }
}

function checkAuth () {
  if (authUser()) return

  window.location.href = 'login.html'
}

function updateNavBar () {
  if (window.localStorage.getItem('auth_token')) {
    document.getElementById('signup').style = 'display: none;'
    var logoutNode = document.createElement('a')
    logoutNode.id = 'logout'
    logoutNode.classList.add('black', 'text-normal', 'border', 'signup-button', 'box-shadow', 'pointer')
    logoutNode.innerHTML = 'Log Out'
    logoutNode.onclick = () => {
      logout()
    }
    document.getElementById('nav_controls').appendChild(logoutNode)
  }
}

function authUser () {
  return JSON.parse(window.localStorage.getItem('auth_user'))
}

function logout () {
  postData(baseUrl + 'api/auth/logout', {})
  window.localStorage.clear()
  window.location = 'index.html'
}

function groupBy (collection, key) {
  return collection.reduce(function (accumulator, currentItem) {
    (accumulator[currentItem[key]] = accumulator[currentItem[key]] || []).push(currentItem)
    return accumulator
  }, {})
}

function statistics (collection = []) {
  var resultSet = {
    red_flag: {
      pending: 0,
      accepted: 0,
      rejected: 0,
      resolved: 0,
      under_investigation: 0
    },
    intervention: {
      pending: 0,
      accepted: 0,
      rejected: 0,
      resolved: 0,
      under_investigation: 0
    }
  }

  var groupedIncidents = groupBy(collection, 'incident_type')

  for (var incident in groupedIncidents) {
    if (groupedIncidents.hasOwnProperty(incident)) {
      var groupedStatuses = groupBy(groupedIncidents[incident], 'status')

      for (var status in groupedStatuses) {
        if (groupedStatuses.hasOwnProperty(status)) {
          resultSet[incident][status] = groupedStatuses[status].length
        }
      }
      console.log(groupedStatuses)
    }
  }

  // set red flag stats
  document.getElementById('pending_rf').innerHTML = resultSet.red_flag.pending
  document.getElementById('accepted_rf').innerHTML = resultSet.red_flag.resolved
  document.getElementById('rejected_rf').innerHTML = resultSet.red_flag.rejected
  document.getElementById('resolved_rf').innerHTML = resultSet.red_flag.resolved
  document.getElementById('under_investigation_rf').innerHTML = resultSet.red_flag.under_investigation

  // set intervention stats
  document.getElementById('pending_ir').innerHTML = resultSet.intervention.pending
  document.getElementById('accepted_ir').innerHTML = resultSet.intervention.resolved
  document.getElementById('rejected_ir').innerHTML = resultSet.intervention.rejected
  document.getElementById('resolved_ir').innerHTML = resultSet.intervention.resolved
  document.getElementById('under_investigation_ir').innerHTML = resultSet.intervention.under_investigation

  // document.getElementById('resolved_rf').innerHTML = resultSet.red_flag.resolved
  console.log(resultSet)
}

function loadUserProfile () {
  return get(baseUrl + 'auth/user/profile')
    .then(response => response.json())
    .then(data => {
      window.localStorage.setItem('auth_user', JSON.stringify(data))
    })
}

function viewRecord (id) {
  console.log('view record', id)

  get(baseUrl + `incidents/${id}`)
    .then(response => response.json())
    .then(data => {
      console.log(data.data)
      window.localStorage.setItem('current_incident', JSON.stringify(data.data))
      window.location = 'view_record.html'
    })
}

function editRecord (id) {
  console.log('edit record', id)

  get(baseUrl + `incidents/${id}`)
    .then(response => response.json())
    .then(data => {
      window.localStorage.setItem('current_incident', JSON.stringify(data.data))
      window.location = 'edit_record.html'
    })
}

function deleteRecord (id) {
  console.log('delete record', id)

  deleteData(baseUrl + `incidents/${id}`)
    .then(response => response.json())
    .then(data => {
      window.location = 'dashboard.html'
    }).catch(error => {
      console.log(error)
    })
}

function getHeaders () {
  return {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + window.localStorage.getItem('auth_token')
  }
}

async function get (url) {
  const response = await fetch(url, {
    method: 'get',
    headers: getHeaders()
  })

  if (!response.ok) {
    throw Error(response.statusText)
  }
  return response
}

async function deleteData (url) {
  const response = await fetch(url, {
    method: 'delete',
    headers: getHeaders()
  })

  if (!response.ok) {
    throw Error(response.statusText)
  }
  return response
}

async function postData (url, data) {
  const response = await fetch(url, {
    method: 'post',
    body: JSON.stringify(data),
    headers: getHeaders()
  })
  if (!response.ok) {
    throw Error(response.statusText)
  }
  return response
}

async function patch (url, data) {
  const response = await fetch(url, {
    method: 'patch',
    body: JSON.stringify(data),
    headers: getHeaders()
  })
  if (!response.ok) {
    throw Error(response.statusText)
  }
  return response
}

function signup () {
  let signupUrl = baseUrl + 'auth/signup'

  let username = document.getElementsByName('username')[0].value
  let password = document.getElementsByName('password')[0].value
  let email = document.getElementsByName('email')[0].value
  let firstname = document.getElementsByName('firstname')[0].value
  let lastname = document.getElementsByName('lastname')[0].value

  let formData = {
    username,
    password,
    email,
    firstname,
    lastname
  }

  let request = new Request(signupUrl, {
    method: 'post',
    body: JSON.stringify(formData),
    headers: { 'Content-Type': 'application/json' }
  })

  fetch(request)
    .then(response => {
      if (!response.ok) {
        throw Error(response.statusText)
      }

      return response
    }).then(response => response.json())
    .then(data => {
      console.log(data)
      window.localStorage.setItem('user', data.data)
      window.location = 'login.html'
    }).catch(error => {
      console.log(error)
    })
}
