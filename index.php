<!DOCTYPE html>
<html>
<head>
	<title>Basic Image Editor</title>
	<!-- The Wheel logo displayed in the Tab Heading -->
	<link rel='shortcut icon' type='image/x-icon' href='favicon.ico' />
	<!-- I have used bootstrap for buttons, and jQuery for click actions - to make it simple. -->
	<link rel="stylesheet" href="web_resources/bootstrap.min.css">
	<script src="web_resources/jquery.min.js"></script>
	<!-- CSS and JS which i have used in my GUI -->
	<link rel="stylesheet" type="text/css" href="web_resources/gui.css">
	<script src="web_resources/gui.js"></script>
</head>
<body>
	<?php
	/* On page load copy default image to working directory - _target */
	if(copy('images/_gui/default.jpg','images/_target/0.jpg')){
		echo '<span style="display:none;">Default Image Copied.</span>';
	}
	?>
	<!-- This will be hidden by default, but visible when something is loading -->
	<div id="body-overlay"><div><img src="images/_gui/loading.gif" width="64px" height="64px"/></div></div>
	<!-- This is the image display area -->
	<plank>
		<img id="target" src="images/_gui/default.jpg" onload="hideLoading();" style="transform:scale(1);">
		<img id="target_0" src="images/_gui/default.jpg" onload="hideLoading();" style="transform:scale(1);display:none;">
	</plank>
	<!-- The control panel of my GUI -->
	<controls>
		<div>
			<div class="control-box">
			<!-- Upload Image -->
			<div class="control-row">
				<div class="col-sm-6">
				<form id="image_form" method="POST" action="upload.php" enctype="multipart/form-data">
					<button type="button" class="btn btn-default btn-md" id="upload_button">
						<span class="glyphicon glyphicon-upload"></span> Upload
					</button>
					<input id="upload_input" type="file" onchange="customSubmit(this.form)" name="pic" accept="image/*" style="display:none;">
					<!-- <input type="submit" name="submit" value="submit"> -->
				</form>
				</div>
				<!-- Download Image -->
				<div class="col-sm-6">
					<a id="target_slave" href="images/_gui/default.jpg" download>
					<button type="button" class="btn btn-default btn-md">
						<span class="glyphicon glyphicon-save"></span> Save
					</button>
				</a>
				</div>
			</div>
			<div class="control-row">
				<!-- Zoom In -->
				<div class="col-sm-6">
					<button type="button" class="btn btn-default btn-md" id="zoom_in">
					<span class="glyphicon glyphicon-zoom-in"></span> Max
				</button>
				</div>
				<!-- Zoom Out -->
				<div class="col-sm-6">
					<button type="button" class="btn btn-default btn-md" id="zoom_out">
					<span class="glyphicon glyphicon-zoom-out"></span> Min
				</button>
				</div>
			</div>
			<div class="control-row">
				<!-- Undo -->
				<div class="col-sm-6">
					<button type="button" class="btn btn-default btn-md" id="undo">
					<span style="transform: rotateY(180deg);" class="glyphicon glyphicon-repeat"></span> Undo
				</button>
				</div>
				<!-- Reset -->
				<div class="col-sm-6">
					<button type="button" class="btn btn-default btn-md" id="reset">
					<span class="glyphicon glyphicon-refresh"></span> Reset
				</button>
				</div>
			</div>
			<!-- Toggle View - Original/Recent Image -->
			<div class="control-row-single" >
					<button type="button" class="btn btn-default btn-md" id="targetChange" show="0">
					<span class="glyphicon glyphicon-eye-open"></span> View <span id="text">Original</span>
					</button>
			</div>
			</div>
			<div class="control-box">
			<!-- Histogram Equalisation -->
			<div class="control-row-single">
				<button type="button" class="btn btn-default btn-md" id="histeq">
				Histogram Equalise
				</button><br>
			</div>
			<!-- Log Transform -->
			<div class="control-row-single">
				<button type="button" class="btn btn-default btn-md" id="logtx">
				Log Transform
			</button><br>
			</div>
			<!-- Gamma Correction -->
			<div class="control-row">
				<div id="gamma_correct_frame">
					<div class="col-sm-6">
					<input placeholder="gamma" value="" name="gamma" class="form-control" style="width:120%;">
					</div>
					<div class="col-sm-6">
					<button type="button" class="btn btn-default btn-md" id="gamma_correct">
						<b>&gamma;</b> Correct
					</button>
					</div>
				</div>
			</div>
			<!-- Blurring -->
			<div class="control-row-single" style="margin: 10px 0px;">
				<div id="blur_frame">
					<input id="blur_range" class="form-control" type="range" min="1" max="30" value="15">
					<button type="button" class="btn btn-default btn-md" id="blur">
						Blur
					</button>
				</div>
			</div>
			<!-- Sharpening -->
			<div class="control-row-single">
				<div id="sharp_frame">
				<input id="sharp_range" class="form-control" divideby="100" type="range" min="1" max="50" value="10">
				<button type="button" class="btn btn-default btn-md" id="sharp">
					Sharp
				</button>
			</div>
			</div>
			</div>
		</div>
	</controls>
	<!-- Control Panel Ends Here -->
</body>
</html>
