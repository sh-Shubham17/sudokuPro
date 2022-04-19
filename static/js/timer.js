let totalTime = 0;
let timebeforPause = 0
let Interval_Id;
console.log("I'm in script file");
function startTimer(){
    let timer = document.getElementById("timer");
    let inputTime = document.getElementById("timerInput");
    let startTime = Date.now();
    Interval_Id = setInterval(frame, 1000);
    
    function frame(){
        try {
        totalTime = timebeforPause + (Date.now() - startTime);
        let mm = Math.floor(totalTime / (1000*60 ));
        let ss = Math.floor( (totalTime/1000) % 60);
        mm = mm.toString().padStart(2,'0');
        ss = ss.toString().padStart(2,'0');
        let timeString = `${mm}:${ss}`;
        timer.innerHTML = timeString;
        inputTime.value = timeString;
            }
        catch(err){
            console.log("error occured! in catch now");
            console.log(err);
            clearInterval(Interval_Id)
        }
    }
}

function pauseTimer(){
    pausebutton = document.getElementById("pause")
    console.log(pausebutton.value)
    console.log(pausebutton.checked)
    console.log(pausebutton)
    if( pausebutton.checked )
    {
        clearInterval(Interval_Id);
        timebeforPause = totalTime;
        document.getElementById("sudokugrid").style.display = "none";
        document.getElementById("gridReplacer").style.display = "block";
    }
    else{
        document.getElementById("sudokugrid").style.display = "block";
        document.getElementById("gridReplacer").style.display = "none";
        startTimer()
    }

}