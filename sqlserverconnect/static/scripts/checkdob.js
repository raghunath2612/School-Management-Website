function checkDOB(){
    console.log("check dob working")
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1; //January is 0!
    var yyyy = today.getFullYear();
    if(dd<10){
            dd='0'+dd
        } 
        if(mm<10){
            mm='0'+mm
        } 

    maxdate = yyyy-2+'-'+mm+'-'+dd;
    document.getElementById("dob").setAttribute("max",maxdate);
}