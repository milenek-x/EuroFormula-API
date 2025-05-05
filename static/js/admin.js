// CRUD operations for drivers
function loadDrivers() {
    fetch('/api/drivers')
        .then(response => response.json())
        .then(data => {
            const table = document.getElementById('drivers-table');
            table.innerHTML = createTable(data, 'driver');
        });
}

function createDriver(data) {
    fetch('/api/drivers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Driver created successfully');
                loadDrivers();
            }
        });
}

function updateDriver(id, data) {
    fetch(`/api/drivers/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Driver updated successfully');
                loadDrivers();
            }
        });
}

function deleteDriver(id) {
    if (confirm('Are you sure you want to delete this driver?')) {
        fetch(`/api/drivers/${id}`, {
            method: 'DELETE'
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Driver deleted successfully');
                    loadDrivers();
                }
            });
    }
}

// CRUD operations for teams
function loadTeams() {
    fetch('/api/teams')
        .then(response => response.json())
        .then(data => {
            const table = document.getElementById('teams-list');
            table.innerHTML = createTable(data, 'team');
        });
}

function createTeam(data) {
    fetch('/api/teams', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Team created successfully');
                loadTeams();
            }
        });
}

function updateTeam(id, data) {
    fetch(`/api/teams/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Team updated successfully');
                loadTeams();
            }
        });
}

function deleteTeam(id) {
    if (confirm('Are you sure you want to delete this team?')) {
        fetch(`/api/teams/${id}`, {
            method: 'DELETE'
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Team deleted successfully');
                    loadTeams();
                }
            });
    }
}

// CRUD operations for races
function loadRaces() {
    fetch('/api/races')
        .then(response => response.json())
        .then(data => {
            const table = document.getElementById('races-table');
            table.innerHTML = createTable(data, 'race');
        });
}

function createRace(data) {
    fetch('/api/races', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Race created successfully');
                loadRaces();
            }
        });
}

function updateRace(id, data) {
    fetch(`/api/races/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Race updated successfully');
                loadRaces();
            }
        });
}

function deleteRace(id) {
    if (confirm('Are you sure you want to delete this race?')) {
        fetch(`/api/races/${id}`, {
            method: 'DELETE'
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Race deleted successfully');
                    loadRaces();
                }
            });
    }
}

// CRUD operations for results
function loadResults() {
    fetch('/api/results')
        .then(response => response.json())
        .then(data => {
            const table = document.getElementById('results-table');
            table.innerHTML = createTable(data, 'result');
        });
}

function createResult(data) {
    fetch('/api/results', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Result created successfully');
                loadResults();
            }
        });
}

function updateResult(id, data) {
    fetch(`/api/results/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Result updated successfully');
                loadResults();
            }
        });
}

function deleteResult(id) {
    if (confirm('Are you sure you want to delete this result?')) {
        fetch(`/api/results/${id}`, {
            method: 'DELETE'
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Result deleted successfully');
                    loadResults();
                }
            });
    }
}

// Helper functions
function createTable(data, type) {
    if (!data || data.length === 0) {
        return '<p>No data available</p>';
    }

    const headers = Object.keys(data[0]);
    let table = '<table><thead><tr>';
    headers.forEach(header => {
        table += `<th>${header}</th>`;
    });
    table += '<th>Actions</th></tr></thead><tbody>';

    data.forEach(item => {
        table += '<tr>';
        headers.forEach(header => {
            let value = item[header];
            if (typeof value === 'object' && value !== null) {
                value = JSON.stringify(value);
            }
            table += `<td>${value}</td>`;
        });
        table += `<td>
            <button class="action-btn edit-btn" onclick="editItem('${type}', '${item[type === 'driver' ? 'driverNumber' : type === 'team' ? 'teamId' : 'round']}')">Edit</button>
            <button class="action-btn delete-btn" onclick="deleteItem('${type}', '${item[type === 'driver' ? 'driverNumber' : type === 'team' ? 'teamId' : 'round']}')">Delete</button>
        </td></tr>`;
    });

    table += '</tbody></table>';
    return table;
}

function showAddForm(type) {
    const form = document.createElement('form');
    form.className = 'add-form';

    // Create form fields based on type
    switch (type) {
        case 'driver':
            form.innerHTML = `
                <div class="form-group">
                    <label>Driver Number</label>
                    <input type="number" name="driverNumber" required>
                </div>
                <div class="form-group">
                    <label>First Name</label>
                    <input type="text" name="firstName" required>
                </div>
                <div class="form-group">
                    <label>Last Name</label>
                    <input type="text" name="lastName" required>
                </div>
                <div class="form-group">
                    <label>Nationality</label>
                    <input type="text" name="nationality" required>
                </div>
                <div class="form-group">
                    <label>Points</label>
                    <input type="number" name="points" required>
                </div>
                <div class="form-group">
                    <label>Status</label>
                    <input type="text" name="status" required>
                </div>
                <div class="form-group">
                    <label>Team Name</label>
                    <input type="text" name="teamName" required>
                </div>
            `;
            break;
        case 'team':
            form.innerHTML = `
                <div class="form-group">
                    <label>Team ID</label>
                    <input type="text" name="teamId" required>
                </div>
                <div class="form-group">
                    <label>Team Name</label>
                    <input type="text" name="teamName" required>
                </div>
                <div class="form-group">
                    <label>Team Country</label>
                    <input type="text" name="teamCountry" required>
                </div>
                <div class="form-group">
                    <label>Team Points</label>
                    <input type="number" name="teamPoints" required>
                </div>
            `;
            break;
        case 'race':
            form.innerHTML = `
                <div class="form-group">
                    <label>Round</label>
                    <input type="number" name="round" required>
                </div>
                <div class="form-group">
                    <label>Circuit</label>
                    <input type="text" name="circuit" required>
                </div>
                <div class="form-group">
                    <label>City</label>
                    <input type="text" name="city" required>
                </div>
                <div class="form-group">
                    <label>Country</label>
                    <input type="text" name="country" required>
                </div>
            `;
            break;
        case 'result':
            form.innerHTML = `
                <div class="form-group">
                    <label>Round</label>
                    <input type="number" name="round" required>
                </div>
                <div class="form-group">
                    <label>Circuit</label>
                    <input type="text" name="circuit" required>
                </div>
            `;
            break;
    }

    form.innerHTML += '<button type="submit" class="btn btn-primary">Save</button>';

    form.onsubmit = function (e) {
        e.preventDefault();
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        switch (type) {
            case 'driver':
                createDriver(data);
                break;
            case 'team':
                createTeam(data);
                break;
            case 'race':
                createRace(data);
                break;
            case 'result':
                createResult(data);
                break;
        }

        form.remove();
    };

    const container = document.getElementById(`${type}s-table`);
    container.insertBefore(form, container.firstChild);
}

function editItem(type, id) {
    switch (type) {
        case 'driver':
            editDriver(id);
            break;
        case 'team':
            editTeam(id);
            break;
        case 'race':
            editRace(id);
            break;
        case 'result':
            editResult(id);
            break;
        default:
            alert('Unknown type: ' + type);
    }
}

function deleteItem(type, id) {
    if (confirm('Are you sure you want to delete this item?')) {
        switch (type) {
            case 'driver':
                deleteDriver(id);
                break;
            case 'team':
                deleteTeam(id);
                break;
            case 'race':
                deleteRace(id);
                break;
            case 'result':
                deleteResult(id);
                break;
        }
    }
}

// Load initial data
document.addEventListener('DOMContentLoaded', () => {
    loadDrivers();
    loadTeams();
    loadRaces();
    loadResults();
}); 