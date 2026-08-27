const okButton = document.getElementById("okbutton");
const toDel = document.getElementById("delafter");
const after = document.getElementById("afterclick")

okButton.addEventListener("click", () => {
    toDel.remove();
    after.textContent = "gullible";
});
