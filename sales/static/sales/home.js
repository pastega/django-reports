const reportBtn = document.getElementById('report-btn')
const img = document.getElementById('img')
const modalBody = document.getElementById('modal-body')

const reportForm = document.getElementById('report-form')

const reportName = document.getElementById('id_name')
const reportRemarks = document.getElementById('id_remarks')
const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value

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

        fetch(request).then(response => {
            response.json().then(data => {
                console.log(data)
            })
        })

    })
})