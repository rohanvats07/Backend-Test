
<?php
// Database connection parameters
$host = "localhost";  // Change this if your database is on a different server
$username = "root";   // Change this to your database username
$password = "";       // Change this to your database password
$database = "ezdata";  // Change this to your database name


$conn = new mysqli($host, $username, $password, $database);

// Check the connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} else {
    // Get form data
    $name = $_POST['name'];
    $email = $_POST['email'];
    $password = $_POST['password'];

    // Use prepared statement to prevent SQL injection
    $stmt = $conn->prepare("INSERT INTO user (name, email, password) VALUES (?, ?, ?)");
    
    // Bind parameters
    $stmt->bind_param("sss", $name, $email, $password);

    // Execute the statement
    if ($stmt->execute()) {
        echo "Registration successful...";
    } else {
        echo "Error: " . $stmt->error;
        echo "SQL Error: " . $stmt->errno . " - " . $stmt->error;
    }

    // Close the statement and connection
    $stmt->close();
    $conn->close();
}


?>

