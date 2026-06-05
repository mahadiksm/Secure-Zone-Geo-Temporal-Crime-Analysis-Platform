<?php

$conn = new mysqli("localhost","root","","crime_db");

if($conn->connect_error){
die("Connection Failed : " . $conn->connect_error);
}

$data = json_decode(file_get_contents("php://input"), true);

if(!$data){
die("No Data Received");
}

$crime_id    = $data['crime_id'];
$date        = $data['date'];
$day         = $data['day'];
$month       = $data['month'];
$year        = $data['year'];
$start_time  = $data['start_time'];
$end_time    = $data['end_time'];
$location    = $data['location'];
$crime_type  = $data['crime_type'];
$crime_count = $data['crime_count'];

$sql = "INSERT INTO crimes
(
crime_id,
date,
day,
month,
year,
start_time,
end_time,
location,
crime_type,
crime_count
)

VALUES
(
'$crime_id',
'$date',
'$day',
'$month',
'$year',
'$start_time',
'$end_time',
'$location',
'$crime_type',
'$crime_count'
)";

if($conn->query($sql) === TRUE){

echo "Success";

}else{

echo "Database Error : " . $conn->error;

}

$conn->close();

?>