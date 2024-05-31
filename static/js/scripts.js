async function borrar(ev) {
    post_id = ev.currentTarget.dataset.id

    resultado = await fetch(`/post/${post_id}`, {
        method: 'DELETE',

    })
    if (!resultado.ok) {
        mensaje = await resultado.text()
        window.alert(mensaje)
        return
    }

    window.location.reload()
}

document.querySelectorAll('a[data-id]').forEach(el => {
    el.addEventListener('click', borrar)
})