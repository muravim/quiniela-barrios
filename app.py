function doGet(e) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName("Respuestas");
  var nombreConsulta = e.parameter.nombre;
  
  if (!nombreConsulta) return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": "Nombre requerido"}));

  var data = sheet.getDataRange().getValues();
  for (var i = 1; i < data.length; i++) {
    if (data[i][0].toString().trim().toLowerCase() === nombreConsulta.trim().toLowerCase()) {
      
      // Corrección automática: Si eres tú, fuerza el rol a Admin en la hoja
      var esAdmin = (data[i][0].toString().trim() === "Muravi Molina");
      if (esAdmin && data[i][18] !== "Admin") {
        sheet.getRange(i + 1, 19).setValue("Admin");
        data[i][18] = "Admin";
      }
      
      return ContentService.createTextOutput(JSON.stringify({
        "status": "success", 
        "datos": data[i],
        "es_admin": (data[i][18] === "Admin")
      })).setMimeType(ContentService.MimeType.JSON);
    }
  }
  return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": "Participante no encontrado"}));
}

function doPost(e) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName("Respuestas");
  var p = e.parameter;
  
  if (!p.nombre) return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": "Falta nombre"}));

  var esAdmin = (p.nombre.trim() === "Muravi Molina");
  var rol = esAdmin ? "Admin" : "Usuario";

  var data = sheet.getDataRange().getValues();
  var rowIndex = -1;
  
  for (var i = 1; i < data.length; i++) {
    if (data[i][0].toString().trim().toLowerCase() === p.nombre.trim().toLowerCase()) {
      if (data[i][16] === "Definitiva") return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": "Quiniela bloqueada"}));
      rowIndex = i + 1;
      break;
    }
  }
  
  if (rowIndex === -1) {
    sheet.appendRow([
      p.nombre, p.password, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "{}", "Pendiente", "En Edición", 0, rol
    ]);
  } else {
    var fila = [
      p.nombre, p.password, 
      p.grupo_a || data[rowIndex-1][2], p.grupo_b || data[rowIndex-1][3], 
      p.grupo_c || data[rowIndex-1][4], p.grupo_d || data[rowIndex-1][5], 
      p.grupo_e || data[rowIndex-1][6], p.grupo_f || data[rowIndex-1][7], 
      p.grupo_g || data[rowIndex-1][8], p.grupo_h || data[rowIndex-1][9], 
      p.grupo_i || data[rowIndex-1][10], p.grupo_j || data[rowIndex-1][11], 
      p.grupo_k || data[rowIndex-1][12], p.grupo_l || data[rowIndex-1][13], 
      p.octavos || data[rowIndex-1][14], p.campeon || data[rowIndex-1][15], 
      p.estado || data[rowIndex-1][16], 0, rol
    ];
    sheet.getRange(rowIndex, 1, 1, fila.length).setValues([fila]);
  }
  
  return ContentService.createTextOutput(JSON.stringify({"status": "success", "message": "Procesado"}));
}
