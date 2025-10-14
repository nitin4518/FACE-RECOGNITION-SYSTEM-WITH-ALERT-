<?php
include 'connect.php';
if(isset($_POST['submit']))
{
    $name=$_POST['fullName'];
    $email=$_POST['email'];
    $address=$_POST['address'];
    $pincode=$_POST['pin'];
    $password=$_POST['password'];
    $sql="insert into shop_owners_login(Name,Email,Address,pincode,Password) values('$name','$email','$address','$pincode','$password')";
    if(mysqli_query($con,$sql))
    {
        header("Location: login.html");
        exit();
    }
    else
    {
        echo "error detected".mysqli_error($con);
    }
    mysqli_close($con);
}
?>