// Utility: Generate random hex color
function getRandomColor() {
const letters = '0123456789ABCDEF';
let color = '#';
for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
}
return color;
}

// Utility: Calculate brightness from hex color
function getBrightness(hex) {
// Convert hex to RGB
const r = parseInt(hex.substr(1, 2), 16);
const g = parseInt(hex.substr(3, 2), 16);
const b = parseInt(hex.substr(5, 2), 16);
// Return brightness (formula for perceived brightness)
return (r * 299 + g * 587 + b * 114) / 1000;
}

// Main: Apply random colors with readable text
document.addEventListener("DOMContentLoaded", function () {
const tags = document.querySelectorAll(".tag-box");
tags.forEach(tag => {
    const bgColor = getRandomColor();
    const brightness = getBrightness(bgColor);
    tag.style.backgroundColor = bgColor;
    tag.style.color = brightness > 160 ? "#000000" : "#FFFFFF"; // Use black text on light backgrounds, white on dark
    });
});