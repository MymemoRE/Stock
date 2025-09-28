function inputChange(){
    if (textform[1].selected){
        document.getElementById( "SQinput" ).value ="update trade set cost=-10 where rowid="+rowid;
	goukei.textContent="test"+rowid;
    } else if (textform[0].selected){
        document.getElementById( "SQinput" ).value ="insert into trade values("+tday+"01,'"+corp.value+"','"+testt.value+"',"+tnum.value+",0.1,"+rnum.value+","+rate.value+",1,"+stock.value+")"  ;
	
	goukei.textContent="insert new record";
	document.getElementById("testarea").innertext="qqq";
    } else if (textform[2].selected){
	document.getElementById( "SQinput" ).value ="update trade set date="+tday+"01 where rowid="+rowid;
	goukei.textContent="test"+rowid;
    }
}

let textform=document.getElementById("SQform");
let textforms=textform.options;
let goukei=document.getElementById("goukei");
let testt=document.getElementById("tterm");
let corp=document.getElementById("corp");
let tnum=document.getElementById("tnum");
let rnum=document.getElementById("rnum");
let rate=document.getElementById("rate");
let stock=document.getElementById("stock");
const today=new Date();
let ttest=today.getFullYear()*10000+today.getMonth()*100+today.getDate()+100;
let tday=(""+ttest).slice(-6);
let nyear=(""+today).slice(-2);

document.getElementById( "SQinput" ).value ="update trade set date="+tday+"01 where rowid=";

textform.onchange=inputChange;
