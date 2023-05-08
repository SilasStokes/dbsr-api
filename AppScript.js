
/**
 * This file is mirrors the script that is rad in the google sheet that houses the database. 
 * It calls the api developed in app when someone at dbsr makes an update. 
 */

function myFunction(e = {
    "authMode": "FULL", 
    "oldValue": "From Water to Horse row # 2", 
    "range": {
        "columnEnd": 2, 
        "columnStart": 2, 
        "rowEnd": 2, 
        "rowStart": 2
    }, 
    "source": {}, 
    "triggerUid": "15362436", 
    "user": {
        "email": "daybreakstarradio@gmail.com", 
        "nickname": "daybreakstarradio"
    }, 
    "value": "From Water to Horse row # 2 edit again"
}) {
  const ngrok_url = 'https://3e8c-71-227-227-56.ngrok-free.app'
  const api_endpoint = '/test'
  const full_url = `${ngrok_url}${api_endpoint}`
  if ( e === undefined){
    console.log('e undefined, returning...')
    return
  }

  // Logger.log(`row start: ${e.range.rowStart} typeof: ${typeof e.range.rowStart}`)
  console.log(e)
  let ss = SpreadsheetApp.getActiveSheet()
  // let sheetname = ss.getSheetName()
  let headers = ss.getRange("1:1").getValues()[0] // returns
  
  Logger.log(`headers: ${headers}, typeof: ${typeof headers} length : ${headers.length}`)
  
  var range = ss.getRange(e["range"]["rowStart"], 1, e["range"]["rowStart"], headers.length)
  var values = range.getValues()[0];

  var event = {
    oldVal: e.oldValue,
    newVal: e.value,
    changedCol : headers[e.range.columnStart],
  }
  var row = {}

  for( let i = 0; i < headers.length; i ++) {
    if (!headers[i]) break 
    row[headers[i]] = values[i]

  }
  event['row'] = row
  
  // Logger.log(`values: ${values}`)



  var options = {
    'method' : 'POST',
    'contentType': 'application/json',
    'payload' : JSON.stringify(event)
  }


  UrlFetchApp.fetch(full_url, options);

}
