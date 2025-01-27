

let formId = 'send-resource';
let resourceForm = document.getElementById(formId);

let checkForm = function () {
    let data = new FormData(resourceForm);
    let donationAmount = data.get('donation_amount');
    let itemAmount = data.get('item_amount');

    if (donationAmount < itemAmount) {
        if (document.getElementById('error-item') != null) {
            return false;
        }
        let element = document.body.appendChild(document.createElement('button'));
        element.id = 'error-item';
        element.classList.add('btn')
        element.classList.add('btn-primary')
        element.classList.add('btn-ln')
        element.style['background-color'] = 'red'

        element.textContent = 'Cannot send items to current request';
        return false;
    }
    return true;
}