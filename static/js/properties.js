'use strict;'
// alert('properties.js is loaded');
//generate one color for each property different shades of pink
function randomizeColors(arrayLength) {
    const r = Math.floor(213 + (Math.random() * 35));
    const g = Math.floor(172 + (Math.random() * 5));
    const b = Math.floor(196 + (Math.random() * 20));
    const a = 1;
    const rgba = `rgba(${r}, ${g}, ${b}, ${a})`;
    return rgba
}
// 'rgba(213, 172, 196, 1)'
function compareProperties(event) {
    // get property ID from user clicked on checkboxes
    let cb = document.querySelectorAll('input[name="checked-property"]:checked');
    let values = [];
    cb.forEach((checkbox) => {
        let propertyId = values.push(parseInt(checkbox.value));
    });
    // query data of the properties by their ID from the database
    const propertyIds = {
        'propertyIds': values
    }

    fetch('/compare-properties.json', {
            method: 'POST',
            body: JSON.stringify(propertyIds),
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then((response) => response.json())
        .then((responseJson) => {
            // console.log(Object.keys(responseJson).length);
            console.log(responseJson);
            // let chartData = responseJson;
            // console.log(typeof chartData);
            let labels = ['Rent', 'Mortgage', 'Tax', 'Insurance', 'HOA', 'CapEx', 'PM', 'Utilities', 'Vacancy', 'Maintenance'];
            let datasets = [];



            for (let property of responseJson) {
                let dataset = {}
                // const colorArray = randomizeColors(labels.length);
                const color = randomizeColors();
                dataset.backgroundColor = color;
                console.log(color);
                dataset.borderColor = color;
                dataset.borderWidth = 1;
                dataset.label = `Property ID: ${property.id}`;
                let data = [property.rent, property.mortgage, property.tax, property.insurance, property.hoa, property.capex, property.pm, property.utilities, property.vacancy, property.maintenance]
                dataset.data = data;
                datasets.push(dataset);

            }

            new Chart(document.querySelector('#compare_bar'), {
                type: 'bar',
                data: {
                    labels,
                    datasets,

                },
                options: {
                    plugins: {
                        title: {
                            display: true,
                            text: 'Property Comparison'
                        },
                    },
                    responsive: true,
                    scales: {
                        x: {
                            stacked: true,
                        },
                        y: {
                            stacked: true
                        }
                    }
                }
            });
        });


}





const compareBtn = document.querySelector('#compare-btn')
compareBtn.addEventListener('click', compareProperties);