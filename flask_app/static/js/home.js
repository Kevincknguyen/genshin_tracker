
document.getElementById("defaultOpen").click();

function openTab(evt, tabName) {
    
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";


}

let deselect=""
function filter(filter){
    let here=document.getElementsByClassName(filter)
    let gone=document.getElementsByClassName("entry");
    for (let i=0; i<gone.length;i++){
        gone[i].style.display="none"
        for (let j=0; j<here.length; j++){
            here[j].style.display="initial"
        }
    
    }
    if (deselect==filter){
        for (let i=0; i<gone.length;i++){
            gone[i].style.display="initial"
        }
        deselect="";
        return;
    
    }
    deselect=filter;
}


var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("mouseover", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    content.style.display = "block" 
    });
    coll[i].addEventListener("mouseout", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        content.style.display = "none" 
        });
}



// let myForm=document.getElementById('myForm');
// myForm.onkeyup=function(e){
//     e.preventDefault();
//     let form= new FormData(myForm);
//     fetch ("http://localhost:5000/search", {method: 'POST', body : form})
//         .then(response => response.json())
//         .then(data => 
            
            
//             {
//             var livesearchresults=document.getElementById('livesearchresults')
//             for (let i=0; i<data.length;i++){
//                 let div=document.createElement('div')
//                 div.innerHTML=data[i].name;

//                 livesearchresults.append(div)
//             }
//         })
    
// }

const filterForm=document.getElementById('myForm')
const filterInput=filterForm.querySelector('input')
const matchTable=document.getElementById('livesearchresults')

filterInput.addEventListener('input', e => {
    fetch('/search', {method :'Post', body: new FormData(filterForm)})
    .then(res => res.json())
    .then(res => {
        matchTable.innerHTML=''
        for (let dict of res){
            const div=document.createElement('div')
            div.innerHTML=`
                <h3>${dict.name}</h3>
                <a href="/characters/${dict.name}">
                <img class="searchimage" src="https://api.genshin.dev/characters/${dict.name}/icon" alt="">
                ${dict.name}
                
                </a>
            `
            matchTable.append(div)
        }
    })
})
// function showResult(str) {
//     if (str.length==0) {
//         document.getElementById("livesearch").innerHTML="";
//         document.getElementById("livesearch").style.border="0px";
//         return;
//     }
//     var xmlhttp=new XMLHttpRequest();
//     xmlhttp.onreadystatechange=function() {
//         if (this.readyState==4 && this.status==200) {
//             document.getElementById("livesearch").innerHTML=this.responseText;
//             document.getElementById("livesearch").style.border="1px solid #A5ACB2";
//         }
//     }
//     xmlhttp.open("GET","livesearch.php?q="+str,true);
//     xmlhttp.send();
// }