ALTER TABLE Venta
ADD metodo_pago VARCHAR(50),  -- Nuevo campo para el método de pago
    cliente_id INT;           -- Nuevo campo para el ID del cliente

ALTER TABLE Venta
ADD total DECIMAL(10, 2);  -- Ajusta el tipo de dato según tu necesidad
