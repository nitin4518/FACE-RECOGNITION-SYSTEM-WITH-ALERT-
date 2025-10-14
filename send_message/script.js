let btn = document.querySelector('.yes');


btn.addEventListener("click", ()=> {
        // Import the Twilio module
    const message = "Hello! This is a test message from Twilio.";
    const recipientPhoneNumber = "police_no";

    fetch("https://corn-lyrebird-3238.twil.io/send-sms", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
            message: message,
            to: recipientPhoneNumber,
        }),
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(`Message sent with SID: ${data.sid}`);
        alert("Message sent successfully!");
    })
    .catch((error) => console.error(`Error: ${error.message}`));
});
