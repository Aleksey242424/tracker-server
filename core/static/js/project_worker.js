const time = document.getElementById("time")
const player = document.getElementById("player")
const stateTxt = document.getElementById("state") 
let statePlayer = false
function start(url,url_for_change_active){
    if (statePlayer){
        statePlayer = false
        player.innerHTML = "▶"
        stateTxt.innerHTML = "paused"
        $.ajax({
            url: url_for_change_active,
            method: 'put',
            dataType: 'json'
        });
    }else{
        $.ajax({
            url: url_for_change_active+'?active=' + true,
            method: 'put',
            dataType: 'json'
        });
        statePlayer = true
        player.innerHTML = "⏸️"
        stateTxt.innerHTML = "started"
        const interval = setInterval(
            function(){
                $.ajax({
                    url: url+'?time=' + time.innerHTML,
                    method: 'put',
                    dataType: 'json',
                    success: function(response){
                         time.innerHTML = response.new_time
                    }
                });
                if (!statePlayer){
                    clearInterval(interval)
                }
            }
            ,1000
        )
    }
}

function end(url_for_change_active){
    $.ajax({
        url: url_for_change_active,
        method: 'put',
        dataType: 'json'
    });
}