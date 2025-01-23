<?php

// It takes as arguments lat, long , date, alt

// Define the file path for storing data
$dataFile = '/absolute-path/data.json';

// Enable error reporting
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Retrieve values from POST request
    $x = isset($_POST['lat']) ? $_POST['lat'] : null;
    $y = isset($_POST['long']) ? $_POST['long'] : null;

    if ($x !== null && $y !== null) {
        // Prepare data to be stored
        $data = array('lat' => $lat, 'long' => $long);
        
        // Save data to a JSON file
        $jsonData = json_encode($data);
        $result = file_put_contents($dataFile, $jsonData);
        
        if ($result === false) {
            echo "Error: Could not write to the file.";
        } else {
            echo "Data has been saved successfully.";
        }
    } else {
        echo "Error: Both lat and long are required.";
    }
} elseif ($_SERVER['REQUEST_METHOD'] === 'GET') {
    // Check if the data file exists
    if (file_exists($dataFile)) {
        // Read the data and return it as a JSON response
        header('Content-Type: application/json');
        echo file_get_contents($dataFile);
    } else {
        echo "No data available.";
    }
} else {
    echo "Error: Only POST and GET requests are allowed.";
}
?>


// to retrieve data = curl http://ec2-13-61-2-224.eu-north-1.compute.amazonaws.com/main/main.php
// to public data =  curl -X POST -d "lat=XXXXXX&long=YYYYYYY&date=ZZZZZZZZZ&alt=WWWWWWWW" http://ec2-13-61-2-224.eu-north-1.compute.amazonaws.com
/main/main.php

// flush data.json = truncate -s 0 data.json

