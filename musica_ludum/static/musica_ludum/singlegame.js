var main, all_row, grade = null;

var flag_stop = false;

var bgm_music;

var timer;



function onloadfunc() {
    main = document.getElementById("blacknwhite"); 
    all_row = getall_row(); 
    // alert("rrr");
<<<<<<< HEAD
    // grade = 1;
=======
    grade = 1;
>>>>>>> a7bbc1644fec14765409eb84a2b259953e43f340





    //grade.value = 0;
    //alert(grade);
    
    
    //bgm_music.play();


    // alert(bgm_music.play());
 
    // var play = document.getElementById("play");
 
    // var pause = document.getElementById("pause");
 
    // var exit = document.getElementById("exit");



    
 
    document.onkeyup = function(event){
        keyplaymode(event);
    };
    //alert("bbb");
};

function getall_row() {
    all_row = [];
    var row01 = document.getElementById('row001');
    var row02 = document.getElementById('row002');
    var row03 = document.getElementById('row003');
    var row04 = document.getElementById('row004');
    var row05 = document.getElementById('row005');
    var row06 = document.getElementById('row006');

    all_row.push(row06);
    all_row.push(row05);
    all_row.push(row04);
    all_row.push(row03);
    all_row.push(row02);
    all_row.push(row01);
 
    initial_rows();
    //alert("aaa");

    return all_row;
}

function initial_rows() {
    for(var i = 0; i < all_row.length; i++) {
        
        all_row[i].hasBlackGrid = false;

        all_row[i].blackGridPos = -1;
        var row = all_row[i].getElementsByTagName('div');
        for(var j = 0; j < row.length; j++) {
            row[j].style.background = '#000';
            row[j].rowPos = i; 
            row[j].colPos = j;
        }
    }
    //alert(all_row[5].hasBlackGrid);
}
 

function startGame() {
    flag_stop = false;
    //alert("aaa");
    bgm_music = document.getElementById("bgm");
    bgm_music.loop = true;
    bgm_music.play();

    grade = document.getElementById("score");

    main.style.borderTop = 'none';
    main.style.borderBottom = 'none';
    init_game();
}



 
function init_game() {
    // Change with bgms
    movement(4,20);
}
 




function movement(pxspeed, speed) {
    // alert(pxspeed);
    //alert(speed);


    clearInterval(timer);

    //alert("bbb");
 
    var n = 1; 
    var hasBlack = false; 
    timer = setInterval(function() {
        var flag = false; 
        //alert(all_row.length);
 
        for(var i = 0; i < all_row.length; i++) {
            var obj = all_row[i];
            //alert(obj);
 
            isGameOver(obj);
 
            if(obj.offsetTop >= 520) {
                flag = true;
 
                obj.style.top = -80 + 'px';
 
                if(n > 50 && !obj.hasBlackGrid) {
                    //randomly change to black
                    var k = Math.floor(Math.random() * 8);
                    //alert(k);
                    obj.getElementsByTagName('div')[k].style.background = '#fff';
                    obj.hasBlackGrid = true;
                    obj.blackGridPos = k;
 
                    hasBlack = true;
                }
            }
            obj.style.top = obj.offsetTop + pxspeed + 'px';
        }
        if(!hasBlack) {
            n++;
        }
 
        if(flag) {
            var tempRow01 = all_row[0];
            all_row.shift();
            all_row.push(tempRow01);
 
        }
    }, speed);
    //alert("aaa");
}
 
function pauseGame() {
    clearInterval(timer);
 
    flag_stop = true;
    //alert("bbb");
 
    if(bgm_music.play) {
        bgm_music.pause();
    }
}
 
function stopGame() {

    //grade.innerHTML = '0';

    clearInterval(timer);
 
    flag_stop = true;
 
    main.style.borderTop = '1px solid #E5F16B';
    main.style.borderBottom = '1px solid #E5F16B';

    //alert("ccc");
 
    all_row[0].style.top = 420 + 'px';
    all_row[1].style.top = 320 + 'px';
    all_row[2].style.top = 220 + 'px';
    all_row[3].style.top = 120 + 'px';
    all_row[4].style.top = 20 + 'px';
    all_row[5].style.top = -80 + 'px';
    //alert("ddd");

    initial_rows();
}
 
function keyplaymode(event) {
//     event = event || window.event;

    event.preventDefault ? event.preventDefault() : event.returnValue = false;
    event.stopPropagation ? event.stopPropagation() : event.cancelBubble = true;
    
 
    if(event.keyCode == 113) { //F2
        startGame();
    } else if(event.keyCode == 32) { //space
        pauseGame();
    } else if(event.keyCode == 115) { //F4
        stopGame();
    } 
    else if((event.keyCode == 83) || (event.keyCode == 68) || (event.keyCode == 70) || (event.keyCode == 71) || (event.keyCode == 72) || (event.keyCode == 74) || (event.keyCode == 75) || (event.keyCode == 76)) {
        //alert(event.keyCode);
        if(!flag_stop) {

            var blackRowPos = -1; 
            var blackGridPos = -1; // whitekeyposition
            for(var i = 0; i < all_row.length; i++) {
                if(all_row[i].hasBlackGrid) {
                    blackRowPos = i;
                    blackGridPos = all_row[i].blackGridPos;
                    break;
                }
            }
 
            // S:83 D:68  F:70 G:71 H:72 J:74  K:75 L:76
 
            if(blackRowPos != -1 && blackGridPos != -1) {
                if((event.keyCode == 83 && blackGridPos == 0)
                    || (event.keyCode == 68 && blackGridPos == 1)
                    || (event.keyCode == 70 && blackGridPos == 2)
                    || (event.keyCode == 71 && blackGridPos == 3)
                    || (event.keyCode == 72 && blackGridPos == 4)
                    || (event.keyCode == 74 && blackGridPos == 5)
                    || (event.keyCode == 75 && blackGridPos == 6)
                    || (event.keyCode == 76 && blackGridPos == 7)){
 
                    if(bgm_music.pause) {
                        bgm_music.play();
                    }
 
                    rightChange(blackRowPos, blackGridPos);
                }
                

                // else if (all_row[5].hasBlackGrid) {
                //         errorGrid = all_row[blackRowPos].getElementsByTagName('div')[7];
                //         alert("aaa");
                //         gameOver(errorGrid);
                //     }

 
 
                  else {
                    var errorGrid;
                    if(event.keyCode == 83) {
                        errorGrid = all_row[blackRowPos].getElementsByTagName('div')[0];
                    } else if(event.keyCode == 68) {
                        errorGrid = all_row[blackRowPos].getElementsByTagName('div')[1];
                    } else if(event.keyCode == 70) {
                        errorGrid = all_row[blackRowPos].getElementsByTagName('div')[2];
                    } else if(event.keyCode == 71) {
                        errorGrid = all_row[blackRowPos].getElementsByTagName('div')[3];
                    } else if(event.keyCode == 72) {
                        errorGrid = all_row[blackRowPos].getElementsByTagName('div')[4];
                    } else if(event.keyCode == 74) {
                        errorGrid = all_row[blackRowPos].getElementsByTagName('div')[5];
                    } else if(event.keyCode == 75) {
                        errorGrid = all_row[blackRowPos].getElementsByTagName('div')[6];
                    } else if(event.keyCode == 76) {
                        errorGrid = all_row[blackRowPos].getElementsByTagName('div')[7];
                    } 


 
                    gameOver(errorGrid);
                }
            }
        }
    //alert("aaa");
    }
}

function rightChange(blackRowPos, blackGridPos) {

    all_row[blackRowPos].hasBlackGrid = false;
    all_row[blackRowPos].blackGridPos = -1;
    //grade.innerHTML = (parseInt(grade.innerHTML) + 1) + '';
 
    var grid = all_row[blackRowPos].getElementsByTagName('div')[blackGridPos];
 
    grid.style.background = 'green';
    setTimeout(function() {
        grid.style.background = '#000';
    }, 100);
}

 
function isGameOver(obj) {
    var temp1 = obj.offsetTop + obj.offsetHeight;
    var temp2 = main.offsetTop + main.offsetHeight - 20;
    if(temp1 > temp2) {
        if(obj.hasBlackGrid) {
            obj.hasBlackGrid = false;
            var index = obj.blackGridPos;
            obj.blackGridPos = -1;
            gameOver(obj.getElementsByTagName('div')[index]);
        }
    }
}
 
function gameOver(errorGrid) {
    errorGrid.style.background = 'red';
    setTimeout(function() {
        errorGrid.style.background = '#000';
        setTimeout(function() {
            errorGrid.style.background = 'red';
            alert("Game Over!");
            //alert('Game Over! Your Score：' + grade.innerHTML + '！');
            stopGame();
        }, 100);
    }, 100);
 
    if(bgm_music.play) {
        bgm_music.pause();
        bgm_music.currentTime = 0;
    }
}
