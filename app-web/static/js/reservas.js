// No permite enviar la modificación de la reserva hasta que el usuario no cambie alguna fecha.
$('#modificarReserva').attr('disabled', true);

// Habilita el botón de modificar al cambiar la fecha de inicio si es distinta a la fecha inicio original de la reserva.
$('#inicio_reserva').on('change', function (event, date) {
  const fechaInicial = $('#inicio_reserva').attr('data-fecha-inicio');
  const fechaFinal = $('#fin_reserva').attr('data-fecha-fin');
  const fechaSeleccionada = moment(date).format('YYYY-MM-DD');
  $('#fin_reserva').bootstrapMaterialDatePicker('setMinDate', fechaSeleccionada);
  $('#fin_reserva').bootstrapMaterialDatePicker('setDate', fechaSeleccionada);
  $('#fin_reserva').val(fechaSeleccionada);

  if (fechaInicial != fechaSeleccionada) {
    $('#modificarReserva').attr('disabled', false);
  } else if (fechaInicial == fechaSeleccionada && fechaFinal == $('#fin_reserva').val()) {
    $('#modificarReserva').attr('disabled', true);
  }
});

// Habilita el botón de modificar al cambiar la fecha de fin si es distinta a la fecha fin original de la reserva.
$('#fin_reserva').on('change', function (event, date) {
  const fechaInicial = $('#inicio_reserva').attr('data-fecha-inicio');
  const fechaFinal = $('#fin_reserva').attr('data-fecha-fin');
  const fechaSeleccionada = moment(date).format('YYYY-MM-DD');
  if (fechaFinal != fechaSeleccionada) {
    $('#modificarReserva').attr('disabled', false);
  } else if (fechaFinal == fechaSeleccionada && fechaInicial == $('#inicio_reserva').val()) {
    $('#modificarReserva').attr('disabled', true);
  }
});

// Setea el texto del modal si se toca cancelar.
$('#cancelarReserva').on('click', function () {
  $('#myModalTitle').text('Cancelar reserva');
  $('#myModalBody').html('Si continua la reserva se cancelará.<br>Este proceso es <strong>irreversible.</strong>');
  $('form').attr('action', "{{url_for('cancelar_reserva')}}");
});

// Setea el texto del modal si se toca modificar.
$('#modificarReserva').on('click', function () {
  $('#myModalTitle').text('Modificar reserva');
  $('#myModalBody').html('Los cambios estarán sujetos a la<strong> disponibilidad</strong> del hotel.');
  $('form').attr('action', "{{url_for('modificar_reserva')}}");
});
