from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Clientes"

headers = ["nombre", "celular", "placa"]
ws.append(headers)

datos = [
    ["Juan Perez", "3022475080", "ABC123"],
    ["Maria Gomez", "3022475080", "DEF456"],
    ["Carlos Lopez", "3022475080", "GHI789"],
    ["Ana Martinez", "3022475080", "JKL012"],
    ["Pedro Rodriguez", "3022475080", "MNO345"],
]

for dato in datos:
    ws.append(dato)

wb.save("clientes_ejemplo.xlsx")
print("Archivo creado: clientes_ejemplo.xlsx")