function deleteNode(quote_no) {
    fetch('/delete-quote', {
        method: 'POST',
        body: JSON.stringify({
            quote_no: quote_no
        }),
    }).then((_res) => {
        window.location.href = "/";
    })
}