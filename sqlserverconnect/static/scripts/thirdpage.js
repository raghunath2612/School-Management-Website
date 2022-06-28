function validateEmail(emailField){
    var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;

    if (reg.test(emailField.value) == false) 
    {
        alert('Invalid Email Address');
        return false;
    }

    return true;
}
var arrHead1 = new Array();	// array for header.
    arrHead1 = ['Class & Section','Name','Admission no :'];

    function createRowsibs() {
        var empTab = document.getElementById('empTable');
        var limit=document.getElementById("rowlimit").value;
        limit++;
        document.getElementById("rowlimit").value=limit;

        var rowCnt = empTab.rows.length;   // table row count.
        var tr = empTab.insertRow(rowCnt); // the table row.

        for (var c = 0; c < arrHead1.length; c++) {
            var td = document.createElement('td'); // table definition.
            td = tr.insertCell(c);

                // 2nd, 3rd and 4th column, will have textbox.
                var ele = document.createElement('input');
                ele.setAttribute('type', 'text');
                ele.setAttribute('value', '');
                ele.setAttribute('name',(limit-1)*3+c+1)
                ele.setAttribute('id',(limit-1)*3+c+1)
                ele.setAttribute('required','')
                td.appendChild(ele);
        }
    }

    // delete TABLE row function.
    function removeRow() {
        var empTab = document.getElementById('empTable');
        var limit=document.getElementById("rowlimit").value;
        if(limit>0){
            table=document.getElementById("empTable").deleteRow(limit);
            limit--;
        } 
        document.getElementById("rowlimit").value=limit;
    }