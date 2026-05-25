// Disable right click
document.addEventListener("contextmenu", e => e.preventDefault());

// Disable drag
document.addEventListener("dragstart", e => e.preventDefault());

// Disable text selection
document.addEventListener("selectstart", e => e.preventDefault());

// Blur when tab switch
document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
        document.body.style.filter = "blur(8px)";
    } else {
        document.body.style.filter = "none";
    }
});

// Block Ctrl+P
document.addEventListener("keydown", function(e){
    if(e.ctrlKey && e.key === 'p'){
        e.preventDefault();
    }
});
const photo = document.getElementById("protected-photo");

document.addEventListener("visibilitychange", () => {
    if (!photo) return;

    if (document.hidden) {
        photo.style.filter = "blur(20px)";
    } else {
        photo.style.filter = "none";
    }
});