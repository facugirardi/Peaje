
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
    $('.card-select').click(function() {
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
        } else {
            $('.card').removeClass('selected'); 
            $(this).addClass('selected'); 
        }
    });
});

    $('.emitir').on('click', function() {
        var selectedId = $('.selected').attr('id');

        if(selectedId){

            var resultadoDiv = '';
        
            switch (selectedId) {
                case 'elemento1':
                    resultadoDiv = '1; Motocicleta; 40';
                    break;
                case 'elemento2':
                    resultadoDiv = '2; Automoviles; 80';
                    break;
                case 'elemento3':
                    resultadoDiv = '3; 2 Ejes Con Ruedas Duales o Altura Mayor a 2,10m; 160';
                    break;
                case 'elemento4':
                    resultadoDiv = '4; 3 o 4 Ejes Sin Ruedas Duales y Altura Menor a 2,10m; 160';
                    break;
                case 'elemento5':
                    resultadoDiv = '5; 3 o 4 Ejes Con Ruedas Duales o Altura Mayor a 2,10m; 240';
                    break;
                case 'elemento6':
                    resultadoDiv = '6; 5 o 6 Ejes; 320';
                    break;
                case 'elemento7':
                    resultadoDiv = '7; Más de 6 Ejes; 400';
                    break;
            }    

            console.log(resultadoDiv);

            $('.selected').removeClass('selected');

        }

    });

