import puppeteer from "puppeteer";
import ExcelJS from "exceljs"
import fs from "fs"
import { Http2ServerRequest } from "http2";
// import parse from 'date-fns';
// const {parse} = require ("date-fns")
import { parse,format } from 'date-fns'


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

function otraFuncionMas(fechaHTML) {
    // Define el mapeo de nombres de meses a abreviaturas en inglés
    const meses = {
      ENERO: 'Jan',
      FEBRERO: 'Feb',
      MARZO: 'Mar',
      ABRIL: 'Apr',
      MAYO: 'May',
      JUNIO: 'Jun',
      JULIO: 'Jul',
      AGOSTO: 'Aug',
      SEPTIEMBRE: 'Sep',
      OCTUBRE: 'Oct',
      NOVIEMBRE: 'Nov',
      DICIEMBRE: 'Dec'
    };
    // Reemplaza el nombre del mes con la abreviatura en inglés
    const fechaHTMLAbreviada = fechaHTML.replace(
      /(?:ENERO|FEBRERO|MARZO|ABRIL|MAYO|JUNIO|JULIO|AGOSTO|SEPTIEMBRE|OCTUBRE|NOVIEMBRE|DICIEMBRE)/g,
      (match) => meses[match]
    );
    // Define el formato de entrada
    const formatoEntrada = 'dd MMMM yyyy';
    const fecha = parse(fechaHTMLAbreviada, formatoEntrada, new Date());
    const formatDate = format(fecha,'dd/MM/yyyy');
    return formatDate;
}

// Ejemplo de uso de la función
// const fechaHTML = '22 FEBRERO 2011';
// const fecha = parseFechaHTML(fechaHTML);
// console.log("La fecha es: ",fecha," es de tipo: ",typeof fecha);
// const fechaActual = new Date().toLocaleDateString();
// console.log(typeof fechaActual)

async function dataT(URLelement){
    const browser = await puppeteer.launch({
    headless:'false',
    slowMo:400
    })
    const page = await browser.newPage()   
    await page.setDefaultNavigationTimeout(0)
    //Recorremos
    const arrgURL = [
    "https://www.servir.gob.pe/tribunal-sc/resoluciones-de-salas/primera-sala/resoluciones-2011-enero/"
    // "https://www.servir.gob.pe/tribunal-sc/resoluciones-de-salas/primera-sala/resoluciones-2011-febrero/",
    // "https://www.servir.gob.pe/tribunal-sc/resoluciones-de-salas/primera-sala/resoluciones-2011-marzo/"
    ];
    const allTableData = [];
    for (const URL of arrgURL) {
        console.log("Estamos entrando a ", URL)
        await page.goto(URL);
        await page.waitForSelector('tr');
        const tableData = await page.evaluate(() => {
            const rows = Array.from(document.querySelectorAll('tr')).slice(1);
            const result = [];
            let sessionArray = [];
            let sessionDateArray = [];
            const fechaActual = new Date().toLocaleDateString();
            rows.forEach((row) => {
                const columns = row.querySelectorAll('td');
                const header = row.querySelector('th');
                if (header) {
                    const session = header.innerText;
                    sessionArray.push(session);
                    const dateSS = header.querySelector('b').innerText;
                    const dateF = otraFuncionMas('22 FEBRERO 2011');
                    sessionDateArray.push(dateF)
                }
                if (columns.length === 3) {
                    const nombre = columns[0].querySelector('a').innerText;
                    const href = columns[0].querySelector('a').getAttribute('href');
                    const entidad = columns[2].innerText;
                    const resolucion = columns[1].innerText;
                    const valorSession = sessionArray.length > 0 ? sessionArray[sessionArray.length - 1] : '';
                    const dateSession = sessionDateArray.length > 0 ? sessionDateArray[sessionDateArray.length - 1] : '';
                    result.push([fechaActual, nombre, href, resolucion, entidad, valorSession,dateSession]);
                }
            });
            return result;
        });
        allTableData.push(...tableData);
    }
    // Realiza todas las solicitudes web y extracción de datos en paralelo
    // await Promise.all(arrgURL.map(URL => getDataFromURL(URL)));
    await browser.close();
    // Ordena los datos por un criterio, por ejemplo, la fecha
    // allTableData.sort((a, b) => a[0].localeCompare(b[0])); 
    // Crear un archivo CSV usando exceljs y guardar los datos
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('Table');
    worksheet.addRow(['FechaExtraccion', 'Nombre', 'URL', 'Resolución', 'Entidad', 'Session','Fecha']);
    allTableData.forEach((row) => {
        worksheet.addRow(row);
    });
    // const fileName = URL.split('/').pop() + '.csv';
    const fileName = 'DataTable.csv';
    await workbook.csv.writeFile(fileName);
    console.log(`Datos guardados en ${fileName}`);
}

dataT();

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


