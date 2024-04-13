function recommendBooks() {
    let query = document.getElementById("user_query");

    if (query.value === '') {
        alert("Please enter some text before querying!")
    }
    else {
        const url = `http://localhost:5000/recommend/${query.value}`
        fetch(url)
            .then(response => response.json())
            .then(json => {
                console.log(json);
            })
    }
}
