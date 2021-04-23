const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const alertBox = document.getElementById('alert-box')

const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
    <div class="alert alert-${type}" role="alert">
        ${msg}
    </div>
    `
}

Dropzone.autoDiscover = false

const myDropZone = new Dropzone('#dropzone-form', {
    url: '../upload/',
    init: function (){
        this.on('sending', function (file, xhr, formData){
            console.log('sending...')
            formData.append('csrfmiddlewaretoken', csrf)
        })
        this.on('success', function (file, response){
            console.log(response)
            const file_upload = response.file_upload
            if (file_upload){
                handleAlerts('success', 'File uploaded successfully')
            }
            else {
                handleAlerts('danger', 'File already exists')
            }
        })
    },
    maxFiles: 3,
    maxFilesize: 3,
    acceptedFiles: '.csv',
})