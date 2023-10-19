import puppeteer from "puppeteer";
import ExcelJS from "exceljs"
import fs from "fs"
import { Http2ServerRequest } from "http2";

function leerArchivoYObtenerUrls(callback) {
  const filePath = 'urlServiceR';
  fs.readFile(filePath, 'utf-8', (err, data) => {
    if (err) {
      console.error('Error al leer el archivo:', err);
      callback([]); // Llama al callback con un array vacío en caso de error
      return;
    }
    const lines = data.split('\n').map(line => line.trim()).filter(Boolean);
    const urlServices = [];
    lines.forEach((line) => {
      urlServices.push(line);
    });
    callback(urlServices); // Llama al callback con el array resultante
  });
}
async function dataT(URLelement){
    const browser = await puppeteer.launch({
    headless:'false',
    slowMo:400
    })
    const page = await browser.newPage()   
    await page.setDefaultNavigationTimeout(0)
    //Recorremos
    let arrgURL = ["https://www.servir.gob.pe/tribunal-sc/resoluciones-de-salas/primera-sala/resoluciones-2011-enero/","https://www.servir.gob.pe/tribunal-sc/resoluciones-de-salas/primera-sala/resoluciones-2011-febrero/","https://www.servir.gob.pe/tribunal-sc/resoluciones-de-salas/primera-sala/resoluciones-2011-marzo/"]
    arrgURL.forEach(elemento =>{
        console.log(elemento);
    });
    await page.goto(URLelement)
    await page.waitForSelector('tr');
    const tableData = await page.evaluate(() => { 
        const rows = Array.from(document.querySelectorAll('tr')).slice(1)
        const result = [];
        let sessionArray = [];
        const fechaActual = new Date().toLocaleDateString();; // Obtiene la fecha y hora actuales
        rows.forEach((row) => {
            const columns = row.querySelectorAll('td');            
            const header = row.querySelector('th');
            let rowContent = row.innerHTML;
            if (header){
                const session = header.innerText;
                sessionArray.push(session);
            }
            // const session = header ? header.innerText : '';
            if (columns.length === 3) {
                const nombre = columns[0].querySelector('a').innerText;
                const href = columns[0].querySelector('a').getAttribute('href');
                const entidad = columns[2].innerText;
                const resolucion = columns[1].innerText;
                const valorSession = sessionArray.length > 0 ? sessionArray[sessionArray.length - 1] : '';
                result.push([fechaActual,nombre,href,resolucion,entidad,valorSession]);
            }
        });
        return result;
    });
    await browser.close();
    //Save data
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('Table');
    worksheet.addRow(['FechaExtraccion','Resolución','URL','Nombre','Entidad','Session']);
    tableData.forEach((row) => {
      worksheet.addRow(row);
    });
    await workbook.csv.writeFile('tabla.csv');
    console.log('Datos guardados en tabla.csv');
}

// dataT();

const TestOne = parametro => {
    let arrgURL = ["https://www.servir.gob.pe/tribunal-sc/resoluciones-de-salas/primera-sala/resoluciones-2011-enero/","https://www.servir.gob.pe/tribunal-sc/resoluciones-de-salas/primera-sala/resoluciones-2011-febrero/","https://www.servir.gob.pe/tribunal-sc/resoluciones-de-salas/primera-sala/resoluciones-2011-marzo/"]
    arrgURL.forEach(elemento =>{
        console.log(elemento);
    });
};

// TestOne('Hola, mundo');


// leerArchivoYObtenerUrls((urlServices) => {
// //   console.log('Array de URL services:', urlServices);
//     urlServices.forEach(element => {
//         // console.log(element);       
//     });
// });



