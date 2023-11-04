
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
        var categoria = '';
        var precio = '';
        

        if(selectedId){

            switch (selectedId) {
                case 'elemento1':
                    categoria = '1';
                    precio = '40';
                    break;
                case 'elemento2':
                    categoria = '2';
                    precio = '80';
                    break;
                case 'elemento3':
                    categoria = '3';
                    precio = '160';
                    break;
                case 'elemento4':
                    categoria = '4';
                    precio = '160';
                    break;
                case 'elemento5':
                    categoria = '5';
                    precio = '240';
                    break;
                case 'elemento6':
                    categoria = '6';
                    precio = '320';
                    break;
                case 'elemento7':
                    categoria = '7';
                    precio = '400';
                    break;
            }    


            $('#input_precio').val(precio);
            $('#input_categoria').val(categoria);

            $('#form_operador').submit();


            $('.selected').removeClass('selected');

        }

    });

