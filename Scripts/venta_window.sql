USE [PetlandDb]
GO

/****** Object:  Table [dbo].[Venta]    Script Date: 06/10/2024 16:35:23 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Venta](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[id_articulo] [int] NULL,
	[cantidad] [int] NULL,
	[fecha] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Venta] ADD  DEFAULT (getdate()) FOR [fecha]
GO

ALTER TABLE [dbo].[Venta]  WITH CHECK ADD FOREIGN KEY([id_articulo])
REFERENCES [dbo].[Articulo] ([id])
GO


