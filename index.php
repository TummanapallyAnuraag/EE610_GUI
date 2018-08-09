<!DOCTYPE html>
<html>
<head>
	<title>Basic Image Editor</title>
	<link rel="stylesheet" type="text/css" href="gui.css">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
</head>
<body>
	<?php
	if(copy('images/_gui/default.jpg','images/_target/0.jpg')){
		echo '<span style="display:none;">Default Image Copied.</span>';
	}
	?>
	<div id="body-overlay"><div><img src="images/_gui/loading.gif" width="64px" height="64px"/></div></div>
	<plank>
		<img id="target" src="images/_gui/default.jpg" style="transform:scale(1);">
	</plank>
	<controls>
		<div>
			<form id="image_form" method="POST" action="upload.php" enctype="multipart/form-data">
				<button type="button" class="btn btn-default btn-md" id="upload_button">
					<span class="glyphicon glyphicon-upload"></span> Upload
				</button>
				<input id="upload_input" type="file" onchange="customSubmit(this.form)" name="pic" accept="image/*" style="display:none;">
				<!-- <input type="submit" name="submit" value="submit"> -->
			</form>
			<button type="button" class="btn btn-default btn-md" id="zoom_in">
				<span class="glyphicon glyphicon-zoom-in"></span>
			</button>
			<button type="button" class="btn btn-default btn-md" id="zoom_out">
				<span class="glyphicon glyphicon-zoom-out"></span>
			</button>
			<button type="button" class="btn btn-default btn-md" id="histeq">
				Histogram Equalise
			</button><br>
			<button type="button" class="btn btn-default btn-md" id="histeq">
				<a id="target_slave" href="" download>Download</a>
			</button><br>
			<button type="button" class="btn btn-default btn-md" id="logtx">
				Log Transform
			</button><br>
		</div>
	</controls>
</body>
<script type="text/javascript">
	window.opn = 0;
	window.image = {};
	window.image.format = 'jpg';
	$('#upload_button').bind("click" , function () {
        $('#upload_input').click();
    });

	$('#zoom_in').on('click',function(){
		var scale = $('#target').css('transform');
		scale = scale.replace('matrix(','').replace(')','').replace(' ','').replace(' ','').replace(' ','').replace(' ','').replace(' ','').split(',')[0];
		scale = parseFloat(scale) + 0.1;
		$('#target').css('transform','scale('+scale+')');
	});

	$('#zoom_out').on('click',function(){
		var scale = $('#target').css('transform');
		scale = scale.replace('matrix(','').replace(')','').replace(' ','').replace(' ','').replace(' ','').replace(' ','').replace(' ','').split(',')[0];
		scale = parseFloat(scale) - 0.1;
		if(scale > 0.5){
			$('#target').css('transform','scale('+scale+')');
		}else{
			console.log('Zoom out limit reached');
		}
	});

	$('#histeq').on('click',function(){
		var filename = window.opn +'.'+ window.image.format;
		window.opn = window.opn + 1;
		$.ajax({
        	url: "scripts/histeq.py?opn="+window.opn+"&format="+window.image.format+"&filename="+filename,
			type: "GET",
			beforeSend: function(){$("#body-overlay").show();},
			success: function(data){
		    	var image_name = JSON.parse(data)['filename'];
		    	if(image_name.length < 1){
		    		image_name = 'images/_gui/default.jpg';
		    		alert("There was some error while Uploading the Image !");
		    	}
				d = new Date();
		    	$('#target').attr('src', image_name+'?'+d.getTime());
				$('#target_slave').attr('href', image_name+'?'+d.getTime());
				setInterval(function(){
					$("#body-overlay").hide();
				},500);
			}
	   });
	});

	$('#logtx').on('click',function(){
		var filename = window.opn +'.'+ window.image.format;
		window.opn = window.opn + 1;
		$.ajax({
        	url: "scripts/logtx.py?opn="+window.opn+"&format="+window.image.format+"&filename="+filename,
			type: "GET",
			beforeSend: function(){$("#body-overlay").show();},
			success: function(data){
		    	var image_name = JSON.parse(data)['filename'];
		    	if(image_name.length < 1){
		    		image_name = 'images/_gui/default.jpg';
		    		alert("There was some error while Uploading the Image !");
		    	}
				d = new Date();
		    	$('#target').attr('src', image_name+'?'+d.getTime());
				$('#target_slave').attr('href', image_name+'?'+d.getTime());
				setInterval(function(){
					$("#body-overlay").hide();
				},500);
			}
	   });
	});

    function customSubmit(obj){
    	$.ajax({
        	url: "upload.php",
			type: "POST",
			data:  new FormData(obj),
			beforeSend: function(){$("#body-overlay").show();},
			contentType: false,
    	    processData:false,
			success: function(data){
				window.opn = 0;
		    	var image_name = JSON.parse(data)['filename'];
				window.image.format = JSON.parse(data)['format'];
		    	if(image_name.length < 1){
		    		image_name = 'images/_gui/default.jpg';
		    		alert("There was some error while Uploading the Image !");
		    	}
				d = new Date();
		    	$('#target').attr('src', image_name+'?'+d.getTime());
				$('#target_slave').attr('href', image_name+'?'+d.getTime());
				setInterval(function(){
					$("#body-overlay").hide();
				},500);
			}
	   });
    }

</script>
</html>
