function loadProducts(categoryId) {
    fetch(`/products/${categoryId}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        const productList = document.getElementById('product-list');
        productList.innerHTML = ''; // Limpiar lista anterior
        data.forEach(product => {
            const li = document.createElement('li');
            li.textContent = product.nombre;
            productList.appendChild(li);
        });
    })
    .catch(error => console.error('Error:', error));
}

async function searchProducts(query, tableId) {
    // if (query) {
    //     fetch(`/search?${query}`)
    //     .then(response =>  {
    //         console.log(response.htmlresponse)
    //         // if (data) {
    //         //     $(`#${tableId} tbody`).html("");
    //         //     let miData = response.data;
    //         //     $(`#${tableId} tbody`).append(miData);
    //         // }else {
    //         //     $(`#${tableId} tbody`).html("");
    //         //     $(`#${tableId} tbody`).html(`
    //         //     <tr>
    //         //     <td colspan="6" style="text-align:center;color: red;font-weight: bold;">No hay resultados para la busqueda.</td>
    //         //     </tr>`);
    //         //     return false;
    //         // }

    //         // const productList = document.getElementById('product-list');
    //         // productList.innerHTML = ''; // Limpiar lista anterior
    //         // data.forEach(product => {
    //         //     console.log(product)
    //         //     const li = document.createElement('li');
    //         //     li.textContent = product.nombre;
    //         //     productList.appendChild(li);
    //         // });
    //     })
    //     .catch(error => console.error('Error:', error));
    // } else {
    //     // Si la barra de búsqueda está vacía, limpia la lista
    //     //document.getElementById('product-list').innerHTML = '';
    //     console.log("No llegó el query")
    // }
    const headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      };
    try {
        // Axios: Envía solicitudes HTTP mediante promesas en JS
        console.log(query)
        const response = await axios.get(`/search?${query}`);
        if (!response.status) {
          console.log(`HTTP error! status: ${response.status} 😭`);
        }
        console.log(response)
        if (response.data.fin === 0) {
          $(`#${tableId} tbody`).html("");
          $(`#${tableId} tbody`).html(`
          <tr>
            <td colspan="6" style="text-align:center;color: red;font-weight: bold;">No hay resultados para la busqueda: <strong style="text-align:center;color: #222;">${fecha_desde} - ${fecha_hasta}</strong></td>
          </tr>`);
          return false;
        }
        console.log(tableId)
        if (response.data) {
          $(`#${tableId} tbody`).html("");
          let miData = response.data;
          $(`#${tableId} tbody`).append(miData);
        }
      } catch (error) {
        console.error(error);
      }
}

async function buscadorTableMedicion(tableId) {
  let nombre,categoria_id, marca_id, precio_min, precio_max, url;
  url = "/product";
  nombre = document.getElementById("search_text").value
  categoria_id = document.getElementById("search_filter_category").value
  marca_id = document.getElementById("search_filter_brand").value
  precio_min = document.getElementById("search_text_min").value
  precio_max = document.getElementById("search_text_max").value
  console.log(nombre,categoria_id, marca_id, precio_min, precio_max)
  let query=""
  if(nombre != "") query +=`nombre=${nombre}&`
  if(categoria_id != "") query +=`categoria_id=${categoria_id}&`
  if(marca_id != "") query +=`marca_id=${marca_id}&`
  if(precio_min != "") query +=`precio_min=${precio_min}&`
  if(precio_max != "") query +=`precio_max=${precio_max}&`
  console.log(query)
  //searchProducts(query, tableId)

  try {
    // Axios: Envía solicitudes HTTP mediante promesas en JS
    console.log(query)
    const response = await axios.get(`/search?${query}`);
    if (!response.status) {
      console.log(`HTTP error! status: ${response.status} 😭`);
    }
    console.log(response)
    console.log(tableId)
    if (response.data) {
      $(`#${tableId} tbody`).html("");
      let miData = response.data;
      $(`#${tableId} tbody`).append(miData);
    } else {
      $(`#${tableId} tbody`).html("");
      $(`#${tableId} tbody`).html(`
      <tr>
        <td colspan="6" style="text-align:center;color: red;font-weight: bold;">No hay resultados para la busqueda: <strong style="text-align:center;color: #222;">${fecha_desde} - ${fecha_hasta}</strong></td>
      </tr>`);
      return false;
    }
  } catch (error) {
    console.error(error);
  }

}
async function buscar(tableId){
    console.log("tableId",tableId)
    buscadorTableMedicion(tableId);
  }