<?php
include 'connect.php';

$name = $_POST['name'];
$father = $_POST['father-name'];
$gender = $_POST['gender'];
$type = $_POST['ctype'];
$religion = $_POST['religion'];
$blood_group = $_POST['blood-group'];
$mark = $_POST['body-mark'];
$nationality = $_POST['nationality'];
$crime = $_POST['crime'];


$image = $_FILES['face-image']['name'];
$image_tmp = $_FILES['face-image']['tmp_name'];
$image_folder = "uploads/" . basename($image);


if (!is_dir("uploads")) {
    mkdir("uploads", 0777, true);
}


if (move_uploaded_file($image_tmp, $image_folder)) {

    $stmt = $con->prepare("INSERT INTO criminal_registration (`Name`, `Father`, `Gender`, `Type`, `Religion`, `Blood Group`, `Mark`, `Nationality`, `Crime`, `image`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
    $stmt->bind_param("ssssssssss", $name, $father, $gender, $type, $religion, $blood_group, $mark, $nationality, $crime, $image);

    if ($stmt->execute()) {
        echo "<script>alert('Criminal registered successfully'); window.location.href='register.html';</script>";
    } else {
        echo "Error: " . $stmt->error;
    }

    $stmt->close();
} else {
    echo "Failed to upload image.";
}

$con->close();
?>