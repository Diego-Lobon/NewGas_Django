function cambiarCantidad(idForm){
    
    var recolec = $('#'+idForm).serialize();
    recolec += '&metodo=actualizar'


    $.ajax({
        
        url: '',
        type: 'POST',
        data: recolec,

        success:function(vs) {
            $('#contenedorFormulario').load('. #contenedorFormulario')
        }

    })

    
}

function eliminarProducto(idForm, peticion){
    
    var recolec = $('#'+idForm).serialize();
    recolec += '&metodo=eliminar'
    
    $.ajax({
        
        url: '',
        type: 'POST',
        data: recolec,

        success:function(vs) {
            $('#contenedorFormulario').load('. #contenedorFormulario')
        }

    })
  
}