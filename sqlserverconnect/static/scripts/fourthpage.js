var loadFile = function(event,image) {
    var output = document.getElementById(image);
    output.src = URL.createObjectURL(event.target.files[0]);
};

function openImageInNewTab(){
    images=document.getElementsByTagName("img");
    for(let i=0;i<images.length;i++){
        if(images[i].src!="http://127.0.0.1:8000/static/images/student.png"){
            images[i].onclick=function(){
                window.open(images[i].src);
            };
        }
    }
}