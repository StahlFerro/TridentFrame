function escapeHtml(unsafe) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
 }

 function quintcell_generator(paths, table_body) {
    table_body.innerHTML = '';
    for (var row = 0; row < Math.ceil(paths.length / 5); row++) {
        var tr = document.createElement('TR');
        for (var c = 0; c < 5; c++) {
            const index = (row * 5) + c;
            const img_path = paths[index];
            if (img_path === undefined) {continue;}
            var td = document.createElement('TD');
            var div = document.createElement('DIV');
            div.classList.add('seqdiv');
            var img = document.createElement('IMG');
            img.src = escapeHtml(img_path);
            var i = document.createElement('I');
            i.className = 'fas fa-minus-circle del-icon';
            i.onclick = del_frame;

            var span = document.createElement('SPAN');
            span.classList.add('icon');
            span.appendChild(i);

            var a = document.createElement('A');
            a.className = 'del-anchor';
            a.append(span);

            div.appendChild(img);
            div.appendChild(a);
            td.appendChild(div);
            tr.appendChild(td);
        }
        table_body.appendChild(tr);
    }
}

function del_frame() {
    console.log("delet");
}

 module.exports.escapeHtml = escapeHtml;
 module.exports.quintcell_generator = quintcell_generator;
