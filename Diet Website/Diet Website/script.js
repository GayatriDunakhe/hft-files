// let result = document.getElementById("result");

// function clearResult() {
//     result.value = "";
// }

// function appendToResult(value) {
//     result.value += value;
// }

// function calculateResult() {
//     try {
//         result.value = eval(result.value);
//     } catch (error) {
//         result.value = "Error";
//     }
// }
document.getElementById("calculate").addEventListener("click", function() {
    const weight = parseFloat(document.getElementById("weight").value);
    const height = parseFloat(document.getElementById("height").value);
    const age = parseInt(document.getElementById("age").value);
    const gender = document.getElementById("gender").value;

    let bmr = 0;

    if (gender === "male") {
        bmr = 10 * weight + 6.25 * height - 5 * age + 5;
    } else if (gender === "female") {
        bmr = 10 * weight + 6.25 * height - 5 * age - 161;
    }

    document.getElementById("bmrResult").textContent = bmr.toFixed(2);
});
