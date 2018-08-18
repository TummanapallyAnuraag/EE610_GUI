<?php
/* Some part of this code is inspired from https://www.w3schools.com/ */
/*Varialbe Declarations - self explanatory*/
$target_dir = "images/_target/";
$uploadOk = 1;
$imageFileType = strtolower(pathinfo(basename($_FILES["pic"]["name"]),PATHINFO_EXTENSION));
$target_file = $target_dir . "0." . $imageFileType;

/* Response to be sent to the Webpage */
$response = array();
$response["filename"] = "";
$response["format"] = "";
// Check if image file is a actual image or fake image
$check = getimagesize($_FILES["pic"]["tmp_name"]);
if($check !== false) {
    // echo "File is an image - " . $check["mime"] . ".";
    $response[] = "File is an image - " . $check["mime"] . ".";
    $uploadOk = 1;
} else {
    $response[] = "File is not an image.";
    $uploadOk = 0;
}
// Check file size max: 20MB
if ($_FILES["pic"]["size"] > 20000000) {
    $response[] = "Sorry, your file is too large.";
    $uploadOk = 0;
}

if ($uploadOk == 0) {
    $response[] = "Sorry, your file was not uploaded.";
// if everything is ok, try to upload file
} else {
    if (move_uploaded_file($_FILES["pic"]["tmp_name"], $target_file)) {
        $response[] = "The file ". basename( $_FILES["pic"]["name"]). " has been uploaded.";
        $response["filename"] = $target_file;
        $response["format"] = $imageFileType;
    } else {
        $response[] = "Sorry, there was an error uploading your file.";
    }
}
/* JSON is a popular format to send data to and from webpages */
echo json_encode($response);
?>
