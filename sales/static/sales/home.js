const reportBtn = document.getElementById('report-btn')
const img = document.getElementById('img')
const modalBody = document.getElementById('modal-body')

const reportForm = document.getElementById('report-form')
const alertBox = document.getElementById('alert-box')

const reportName = document.getElementById('id_name')
const reportRemarks = document.getElementById('id_remarks')
const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value

const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${msg}
        </div>
    `
}

if (img) {
    document.getElementById('img').classList.remove('not-visible')
}

reportBtn.addEventListener('click', () => {
    img.setAttribute('class', 'w-100')
    modalBody.prepend(img)

    reportForm.addEventListener('submit', event => {
        event.preventDefault()

        const formData = new FormData()
        formData.append('name', reportName.value)
        formData.append('remarks', reportRemarks.value)
        formData.append('image', img.src)

        const request = new Request(
            'reports/save/',
            {
                method: 'POST',
                mode: 'same-origin',
                headers: {'X-Requested-With': 'XMLHttpRequest', 'X-CSRFToken': csrfToken},
                body: formData 
            }
        )

        fetch(request)
            .then(response => {

                if (!response.ok) {
                    handleAlerts('danger', `Oops! Something went wrong! Status ${response.status}`)
                    return;
                }

                response.json()
                    .then(data => console.log(data))

                handleAlerts('success', 'Report created!')    
            })

    })
})