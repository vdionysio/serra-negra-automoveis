var removePicButton = document.getElementById("remove-pic-btn");
button.addEventListener("click", removePicDiv);

function removePicDiv() {
fetch('https://example.com/api/data')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById("thumb-edit-div").remove()
        console.log(data);
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
  
}