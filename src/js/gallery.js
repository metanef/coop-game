// src/js/gallery.js

let currentImageIndex = 0;

export function setupGallery(images) {
    const galleryContainer = document.createElement('div');
    galleryContainer.id = 'gallery';
    galleryContainer.style.display = 'none'; // Cacher par défaut

    const imageElement = document.createElement('img');
    imageElement.id = 'gallery-image';
    imageElement.style.maxWidth = '90%';
    imageElement.style.maxHeight = '90%';
    galleryContainer.appendChild(imageElement);

    const closeButton = document.createElement('button');
    closeButton.innerText = '✖'; // Symbole de fermeture
    closeButton.id = 'close-gallery';
    closeButton.onclick = () => {
        galleryContainer.style.display = 'none'; // Fermer la galerie
    };
    galleryContainer.appendChild(closeButton);

    const prevButton = document.createElement('button');
    prevButton.innerText = '◀'; // Bouton Précédent
    prevButton.onclick = () => changeImage(-1);
    galleryContainer.appendChild(prevButton);

    const nextButton = document.createElement('button');
    nextButton.innerText = '▶'; // Bouton Suivant
    nextButton.onclick = () => changeImage(1);
    galleryContainer.appendChild(nextButton);

    document.body.appendChild(galleryContainer);

    // Écouteur d'événements pour fermer la galerie en cliquant dehors
    galleryContainer.addEventListener('click', (event) => {
        if (event.target === galleryContainer) {
            galleryContainer.style.display = 'none'; // Fermer la galerie
        }
    });

    // Afficher la galerie
    function showGallery(index) {
        currentImageIndex = index;
        imageElement.src = images[currentImageIndex];
        galleryContainer.style.display = 'flex';
        galleryContainer.style.position = 'fixed';
        galleryContainer.style.top = '50%';
        galleryContainer.style.left = '50%';
        galleryContainer.style.transform = 'translate(-50%, -50%)';
        galleryContainer.style.zIndex = '1000';
        galleryContainer.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        imageElement.style.borderRadius = '10px';
    }

    function changeImage(direction) {
        currentImageIndex += direction;
        if (currentImageIndex < 0) {
            currentImageIndex = images.length - 1; // Boucle vers la dernière image
        } else if (currentImageIndex >= images.length) {
            currentImageIndex = 0; // Boucle vers la première image
        }
        imageElement.src = images[currentImageIndex];
    }

    // Ajouter un événement de clic aux images de la galerie
    document.querySelectorAll('#game-screenshots img').forEach((img, index) => {
        img.addEventListener('click', () => showGallery(index));
    });
}