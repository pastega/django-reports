const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value
const alertBox = document.getElementsId('alert-box')

Dropzone.autoDiscover = false

const myDropZone = new Dropzone('#my-dropzone', {
    url: '/reports/upload/',
    init() {
        this.on('sending', (file, xhr, formData) => {
            console.log('Sending...')
        })

        this.on('success', (file, response) => {
            const ex = response.ex
            
            if (ex) {
                alertBox.innerHTML = `
                    <div class="alert alert-danger" role="alert">
                        File already exists!
                    </div>
                `
            } else {
                alertBox.innerHTML = `
                    <div class="alert alert-success" role="alert">
                        Your file has been uploaded!
                    </div>
                ` 
            }
        })
    },
    maxFiles: 3,
    maxFileSize: 3,
    acceptedFiles: '.csv'
})