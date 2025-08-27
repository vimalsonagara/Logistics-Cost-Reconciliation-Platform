document.getElementById('upload-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  const formData = new FormData();
  formData.append('total_cost', document.getElementById('total_cost').value);
  formData.append('file', document.getElementById('excel_file').files[0]);

  try {
    //     for (let [key, value] of formData.entries()) {
    //   console.log(key, value);
    // }
       const response = await fetch('/upload/', {
            method: 'POST',
            body: formData  
          });
    
    if (!response.ok) 
    {
      const errText = await response.text(); 
      throw new Error(errText);
    }

    const data = await response.json();
    // console.log(data)
    document.getElementById('response').innerHTML = formatResponse(data);
  } catch (error) {
    document.getElementById('response').innerText = 'Error: ' + error.message;
  }
});

function formatResponse(data) {
  let html = `<h3>Result</h3>`;
  html += `<strong>Total Cost:</strong> ${data.total_cost}<br>`;
  html += `<strong>Total Load:</strong> ${data.total_load}<br>`;
  html += `<h4>Company Costs:</h4><ul>`;
  for (const [company, cost] of Object.entries(data.company_costs)) {
    html += `<li>${company}: ${cost}</li>`;
  }
  html += `</ul>`;

  const opt = data.Optimization;
  html += `<h4>Optimization Summary:</h4>`;
  html += `Total Capacity: ${opt.total_capacity}<br>`;
  html += `Used Trucks: ${opt.used_trucks}<br>`;
  html += `Utilization: ${opt.utilization_percent}%<br>`;
  html += `Unused Capacity: ${opt.unused_capacity}<br>`;

  html += `<h4>Assignments (${opt.assignments.length}):</h4><table><tr><th>Original Truck</th><th>Assigned Load</th><th>Placed In</th><th>Company</th></tr>`;
  opt.assignments.forEach(a => {
    html += `<tr><td>${a.original_truck}</td><td>${a.assigned_load}</td><td>${a.placed_in}</td><td>${a.company}</td></tr>`;
  });
  html += `</table>`;

  html += `<h4>Bins (${opt.bins.length}):</h4><table><tr><th>Truck ID</th><th>Company</th><th>Capacity</th><th>Allocated</th><th>Remaining</th></tr>`;
  opt.bins.forEach(b => {
    html += `<tr><td>${b.truck_id}</td><td>${b.company}</td><td>${b.capacity}</td><td>${b.allocated}</td><td>${b.remaining}</td></tr>`;
  });
  html += `</table>`;

  return html;
}
