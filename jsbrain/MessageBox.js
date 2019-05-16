function mboxClear(msgbox) {
    msgbox.className = '';
    msgbox.innerHTML = '';
}

function mboxError(msgbox, text) {
    msgbox.classList.add('has-text-danger');
    msgbox.innerHTML = text;
}

function mboxSuccess(msgbox, text) {
    msgbox.classList.add('has-text-success');
    msgbox.innerHTML = text;
}

module.exports = { mboxClear, mboxError, mboxSuccess }
