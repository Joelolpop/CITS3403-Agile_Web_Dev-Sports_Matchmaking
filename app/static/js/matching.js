function removeCard(event) {
    const col = event.target.closest('.col-12, .col-md-6, .col-lg-4');
    if (col) {
        col.remove();
    }
}
