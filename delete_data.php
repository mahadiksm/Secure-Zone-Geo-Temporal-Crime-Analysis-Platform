<?php
include "db.php";

$id = $_GET['id'];

$conn->query("DELETE FROM crimes WHERE id=$id");

echo "Deleted";
?>