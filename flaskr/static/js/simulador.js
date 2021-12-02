(function()
{
	if( !window.bootstrap && window.coreui )
		window.bootstrap = window.coreui;
		
	const modal 			= new bootstrap.Modal(document.querySelector('#modal-resultado'), {});
	const btnGuardar 		= document.querySelector('#btn-guardar-diagnostico');
	const btnDiagnosticar 	= document.querySelector('#btn-diagnosticar');
	const elResultado		= document.querySelector('#resultado-diagnostico');
	
	function obtenerSeleccion()
	{
		const ids = [];
		document.querySelectorAll('[name=sintoma]:checked').forEach( (el) => 
		{
			ids.push( parseInt(el.value) );
		});
		return ids;
	}
	function obtenerResultado(ids)
	{
		let match = null;
		for(let resultado of resultados)
		{
			if( resultado.ids.equals(ids) )
			{
				match = resultado;
				break;
			}
		}
		return match;
	}
	btnDiagnosticar.addEventListener('click', function()
	{
		
		try
		{
			const ids = obtenerSeleccion();
			if( ids.length <= 0 )
				throw {error: 'Debe seleccionar almenos un sintoma'};
			const resultado = obtenerResultado(ids);
			console.log('resultado', resultado);
			if( !resultado )
			{
				elResultado.innerHTML = 'No se encontraron resultados para los sintomas seleccionados';
			}
			else
			{
				elResultado.innerHTML = resultado.resultado;
			}
			modal.show();
		}
		catch(e)
		{
			console.log(e);
			alert(e.error);
		}
		
	});
	btnGuardar.addEventListener('click', function()
	{
		try
		{
			const ids = obtenerSeleccion();
			if( ids.length <= 0 )
				throw {error: 'Debe seleccionar almenos un sintoma'};
			const resultado = obtenerResultado(ids);
			console.log('resultado', resultado);
			const form = document.createElement('form');
			const elRes = document.createElement('input');
			elRes.type = 'hidden';
			elRes.name = 'resultado';
			elRes.value = btoa(JSON.stringify(resultado));
			form.style	= 'display:none;';
			form.action = baseurl + 'pacientes/'+ paciente.id +'/diagnosticos/nuevo';
			form.method = 'post';
			form.appendChild(elRes);
			document.body.appendChild(form);
			form.submit();
		}
		catch(e)
		{
			console.log(e);
			alert(e.error);
		}
	});
})();
