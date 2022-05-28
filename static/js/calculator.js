'use strict';

//user inputs in index.html posted to server.py to do some calculation, js to show results via fetch ajax
// get user input directly from HTML to JS
// alert('map and chart js is loaded!')
//generate one color for each property different shades of pink

// 'rgba(213, 172, 196, 1)'
const backgroundColor = [
  'rgba(213, 172, 196, 1)',
  'rgba(235, 216, 224, 1)',
  'rgba(255, 200, 215, 1)',
  'rgba(255, 207, 220, 1)',
  'rgba(249, 215, 214, 1)',
  'rgba(239, 207, 212, 1)',
  'rgba(245, 220, 224, 1)',
  'rgba(255, 214, 225, 1)',
  'rgba(236, 189, 196, 1)'
]
const borderColor = 'rgba(213, 172, 196, 1)'

function runNumbers(event) {
  document.querySelector('#hidden').style.backgroundImage = "url('/static/white.jpg')";
  const calForm = document.querySelector('#calform');
  const data = new FormData(calForm);
  const rent = parseInt(data.get('rent'));
  console.log(rent);
  const mortgage = parseInt(data.get('mortgage'));
  const tax = parseInt(data.get('tax'));
  const insurance = parseInt(data.get('insurance'));
  const hoa = parseInt(data.get('hoa'));
  const utilities = parseInt(data.get('utilities'));
  const maintenance = parseInt(data.get('maintenance'));
  const pm = parseInt(data.get('pm'));
  const vacancy = parseInt(data.get('vacancy'));
  const capex = parseInt(data.get('capex'));
  let total_expenses = (mortgage + tax + insurance + hoa + utilities + maintenance + pm + vacancy + capex)
  let cashflow = rent - total_expenses
  let annual_cashflow = 12 * cashflow
  console.log(total_expenses);
  document.querySelector('#result-cash-flow').innerHTML = `<h1>$${cashflow}.00</h1>`;
  if (cashflow < 0) {
    document.querySelector('#cashflow-row').style.backgroundColor = '#d5acc4';
  } else {
    document.querySelector('#cashflow-row').style.backgroundColor = '#739bc5';
  };
  document.querySelector('#total-expenses').value = total_expenses;
  document.querySelector('#annual').value = annual_cashflow;
  // data for charts
  const cmortgage = Number(document.querySelector('#mortgage').value)
  const ctax = Number(document.querySelector('#tax').value)
  const cinsurance = Number(document.querySelector('#insurance').value)
  const choa = Number(document.querySelector('#hoa').value)
  const cutilities = Number(document.querySelector('#utilities').value)
  const cmaintenance = Number(document.querySelector('#maintenance').value)
  const cpm = Number(document.querySelector('#pm').value)
  const cvacancy = Number(document.querySelector('#vacancy').value)
  const ccapex = Number(document.querySelector('#capex').value)
  console.log(` this is chart data 0 ${ctax}`);
  const chartData = [cmortgage, ctax, cinsurance, choa, cutilities, cmaintenance, cpm, cvacancy, ccapex]
  console.log(` this is chart data 0 ${chartData}`);


  //have a nice image on the homepage as placeholder, as user click on run numbers, image turns into charts!!!
  // chart num 1
  new Chart(document.querySelector('#pieChart'), {
    type: 'doughnut',
    data: {
      labels: ['Mortgage', 'Tax', 'Insurance', 'HOA', 'Utilities', 'Maintenance', 'PM', 'Vacancy', 'CapEx'],
      datasets: [{
        label: 'Monthly Expenses',
        data: chartData,
        backgroundColor,
        borderColor,
        borderWidth: 2
      }]

    },
    // percentage below

    // percentage above
  });
  // chart num 2
  // new Chart(document.querySelector('#lineChart'), {
  //   type: 'line',
  //   data: {
  //     labels: ['Mortgage', 'Tax', 'Insurance', 'HOA', 'Utilities', 'Maintenance', 'PM', 'Vacancy', 'CapEx'],
  //           datasets: [{
  //               label: 'Monthly Expenses',
  //               data: chartData,
  //               backgroundColor,
  //               borderColor,
  //               borderWidth: 1
  //           }]

  //   },

  //   });
  // chart num 3
  new Chart(document.querySelector('#barChart'), {
    type: 'bar',
    data: {
      labels: ['Mortgage', 'Tax', 'Insurance', 'HOA', 'Utilities', 'Maintenance', 'PM', 'Vacancy', 'CapEx'],
      datasets: [{
        label: 'Monthly Expenses',
        data: chartData,
        backgroundColor,
        borderColor,
        borderWidth: 2
      }]


    },


  });
  // chart num 4
  // new Chart(document.querySelector('#donutChart'), {
  //   type: 'doughnut',
  //   data: {
  //     labels: ['Mortgage', 'Tax', 'Insurance', 'HOA', 'Utilities', 'Maintenance', 'PM', 'Vacancy', 'CapEx'],
  //           datasets: [{
  //               label: 'Monthly Expenses',
  //               data: chartData,
  //               backgroundColor,
  //               borderColor,
  //               borderWidth: 1
  //           }]




  //   },

  //   });
  // inside function
}
const form = document.querySelector('#run-numbers');
form.addEventListener('click', runNumbers);