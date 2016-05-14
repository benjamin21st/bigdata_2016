/* globals $, d3 */

'use strict';

/**
 * Load total travel distance for different taxi types
 */
$.getJSON('/tripstats/dist/all', function (data) {
    $('#total-travel-distance').find('.data-yellow').text(data.yellow);
    $('#total-travel-distance').find('.data-green').text(data.green);
});

/**
 * Load average count by different tiem intervals for different
 * taxi types
 */
$.getJSON('/tripstats/count/all', function (data) {
    $('#average-trip-counts')
        .find('.interval-year .data-yellow').text(data.yellow.year);
    $('#average-trip-counts')
        .find('.interval-month .data-yellow').text(data.yellow.month);
    $('#average-trip-counts')
        .find('.interval-week .data-yellow').text(data.yellow.week);
    $('#average-trip-counts')
        .find('.interval-day .data-yellow').text(data.yellow.day);

    $('#average-trip-counts')
        .find('.interval-year .data-green').text(data.green.year);
    $('#average-trip-counts')
        .find('.interval-month .data-green').text(data.green.month);
    $('#average-trip-counts')
        .find('.interval-week .data-green').text(data.green.week);
    $('#average-trip-counts')
        .find('.interval-day .data-green').text(data.green.day);
});


/**
 * Load passenger counts by different taxi types and time intervals
 */
$.getJSON('/tripstats/passengers/all', function (data) {
    $('#passenger-counts')
        .find('.interval-year .data-yellow').text(data.yellow.year);
    $('#passenger-counts')
        .find('.interval-month .data-yellow').text(data.yellow.month);
    $('#passenger-counts')
        .find('.interval-week .data-yellow').text(data.yellow.week);
    $('#passenger-counts')
        .find('.interval-day .data-yellow').text(data.yellow.day);

    $('#passenger-counts')
        .find('.interval-year .data-green').text(data.green.year);
    $('#passenger-counts')
        .find('.interval-month .data-green').text(data.green.month);
    $('#passenger-counts')
        .find('.interval-week .data-green').text(data.green.week);
    $('#passenger-counts')
        .find('.interval-day .data-green').text(data.green.day);
});


/**
 * Load a simple d3 graph to show distribution of trips based
 * on month and weekday
 */
drawTripGraph('month');
drawTripGraph('weekday');

function drawTripGraph (type) {
    var COLOR_CODE = {
        1: "#B7D796",
        2: "#CA9A52"
    };
    // Set the dimensions of the canvas / graph
    var margin = {top: 30, right: 20, bottom: 30, left: 100},
        width = 600 - margin.left - margin.right,
        height = 270 - margin.top - margin.bottom;

    // Set the ranges
    var x = d3.scale.linear().range([0, width]);
    var y = d3.scale.linear().range([height, 0]);

    // Define the axes
    var dataset, selector, dataUrl;

    if (type === 'month') {
        dataset = {
            1: 'Jan',
            2: 'Feb',
            3: 'Mar',
            4: 'Apr',
            5: 'May',
            6: 'Jun',
            7: 'Jul',
            8: 'Aug',
            9: 'Sep',
            10:'Oct',
            11:'Nov',
            12:'Dec'
        };
        selector = "#trip-distribution-yellow";
        dataUrl = "/tripstats/distribution/yellow?interval=month";
    } else if (type === 'weekday') {
        dataset = {
            1: 'Mon',
            2: 'Tue',
            3: 'Wed',
            4: 'Thu',
            5: 'Fri',
            6: 'Sat',
            7: 'Sun'
        };
        selector = "#trip-distribution-weekday";
        dataUrl = "/tripstats/distribution/yellow?interval=week";
    }


    var xAxis = d3.svg.axis().scale(x)
        .tickFormat(function(d) {
            return dataset[d]; })
        .orient("bottom").ticks(5);

    var yAxis = d3.svg.axis().scale(y)
        .orient("left").ticks(5);

    // Define the line
    var valueline = d3.svg.line()
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.count); });


    // Adds the svg canvas
    var svg = d3.select(selector)
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform",
                  "translate(" + margin.left + "," + margin.top + ")");


    // Append a hover line
    // d3.select("#trip-distribution-yellow")
    //     .append("span")
    //         .attr("class", "hover-line");

    d3.select(selector)
        .on("mousemove", function () {
            $('.hover-line').css({
                'left': d3.event.offsetX + 10,
                'display': 'block'
            });
        })
        .on("mouseleave", function () {
            $('.hover-line').css({
                'display': 'none'
            });
        });

    // Get the data
    d3.json(dataUrl, function(error, data) {
        // data.forEach(function(d) {
        //     d.date = parseDate(d.date);
        // });

        // Scale the range of the data
        x.domain(d3.extent(data, function(d) { return d.date; }));
        y.domain([
            d3.min(data, function(d) { return d.count; }),
            d3.max(data, function(d) { return d.count; })
        ]);

        // Add the valueline path.
        svg.append("path")
            .attr("class", "line yellow-taxi")
            .attr("stroke", COLOR_CODE[2])
            .attr("d", valueline(data.filter(function (dpoint) {
                return dpoint.type === 2;
            })));

        svg.append("path")
            .attr("class", "line green-taxi")
            .attr("stroke", COLOR_CODE[1])
            .attr("d", valueline(data.filter(function (dpoint) {
                return dpoint.type === 1;
            })));


        // Add the tool tip
        d3.select(selector).append("span")
            .attr("id", "point-tool-tip")
            .attr("class", "point-tool-tip");

        svg.selectAll("dot")
            .data(data)
            .enter().append("circle")
                .attr("r", 5)
            .attr("cx", function(d) { return x(d.date); })
            .attr("cy", function(d) { return y(d.count); })
            .attr("fill", function (d) {
                return COLOR_CODE[d.type];
            })
            .on("mouseenter", function (d) {
                console.log(d);
                $(selector).find('.point-tool-tip').text(d.count).css({
                    "border": "1px solid #000",
                    "left": d3.event.offsetX + 10,
                    "top": d3.event.offsetY,
                    "padding": "5px",
                    "z-index": 99,
                    "background": COLOR_CODE[d.type]
                }).fadeIn();
            })
            .on("mouseleave", function () {
                $(selector).find('.point-tool-tip').fadeOut();
            });

        // Add the X Axis
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        // Add the Y Axis
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis);

    });
}

