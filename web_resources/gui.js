/* Some variables describing the state of the GUI */
window.opn = 0;
window.image = {};
window.image.format = 'jpg';

/* Some onclick functions */
$(window).on('load', function(){

    /* Trigger click of input tag when button tag is clicked  */
    $('#upload_button').bind("click" , function () {
        $('#upload_input').click();
    });

    /* Increase the size of image in plank when zoom in button is clicked*/
    $('#zoom_in').on('click',function(){
        var scale = $('#target').css('transform');
        scale = scale.replace('matrix(','').replace(')','').replace(' ','').replace(' ','').replace(' ','').replace(' ','').replace(' ','').split(',')[0];
        scale = parseFloat(scale) + 0.1;
        $('#target').css('transform','scale('+scale+')');
        $('#target_0').css('transform','scale('+scale+')');
    });

    /* Self explanatory */
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

    /* Undo 1 operation on button click */
    $('#undo').on('click',function(){
        window.opn = window.opn - 1;
        if(window.opn < 0){
            window.opn = 0;
        }
        /* this date thing is being appended because,it is uniqe for each moment,
         if the same URL of image is replaced,
         the browser will load the image from its cache, and image doesn't get updated. */
        d = new Date();
        var image_name = 'images/_target/' + window.opn + '.' + window.image.format;
        $('#target').attr('src', image_name+'?'+d.getTime());
        $('#target_slave').attr('href', image_name+'?'+d.getTime());
        showLoading();
    });

    /* Self explanatory */
    $('#reset').on('click',function(){
        window.opn = 0;
        d = new Date();
        var image_name = 'images/_target/' + window.opn + '.' + window.image.format;
        $('#target').attr('src', image_name+'?'+d.getTime());
        $('#target_slave').attr('href', image_name+'?'+d.getTime());
        showLoading();
    });

    /* Blur image on button click */
    $('#blur').on('click',function(){
        var file = window.opn +'.'+ window.image.format;
        window.opn = window.opn + 1;
        /* Get the gima value and send to the pythoin script */
        var sig = jQuery('#blur_range').val();
        dataParams = {
            filename    : file,
            opn         : window.opn,
            format      : window.image.format,
            sig         : sig
        }
        performOperation(dataParams, 'blur.py');
    });

    $('#sharp').on('click',function(){
        var file = window.opn +'.'+ window.image.format;
        window.opn = window.opn + 1;

        /* The HTML slider can only take integer values, so this workaround is done. */
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

    /* This will change the image being displayed. */
    $('#targetChange').on('click',function(){
        show = parseInt(jQuery(this).attr('show') );
        showTarget(show);
    });

    /* Histogram Equalisation - self explanatory (refer earlier operations - with similar code)*/
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

    /* Log Transformation */
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

    /* Gamma Correction */
    $('#gamma_correct').on('click',function(){
        var file = window.opn +'.'+ window.image.format;
        window.opn = window.opn + 1;
        var gamma = $('#gamma_correct_frame input').val();
        /* If no gain parameter is sent, default value is 1 */
        dataParams = {
            filename    : file,
            opn         : window.opn,
            format      : window.image.format,
            gamma       : gamma
        }
        performOperation(dataParams, 'gammacrct.py');
    });

    /* Import some packages on load, and load in RAM so that it will reduce time to load
     the packages in future.
     It was observed that around 8-10 seconds of time was being wasted to load the packages.
     So this time can be pipelined with page load.
     Average time for a person to click some button after page load will be around 5-6 seconds.
     So we are exploiting that here.
     */
    $.ajax({
        url: "scripts/imports.py",
        success: function(data){
            console.log(data);
        }
   });
});

/** FUNCTION DEFINITIONS **/
function customSubmit(obj){
    /* This function will send a AJAX request to upload file - which saves the uploaded file */
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

/* A small function to stop showing the loading image*/
function hideLoading(){
    $("#body-overlay").hide();
}

/* Self explanatory */
function showLoading(){
    $("#body-overlay").show();
}

/* A generic function which takes some parameters,
sends them to some script in server, and displays the image which was returned in response. */
function performOperation(dataParams, scriptname){
    $.ajax({
        url: "scripts/"+scriptname,
        type: "GET",
        data: dataParams,
        beforeSend: function(){
            /* The loading... image will be shown*/
            showLoading();
            /* It will be closed when the image is laoded*/
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
                /* Hide loading because - image will not be loaded if there was any error. */
                hideLoading();
                console.error(error);
                alert('Some ERROR occured !');
            }
        }
   });
}

/* This function is responsible for toggling the current image in display */
function showTarget(num = 1){
    /* num=0  implies the original image */
    if(num == 0){
        // showing orignal
        $('#target_0').show();
        $('#target').hide();
        $('button').attr('disabled','');
        $('#targetChange').removeAttr('disabled');

        // For next one..
        $('#targetChange').attr('show',1);  /* show recent image on next click*/
        $('#text').html('Latest');
        $('#targetChange .glyphicon').removeClass('glyphicon-eye-open').addClass('glyphicon-eye-close');
    }else{
        // showing latest
        $('#target').show();
        $('#target_0').hide();
        $('button').removeAttr('disabled');

        // For next one..
        $('#targetChange').attr('show',0); /* Show original image on next click*/
        $('#text').html('Original');
        $('#targetChange .glyphicon').removeClass('glyphicon-eye-close').addClass('glyphicon-eye-open');
    }
}

/*Function for archiving*/
function archiveOnServer(){
    var filename = window.opn + '.' + window.image.format;
    var format = window.image.format;
    dataParams = {
        filename    : filename,
        format      : format
    }
    $.ajax({
        url: "archive.php",
        type: "GET",
        data: dataParams,
        beforeSend: function(){
            /* The loading... image will be shown*/
            showLoading();
        },
        success: function(data){
            hideLoading();
            alert(data);
        }
   });
}
