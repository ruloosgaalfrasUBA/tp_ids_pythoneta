INSERT INTO hotel (nombre, descripcion, provincia, estrellas) VALUES 
('Flask Seasons Bariloche', 'Ubicado en el centro de Bariloche', 'Río Negro', 4),
('Flask Seasons Mar del Plata', 'Hotel con vista al mar', 'Buenos Aires', 3),
('Flask Seasons Cerro Siete Colores', 'Con vista al famoso cerro', 'Jujuy', 3),
('Flask Seasons Selva Misionera', 'En medio de la selva misionera', 'Misiones', 3),
('Flask Seasons Valle de la Luna', 'Hotel cerca del parque Valle de la Luna', 'San Juan', 4),
('Flask Seasons Cerro Fitz Roy', 'A pocos kilómetros del Cerro Fitz Roy', 'Santa Cruz', 5);
-- 6 hoteles

INSERT INTO reserva (id_hotel) VALUES (4);
INSERT INTO detalle_reservas (id_reserva, numero_reserva, nombre, apellido, dni, inicio_reserva, fin_reserva) VALUES 
((SELECT MAX(id_reserva) as id_reserva FROM reserva), 100, 'Elon', 'Musk', 12312345, '2024-11-15', '2024-11-20');
-- Elon Musk en Flask Seasons Bariloche

INSERT INTO reserva (id_hotel) VALUES (1);
INSERT INTO detalle_reservas (id_reserva, numero_reserva, nombre, apellido, dni, inicio_reserva, fin_reserva) VALUES
((SELECT MAX(id_reserva) as id_reserva FROM reserva), 101, 'Lionel', 'Messi', 45659875, '2024-12-01', '2024-12-10');
-- Lionel Messi en Flask Seasons Mar del Plata

-- 2 clientes

INSERT INTO servicio (nombre, descripcion) VALUES 
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