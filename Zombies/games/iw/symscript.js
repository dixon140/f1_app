const lists = [
    ["n", "ball", "anger", "v", "x", "vslice"],
    ["mount", "vslice", "angel", "a", "plus", "n"],
    ["a", "vslice", "plus", "angel", "mount", "n"],
    ["angel", "v", "anger", "x", "vslice", "ball"],
    ["n", "scissors", "anger", "ball", "x", "vslice"],
    ["v", "scissors", "x", "ball", "vslice", "angel"]
];

const images = document.querySelectorAll('.image');
const resultContainer = document.getElementById('result-container');
let selectedImages = [];

// Handle image selection
images.forEach(image => {
    image.addEventListener('click', () => {
        // Toggle selection
        if (image.classList.contains('selected')) {
            image.classList.remove('selected');
            selectedImages = selectedImages.filter(img => img !== image);
        } else if (selectedImages.length < 4) {
            image.classList.add('selected');
            selectedImages.push(image);
        }

        if (selectedImages.length === 4) {
            findMatchingList(selectedImages);
        } else {
            resultContainer.innerHTML = '';
        }
    });
});


function findMatchingList(selected) {
    const selectedIds = selected.map(img => img.dataset.id);
    resultContainer.innerHTML = '';

    for (const list of lists) {
        const matchingSymbols = list.filter(symbol => selectedIds.includes(symbol));

        if (matchingSymbols.length === 4) {
            matchingSymbols.forEach(symbol => {
                const img = document.querySelector(`img[data-id="${symbol}"]`);
                const newImg = document.createElement('img');
                newImg.src = img.src;
                newImg.classList.add('image');
                resultContainer.appendChild(newImg);
            });
            return;
        }
    }

    resultContainer.innerHTML = '<p>No matching list found</p>';
}
