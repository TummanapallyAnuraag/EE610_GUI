<?php
    $source         = 'images/_target/'.$_GET['filename'];
    $format         = $_GET['format'];
    $date           = getdate();
    $destination    = 'images/_archive/'.$date[0].'.'.$format;
    if(copy($source,$destination)){
        echo "File archived as ".$date[0].'.'.$format;
    }else{
        echo "Error while archiving!!";
    }
?>
