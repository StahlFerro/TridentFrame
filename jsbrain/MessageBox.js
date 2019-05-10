let td_message_box = document.querySelector('#td_message_box')

function mboxClear() {
    td_message_box.classList.remove('has-text-danger');
    td_message_box.innerHTML = '';
}

function mboxError(text) {
    td_message_box.classList.add('has-text-danger');
    td_message_box.innerHTML = text;
}

function mboxSuccess(text) {
    td_message_box.classList.add('has-text-success');
    td_message_box.innerHTML = text;
}

module.exports = { mboxClear, mboxError, mboxSuccess }
