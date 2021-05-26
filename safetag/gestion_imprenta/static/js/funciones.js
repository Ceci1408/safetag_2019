function agregar_terminaciones()
{
        let total_forms = $("#id_spt-TOTAL_FORMS").attr("value");
        console.log(total_forms);
        let formulario_terminaciones = $("#tabla_terminaciones tr:first");
        let nuevo_formulario = formulario_terminaciones.clone();
        let tabla_formularios = $("#tabla_terminaciones");

        total_forms++;
        nuevo_formulario.find("select").attr("id", "id_spt-"+total_forms+"-terminacion");
        nuevo_formulario.find("select").attr("name", "spt-"+total_forms+"-terminacion");
        nuevo_formulario.find("input:checkbox:first").attr("id", "id_spt-"+total_forms+"-doble_cara_flg");
        nuevo_formulario.find("input:checkbox:first").attr("name", "spt-"+total_forms+"-doble_cara_flg");
        nuevo_formulario.find("input:checkbox:first").prop("checked", false);
        nuevo_formulario.find("input:text").attr("id", "id_spt-"+total_forms+"-comentarios");
        nuevo_formulario.find("input:text").attr("name", "spt-"+total_forms+"-comentarios");
        /*
        nuevo_formulario.find("input:checkbox:last").attr("id", "id_spt-"+total_forms+"-DELETE");
        nuevo_formulario.find("input:checkbox:last").attr("name", "spt-"+total_forms+"-DELETE");
        nuevo_formulario.find("input:checkbox:last").prop("checked", false);
        */
        nuevo_formulario.attr("id", "fila_terminacion_"+total_forms);
        nuevo_formulario.appendTo(tabla_formularios);
        $("#id_spt-TOTAL_FORMS").attr("value", total_forms);
        console.log(total_forms);
}

function redirect()
{
    window.location.replace('/autogestion/');
}

function agregar_dato_contacto()
{
        let total_forms = $("#id_form-TOTAL_FORMS").attr("value")-1;
        let formulario_dc = $("#tabla_contactos tr:first");
        let nuevo_formulario = formulario_dc.clone();
        let tabla_formularios = $("#tabla_contactos");

        total_forms++;
        nuevo_formulario.find("select").attr("id", "id_form-"+total_forms+"-terminacion");
        nuevo_formulario.find("select").attr("name", "form-"+total_forms+"-terminacion");
        nuevo_formulario.find("input:checkbox:first").attr("id", "id_form-"+total_forms+"-doble_cara_flg");
        nuevo_formulario.find("input:checkbox:first").attr("name", "form-"+total_forms+"-doble_cara_flg");
        nuevo_formulario.find("input:checkbox:first").prop("checked", false);
        nuevo_formulario.find("input:text").attr("id", "id_form-"+total_forms+"-comentarios");
        nuevo_formulario.find("input:text").attr("name", "form-"+total_forms+"-comentarios");
        nuevo_formulario.find("input:checkbox:last").attr("id", "id_form-"+total_forms+"-DELETE");
        nuevo_formulario.find("input:checkbox:last").attr("name", "form-"+total_forms+"-DELETE");
        nuevo_formulario.find("input:checkbox:last").prop("checked", false);

        nuevo_formulario.attr("id", "fila_terminacion_"+total_forms);
        nuevo_formulario.appendTo(tabla_formularios);
        $("#id_form-TOTAL_FORMS").attr("value", total_forms);
}
