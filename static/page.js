setTimeout(function(){
    $('img').each(function(v, e){
        console.log(v, e)
        $(e).attr('src', $(e).attr('data-original'))
    })
}, 100)