// mi_script.js
const inputIdEstacion = document.getElementById("input-id-estacion");
const selectCasilla = document.getElementById("input-id-casilla");
const casillaOptions = [...selectCasilla];
console.log(casillaOptions);

inputIdEstacion.addEventListener("change", function () {
    const selectedIdEstacion = inputIdEstacion.value;

    casillaOptions.forEach(option => {
        option.style.display = "";
    });

    if (selectedIdEstacion) {
        casillaOptions.forEach(option => {
            const estacionId = option.getAttribute("data-estacion");
            if (estacionId !== selectedIdEstacion) {
                option.style.display = "none";
            }
        });
    }
});
