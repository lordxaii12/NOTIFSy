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