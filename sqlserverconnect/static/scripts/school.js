var arrHead1 = new Array();	// array for header.
arrHead1 = ['Name Of Previous School', 'SchoolAddress', 'Year/s of study', 'Class studied', 'Medium of instruction', 'Marks /grade', 'Board'];

function createRowsibs() {
    var empTab = document.getElementById('empTable');
    var limit = document.getElementById("rowlimit").value;
    limit++;
    document.getElementById("rowlimit").value = limit;

    var rowCnt = empTab.rows.length;   // table row count.
    var tr = empTab.insertRow(rowCnt); // the table row.

    for (var c = 0; c < arrHead1.length; c++) {
        var td = document.createElement('td'); // table definition.
        td = tr.insertCell(c);

        // 2nd, 3rd and 4th column, will have textbox.
        var ele = document.createElement('textarea');
        ele.setAttribute('type', 'text');
        ele.setAttribute('rows', '4')
        ele.setAttribute('cols', '9')
        ele.setAttribute('required', '')
        ele.setAttribute('id', (limit - 1) * 7 + c + 1)
        ele.setAttribute('name', (limit - 1) * 7 + c + 1)
        td.appendChild(ele);
    }
}

// delete TABLE row function.
function removeRow() {
    var empTab = document.getElementById('empTable');
    var limit = document.getElementById("rowlimit").value;
    if (limit > 0) {
        table = document.getElementById("empTable").deleteRow(limit);
        limit--;
    }
    document.getElementById("rowlimit").value = limit;
}
function verifyTextArea() {
    var limit = document.getElementById("rowlimit").value;
    for (var i = 1; i <= limit; i++) {
        var index = ((i * 7) - 1).toString();
        var val = document.getElementById(index);
        if (isNaN(val.value)) {
            alert("Marks/Grade column should be numeric");
            return false;
        }
    }

}