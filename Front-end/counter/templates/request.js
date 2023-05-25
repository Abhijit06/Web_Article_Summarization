async function handleFormSubmit() {
    console.log("Hello");
    var mainText = document.getElementById('input').value;
    console.log(mainText);
    var summary = "";
    try {
        await fetch(`http://localhost:8000/output?summary=${mainText}`)
            .then(res => res.json())
            .then(data => {
                summary = data;
            });
        console.log(summary["Output Text"])
        document.getElementById("output_box_text").innerHTML = summary["Output Text"];
    } catch (e) {
        console.log(e);
    }
    return false;
}
