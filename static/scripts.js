document.addEventListener("DOMContentLoaded", function() {
    // Seleccionamos el contenedor de las galletas
    var container = document.createElement("div");
    container.id = "galletas-container";
    container.style.position = "fixed";
    container.style.top = "0";
    container.style.left = "0";
    container.style.width = "100%";
    container.style.height = "100%";
    container.style.pointerEvents = "none"; // Evitamos que las galletas intercepten clics

    // Añadimos el contenedor al cuerpo del documento
    document.body.appendChild(container);
    
    // Cantidad de galletas que deseamos mostrar
    var cantidadGalletas = 20; // Puedes ajustar este valor según tus necesidades
    
    // Iteramos para crear cada galleta y posicionarlas aleatoriamente
    for (var i = 0; i < cantidadGalletas; i++) {
        // Creamos una nueva imagen de galleta
        var galleta = document.createElement("img");
        galleta.src = "https://th.bing.com/th/id/R.92dcc04a3813069ffb0393c6a784e40a?rik=%2fRHmBswSN3eLTA&pid=ImgRaw&r=0";
        galleta.style.position = "absolute";
        galleta.style.width = "50px"; // Ancho de las galletitas
        galleta.style.height = "auto"; // Altura ajustada automáticamente
        galleta.style.zIndex = "1";
        galleta.style.animation = "caidaGalletitas linear infinite";
        galleta.style.top = Math.random() * window.innerHeight + "px"; // Posición aleatoria vertical
        galleta.style.left = Math.random() * window.innerWidth + "px"; // Posición aleatoria horizontal

        // Agregamos la galleta al contenedor
        container.appendChild(galleta);
    }
});
