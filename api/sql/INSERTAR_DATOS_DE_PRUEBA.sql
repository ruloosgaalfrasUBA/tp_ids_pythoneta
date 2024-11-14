INSERT INTO hoteles (nombre, descripcion, provincia) VALUES 
('Flask Seasons Bariloche', 'Ubicado en el centro de Bariloche', 'Río Negro'),
('Flask Seasons Mar del Plata', 'Hotel con vista al mar', 'Buenos Aires'),
('Flask Seasons Cerro Siete Colores', 'Con vista al famoso cerro', 'Jujuy'),
('Flask Seasons Selva Misionera', 'En medio de la selva misionera', 'Misiones'),
('Flask Seasons Valle de la Luna', 'Hotel cerca del parque Valle de la Luna', 'San Juan'),
('Flask Seasons Cerro Fitz Roy', 'A pocos kilómetros del Cerro Fitz Roy', 'Santa Cruz');
-- 6 hoteles

INSERT INTO reservas (id_hotel) VALUES 
(1),  -- Elon Musk en Flask Seasons Bariloche
(2)  -- Lionel Messi en Flask Seasons Mar del Plata

INSERT INTO reservas (id_reserva, nombre, apellido, dni, inicio_reserva, fin_reserva) VALUES 
((SELECT MAX(id_reserva) as id_reserva FROM reserva;) 'Elon', 'Musk', 12312345, '2024-11-15', '2024-11-20'),
((SELECT MAX(id_reserva) as id_reserva FROM reserva;) 'Lionel', 'Messi', 45659875, '2024-12-01', '2024-12-10');
-- 2 clientes

INSERT INTO servicios (nombre, descripcion) VALUES 
('Spa', 'Acceso completo al spa del hotel'),
('Piscina', 'Uso de la piscina climatizada'),
('Desayuno Buffet', 'Desayuno buffet incluido en la estadía'),
('Gimnasio', 'Acceso al gimnasio del hotel');
-- 4 servicios

INSERT INTO reserva_servicio (numero_reserva, id_servicio) VALUES 
(100, 1),  -- Elon Musk tiene acceso al Spa
(100, 2),  -- Elon Musk tiene acceso a la Piscina
(101, 3),  -- Lionel Messi tiene Desayuno Buffet
(101, 4);  -- Lionel Messi tiene acceso al Gimnasio