window.opn = 0;
window.image = {};
window.image.format = 'jpg';

$(window).on('load', function(){

    $('#upload_button').bind("click" , function () {
        $('#upload_input').click();
    });

    $('#zoom_in').on('click',function(){
        var scale = $('#target').css('transform');
        scale = scale.replace('matrix(','').replace(')','').replace(' ','').replace(' ','').replace(' ','').replace(' ','').replace(' ','').split(',')[0];
        scale = parseFloat(scale) + 0.1;
        $('#target').css('transform','scale('+scale+')');
        $('#target_0').css('transform','scale('+scale+')');
    });

    $('#zoom_out').on('click',function(){
        var scale = $('#target').css('transform');
        scale = scale.replace('matrix(','').replace(')','').replace(' ','').replace(' ','').replace(' ','').replace(' ','').replace(' ','').split(',')[0];
        scale = parseFloat(scale) - 0.1;
        if(scale > 0.5){
            $('#target').css('transform','scale('+scale+')');
            $('#target_0').css('transform','scale('+scale+')');
        }else{
            console.log('Zoom out limit reached');
        }
    });

    $('#undo').on('click',function(){
        window.opn = window.opn - 1;
        if(window.opn < 0){
            window.opn = 0;
        }
        d = new Date();
        var image_name = 'images/_target/' + window.opn + '.' + window.image.format;
        $('#target').attr('src', image_name+'?'+d.getTime());
        $('#target_slave').attr('href', image_name+'?'+d.getTime());
        showLoading();
    });

    $('#reset').on('click',function(){
        window.opn = 0;
        d = new Date();
        var image_name = 'images/_target/' + window.opn + '.' + window.image.format;
        $('#target').attr('src', image_name+'?'+d.getTime());
        $('#target_slave').attr('href', image_name+'?'+d.getTime());
        showLoading();
    });

    $('#blur').on('click',function(){
        var file = window.opn +'.'+ window.image.format;
        window.opn = window.opn + 1;
        var sig = jQuery('#blur_range').val();
        dataParams = {
            filename    : file,
            opn         : window.opn,
            format      : window.image.format,
            sig        : sig
        }
        performOperation(dataParams, 'blur.py');
    });

    $('#sharp').on('click',function(){
        var file = window.opn +'.'+ window.image.format;
        window.opn = window.opn + 1;
        var scale = jQuery('#sharp_range').val();
        var divideby_val = jQuery('#sharp_range').attr('divideby');
        scale = scale/divideby_val;
        dataParams = {
            filename    : file,
            opn         : window.opn,
            format      : window.image.format,
            scale       : scale
        }
        performOperation(dataParams, 'sharp.py');
    });

    $('#targetChange').on('click',function(){
        show = parseInt(jQuery(this).attr('show') );
        showTarget(show);
    });

    $('#histeq').on('click',function(){
        var file = window.opn +'.'+ window.image.format;
        window.opn = window.opn + 1;
        dataParams = {
            filename    : file,
            opn         : window.opn,
            format      : window.image.format
        }
        performOperation(dataParams, 'histeq.py');
    });

    $('#logtx').on('click',function(){
        var file = window.opn +'.'+ window.image.format;
        window.opn = window.opn + 1;
        dataParams = {
            filename    : file,
            opn         : window.opn,
            format      : window.image.format
        }
        performOperation(dataParams, 'logtx.py');
    });

    $('#gamma_correct').on('click',function(){
        var file = window.opn +'.'+ window.image.format;
        window.opn = window.opn + 1;
        var gamma = $('#gamma_correct_frame input').val();
        dataParams = {
            filename    : file,
            opn         : window.opn,
            format      : window.image.format,
            gamma       : gamma
        }
        performOperation(dataParams, 'gammacrct.py');
    });

    $.ajax({
        url: "scripts/imports.py",
        success: function(data){
            console.log(data);
        }
   });
});

/** FUNCTION DEFINITIONS **/
function customSubmit(obj){
    $.ajax({
        url: "upload.php",
        type: "POST",
        data:  new FormData(obj),
        beforeSend: function(){$("#body-overlay").show();},
        contentType: false,
        processData:false,
        success: function(data){
            try{
                window.opn = 0;
                var image_name = JSON.parse(data)['filename'];
                window.image.format = JSON.parse(data)['format'];
                if(image_name.length < 1){
                    image_name = 'images/_gui/default.jpg';
                    alert("There was some error while Uploading the Image !");
                }
                d = new Date();
                $('#target').attr('src', image_name+'?'+d.getTime());
                $('#target_0').attr('src', image_name+'?'+d.getTime());
                $('#target_slave').attr('href', image_name+'?'+d.getTime());
                // setInterval(function(){
                //     $("#body-overlay").hide();
                // },500);
            }catch(error){
                console.error(error);
                alert('Some ERROR occured !');
            }
        }
   });
}

function hideLoading(){
    $("#body-overlay").hide();
}

function showLoading(){
    $("#body-overlay").show();
}

function performOperation(dataParams, scriptname){
    $.ajax({
        url: "scripts/"+scriptname,
        type: "GET",
        data: dataParams,
        beforeSend: function(){
            showLoading();
        },
        success: function(data){
            try{
                var image_name = JSON.parse(data)['filename'];
                if(image_name.length < 1){
                    image_name = 'images/_gui/default.jpg';
                    alert("There was some error while Uploading the Image !");
                }
                d = new Date();
                $('#target').attr('src', image_name+'?'+d.getTime());
                $('#target_slave').attr('href', image_name+'?'+d.getTime());
            }catch(error){
                console.error(error);
                alert('Some ERROR occured !');
            }
        }
   });
}

function showTarget(num = 1){
    if(num == 0){
        // showing orignal
        $('#target_0').show();
        $('#target').hide();
        $('button').attr('disabled','');
        $('#targetChange').removeAttr('disabled');

        // For next one..
        $('#targetChange').attr('show',1);
        $('#text').html('Latest');
        $('#targetChange .glyphicon').removeClass('glyphicon-eye-open').addClass('glyphicon-eye-close');
    }else{
        // showing latest
        $('#target').show();
        $('#target_0').hide();
        $('button').removeAttr('disabled');

        // For next one..
        $('#targetChange').attr('show',0);
        $('#text').html('Original');
        $('#targetChange .glyphicon').removeClass('glyphicon-eye-close').addClass('glyphicon-eye-open');
    }
}
