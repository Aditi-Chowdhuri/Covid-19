//API to fetch historical data of Bitcoin Price Index for four months
const api = '/confirm';

/**
 * Loading data from API when DOM Content has been loaded'.
 */
//event listener which gets fired once the DOM is loaded
document.addEventListener("DOMContentLoaded", function(event) {
fetch(api) // fetch data from api and convert in the form suitable to create line chart
    .then(function(response) { return response.json(); })
    .then(function(data) {
        var parsedData = parseData(data); //this function creates array of objects that contains date and price pf bitcoin on that particular date
        drawChart(parsedData); //function responsible to create our line chart after data is parsed
    })
    .catch(function(err) { console.log(err); })
});

/**
 * Parse data into key-value pairs
 * @param {object} data Object containing historical data of BPI
 */
//this function creates array of objects that contains date and price pf bitcoin on that particular date
function parseData(data) {
    var arr = [];
    for (var i in data.confirmed) {
        arr.push({
            date: new Date(i), //date
            value: +data.confirmed[i] //convert string to number
        });
    }
    return arr;
}

/**
 * Creates a chart using D3
 * @param {object} data Object containing historical data of BPI
 */
//getting dataset in the parameter
function drawChart(data) {
var svgWidth = 800, svgHeight = 500;
var margin = { top: 20, right: 30, bottom: 30, left: 70 };
var width = svgWidth - margin.left - margin.right; // width of the chart
var height = svgHeight - margin.top - margin.bottom; // height of the chart

//select svg element
var svg = d3.select('svg')
    .attr("width", svgWidth)
    .attr("height", svgHeight);
 
//append a group inside our svg element
var g = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// time on x axis
var x = d3.scaleTime()
    .rangeRound([0, width]);

// price of bitcoin on y axis
var y = d3.scaleLinear()
    .rangeRound([height, 0]);

//create the line chart
var line = d3.line()
    .x(function(d) { return x(d.date)})
    .y(function(d) { return y(d.value)})
    x.domain(d3.extent(data, function(d) { return d.date }));// to know scope of the data when it is passed through scale function
    y.domain(d3.extent(data, function(d) { return d.value }));// .extent() ultimately returns minimum and maximum value

g.append("g")// append group element inside our parent group
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x))
    .append("text")
    .attr("fill", "#000")
    .select(".domain")
    .remove();

g.append("g")
    .call(d3.axisLeft(y))
    .append("text")
    .attr("fill", "#000")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", "0.71em")
    .attr("text-anchor", "end")
    .text("Number of Cases");

g.append("path")//line we see in the line chart
    .datum(data)// call method .datum() and pass our dataset
    .attr("fill", "none")
    .attr("stroke", "red")
    .attr("stroke-linejoin", "round")
    .attr("stroke-linecap", "round")
    .attr("stroke-width", 1.5)
    .attr("d", line);// create a line function for the d attribute
}

