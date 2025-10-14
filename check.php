<?php
include 'connect.php';
session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['submit'])) {
    $email = mysqli_real_escape_string($con, $_POST['email']);
    $password = mysqli_real_escape_string($con, $_POST['password']);

    $sql = "SELECT * FROM shop_owners_login WHERE Email='$email' AND Password='$password'";
    $que = mysqli_query($con, $sql);

    if (mysqli_num_rows($que) > 0) {
        $_SESSION['email'] = $email;

        // Redirect to dashboard
        header("Location: mip.html");
        exit();
    } else {
        echo "<script>alert('Invalid email or password'); window.location.href='login.html';</script>";
    }

    mysqli_close($con);
} else {
    echo "<script>alert('Invalid access method'); window.location.href='login.html';</script>";
}
?>
