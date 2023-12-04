function scrollWin(x) {
  window.scrollTo({
    top: 1000 + x,
    left: 1000,
    behavior: "smooth",
  });
}

function addRow() {
  var table = document.getElementById("myTable");
  var row = table.insertRow(-1);
  var rowCount = table.rows.length;
  var cell1 = row.insertCell(0);
  cell1.contentEditable = true;
  cell1.innerHTML = "<th>Тема " + (rowCount - 1) + "</th>";

  for (var i = 1; i < table.rows[0].cells.length; i++) {
      var cell = row.insertCell(i);
      cell.innerHTML = '<div class="input-block" name="cell_' + rowCount + '_' + i + '">' +
          '<p contenteditable="true">--дата--</p>' +
          '<div class="dropdown">' +
          '<button class="dropbtn" onclick="toggleDropdown(this)">Color</button>' +
          '<div class="dropdown-content">' +
          '<a href="#" onclick="updateColor(this, \'green\', \'cell_' + rowCount + '_' + i + '\')">' +
          '<span class="color-circle green"></span>Green' +
          '</a>' +
          '<a href="#" onclick="updateColor(this, \'red\', \'cell_' + rowCount + '_' + i + '\')">' +
          '<span class="color-circle red"></span>Red' +
          '</a>' +
          '<a href="#" onclick="updateColor(this, \'yellow\', \'cell_' + rowCount + '_' + i + '\')">' +
          '<span class="color-circle yellow"></span>Yellow' +
          '</a>' +
          '</div>' +
          '</div></div>';
  }
}

function addColumn() {
  var table = document.getElementById("myTable");
  var columnCount = table.rows[0].cells.length;
  var headerRow = table.rows[0];
  var newHeaderCell = document.createElement("th");
  newHeaderCell.innerHTML = "";
  headerRow.appendChild(newHeaderCell);

  for (var i = 1; i < table.rows.length; i++) {
      var row = table.rows[i];
      var cell = row.insertCell(-1);
      cell.innerHTML = '<div class="input-block" name="cell_' + i + '_' + columnCount + '">' +
          '<p contenteditable="true">--дата--</p>' +
          '<div class="dropdown">' +
          '<button class="dropbtn" onclick="toggleDropdown(this)">Color</button>' +
          '<div class="dropdown-content">' +
          '<a href="#" onclick="updateColor(this, \'green\', \'cell_' + i + '_' + columnCount + '\')">' +
          '<span class="color-circle green"></span>Green' +
          '</a>' +
          '<a href="#" onclick="updateColor(this, \'red\', \'cell_' + i + '_' + columnCount + '\')">' +
          '<span class="color-circle red"></span>Red' +
          '</a>' +
          '<a href="#" onclick="updateColor(this, \'yellow\', \'cell_' + i + '_' + columnCount + '\')">' +
          '<span class="color-circle yellow"></span>Yellow' +
          '</a>' +
          '</div>' +
          '</div></div>';
  }
}

function toggleDropdown(button) {
  button.parentElement.querySelector(".dropdown-content").classList.toggle("show");
}

function updateColor(link, color, cellName) {
  var cell = document.querySelector('[name="' + cellName + '"]');
  cell.style.backgroundColor = color;
  toggleDropdown(link.parentElement.parentElement.parentElement.querySelector(".dropbtn"));
}

window.onclick = function(event) {
  if (!event.target.matches(".dropbtn")) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      for (var i = 0; i < dropdowns.length; i++) {
          var openDropdown = dropdowns[i];
          if (openDropdown.classList.contains("show")) {
              openDropdown.classList.remove("show");
          }
      }
  }
}

function saveTableData() {
    // Get the table HTML
    const tableHTML = document.getElementById('myTable').innerHTML;

    // Prepare the data to send to the server
    const data = {
        table_html: tableHTML,
        title: document.getElementById('tableTitle').innerText
    };

    // Send a POST request to save the table data
    fetch('/save_table_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            // Table data saved successfully
            console.log('Table data saved successfully');
        } else {
            // Error occurred while saving the table data
            console.error('Error saving table data');
        }
    })
    .catch(error => {
        console.error('Error saving table data:', error);
    });

    // Send a POST request to save the table title
    fetch('/save_table_title', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title: data.title })
    })
    .then(response => {
        if (response.ok) {
            // Table title saved successfully
            console.log('Table title saved successfully');
        } else {
            // Error occurred while saving the table title
            console.error('Error saving table title');
        }
    })
    .catch(error => {
        console.error('Error saving table title:', error);
    });
}
