function deleteItExmo(itexmo_id) {
    if (confirm('Are you sure?')) {
        fetch(`/delete_itexmo/${itexmo_id}`, { method: 'POST' })
            .then(() => location.reload());
    }
}

function deleteEmail(ecreds_id) {
    if (confirm('Are you sure?')) {
        fetch(`/delete_email_route/${ecreds_id}`, { method: 'POST' })
            .then(() => location.reload());
    }
}

function deleteHris(hrpears_id) {
    if (confirm('Are you sure?')) {
        fetch(`/delete_hrpears_route/${hrpears_id}`, { method: 'POST' })
            .then(() => location.reload());
    }
}

function deleteLogin(login_api_id) {
    if (confirm('Are you sure?')) {
        fetch(`/delete_loginapi_route/${login_api_id}`, { method: 'POST' })
            .then(() => location.reload());
    }
}

function deleteUSer(user_id) {
    if (confirm('Are you sure?')) {
        fetch(`/delete_user_route/${user_id}`, { method: 'POST' })
            .then(() => location.reload());
    }
}

function deleteRole(role_id) {
    if (confirm('Are you sure?')) {
        fetch(`/delete_role_route/${role_id}`, { method: 'POST' })
            .then(() => location.reload());
    }
}

function deleteDivision(division_id) {
    if (confirm('Are you sure?')) {
        fetch(`/delete_division_route/${division_id}`, { method: 'POST' })
            .then(() => location.reload());
    }
}

function deleteLogs(log_id) {
    if (confirm('Are you sure?')) {
        fetch(`/delete_logs_route/${log_id}`, { method: 'POST' })
            .then(() => location.reload());
    }
}