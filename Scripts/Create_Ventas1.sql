CREATE TABLE Venta (
    id INT PRIMARY KEY IDENTITY(1,1),
    id_articulo INT,
    cantidad INT,
    fecha DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (id_articulo) REFERENCES Articulo(id)
);
