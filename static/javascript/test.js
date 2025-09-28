function inputChange(){
    if (textform[0].selected){
        document.getElementById( "SQinput" ).value ="update trade set date=24000001 where rowid=1";        
    } else if (textform[1].selected){
        document.getElementById( "SQinput" ).value ="insert into trade values(24000001,'KHC','div',0.4,0.1,0.3,144.09,1,1)"  ;
    }
}

let textform=document.getElementById("SQform");
let textforms=textform.options;

textform.onchange=inputChange;
