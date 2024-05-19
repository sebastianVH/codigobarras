import pyodbc

# Configura los detalles de la conexión

# Establece la conexión
def dbini():
    server = '192.168.9.12\ROJOSOFT'
    database = 'AGM'
    username = 'RO'
    password = 'rjsSA2528'
    driver = '{ODBC Driver 17 for SQL Server}'
    try:
        connection = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
        print("Conexión exitosa a SQL Server")

        cursor = connection.cursor()

        query = """SELECT 
	   A.Descripcion AS Articulo,
	   L.Numero AS [Nro. de Orden de Viaje],
	   FCO.SerieLote AS Lote,
	   L.FechaOrigen AS [Fecha de Origen],
       	   CL.Nombre AS Cliente,
           FCO.Cantidad
  FROM LOGISTICA AS L
  LEFT OUTER JOIN CLIENTE AS VEN ON VEN.Cuenta = L.ClienteVendedor 
  LEFT OUTER JOIN FACTURA AS FO ON FO.Logistica = L.IDTabla
  LEFT OUTER JOIN FACTURACUERPO AS FCO ON FCO.Factura = FO.IDTabla
  LEFT OUTER JOIN DEPOSITO AS DP ON DP.IDTabla=FCO.Deposito
  LEFT OUTER JOIN CLIENTE AS CL ON CL.Cuenta = FO.Cliente
  LEFT OUTER JOIN ARTICULOPRECIO AS AP ON AP.IdTabla = FCO.ArticuloPrecio
  LEFT OUTER JOIN ARTICULO AS A ON A.Codigo = AP.Articulo
  LEFT OUTER JOIN CLIENTE AS CT ON CT.Cuenta = L.ClienteTransportista
  LEFT OUTER JOIN COMPROBANTE AS CO ON CO.Codigo = L.Comprobante
  LEFT OUTER JOIN LUGAR As LE On LE.Codigo = FO.LugarEntrega And LE.Planta = FO.Planta  
  LEFT OUTER JOIN LOCALIDAD As LDE On LDE.Codigo = LE.Localidad  
  LEFT OUTER JOIN PROVINCIA As PD On PD.Codigo = LDE.Provincia  
 WHERE L.FechaOrigen>=  CONVERT(date, GETDATE()-3,103) AND FO.Estado<>'AN'
 order by L.Numero, CL.Nombre, A.Descripcion, DP.Descripcion         
        """

        cursor.execute(query)

        rows = cursor.fetchall()
        cursor.close()

        print("Se han recuperado", len(rows), "filas")
        connection.close()

        return rows

    except Exception as e:
        print("Error al conectar a SQL Server", e)

def construir_diccionario(rows):
    diccionario = {}
    
    for row in rows:
        nro_orden = row[1]
        lote = row[2]
        
        if nro_orden not in diccionario:
            diccionario[nro_orden] = []
        
        diccionario[nro_orden].append(lote)
    
    return diccionario