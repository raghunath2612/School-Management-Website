function checkpwds(){
    var pwd1=document.getElementById("newpwd1").value;
    var pwd2=document.getElementById("newpwd2").value;
    if(pwd1===pwd2){
        return true;
    }
    else{
        alert("New passwords are different");
        return false;
    }
}