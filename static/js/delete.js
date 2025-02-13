function deleteItExmo(itexmo_id) {
    if (confirm('Are you sure?')) {
        fetch(`/delete_itexmo/${itexmo_id}`, { method: 'POST' })
            .then(() => location.reload());
    }
}