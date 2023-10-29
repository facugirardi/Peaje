
const inputIdEstacion = document.getElementById("input-id-estacion");

if(inputIdEstacion) {

    const selectCasilla = document.getElementById("input-id-casilla");
    const casillaOptions = [...selectCasilla];
    

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


}

$(document).ready(function() {
    $('.card').click(function() {
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
        } else {
            $('.card').removeClass('selected'); 
            $(this).addClass('selected'); 
        }
    });
});
