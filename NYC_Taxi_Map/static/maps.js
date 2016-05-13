//global AllData: false, GreenData: false, YellowData: false, DropOffData:false, PickUpData:false d3: false  
"use strict";


function findmax(data)
{
    var maxnum = 0
    for (var key in data){
        if(maxnum < data[key])
            maxnum = data[key]
    }
    return maxnum
}
//loading up different datasets, default color and max domain value
var dataSets = {
	"alldata": {
		"data": AllData,
		"color": "YlGnBu",
		"maxDomain": findmax(AllData)*0.4
	},
	"green": {
		"data": GreenData,
		"color": "Greens",
		"maxDomain": findmax(GreenData)*0.4
	},
	"yellow": {
		"data": YellowData,
		"color": "Oranges",
		"maxDomain": findmax(YellowData)*0.4
	},
	"dropoff": {
		"data": DropOffData,
		"color": "YlOrBr",
		"maxDomain": findmax(DropOffData)*0.4
	},
	"pickup": {
		"data": PickUpData,
		"color": "Purples",
		"maxDomain": findmax(PickUpData)*0.4
	},
};

//set up map
var w = screen.width;
var h = screen.height;

//default dataset to load
var currentData = dataSets.alldata;
var svg;
var zips;
var time;

//legend settings
var dataLegendMax = currentData.maxDomain;
var legendWidth = 20;
var legendHeight = 20;
var legendSteps = 12;

//map type & center point 
var projection = d3.geo.mercator()
    //.center([-73.9871, 40.9537])
	.center([-74.000816, 40.752898])
    //.scale(101843);
    .scale(181843);

var path = d3.geo.path().projection(projection);

//set up a qX-9 number to associate with colorbrew.css styles
var setColor = d3.scale.quantize()
    .domain([0, currentData.maxDomain])
    .range(d3.range(9).map(function(i) { return "q" + (i) + "-9"; }));


var initializeSVG = function () {
	svg = d3.select("#d3_map")
		.append("svg")
		.attr("class", "YlGnBu")
		.attr("width", w)
		.attr("height", h);
};


var createMap = function (zipcodes) {
	svg.remove();
	initializeSVG();
	svg.append("g")
		.selectAll("path")
		.data(zipcodes.features)
		.enter()
		.append("path")
		.attr('name', function(d) { return d.properties.name })
		.attr("title", function(d) { return d.id; })
		.attr("class", function(d) { return zipcodeColor(d.id, currentData.data); } )
		.attr("stroke", "#fff")
		.on("mouseover", mouseover)
		.on("mouseout", mouseout)
		.on("click", clickEvent)

		.attr("d", path);

	//scaleExtent is the max and min of zoom level
	svg.call(d3.behavior.zoom().scaleExtent([1/2, 8]).on("zoom", zoom));

	createLegend();
};


//map number of complaint to color intensity
var zipcodeColor = function(zip, data) {
	if(zip in data){
		return setColor(data[zip]);
	}else{
		//no data
		return "white";
	}
};


var createLegend = function () {

	var step = dataLegendMax / legendSteps;
	var legendRange = [];

	for (var k = 0 ; k < legendSteps ; k++) {
		legendRange.push (Math.floor(k * step));
	}
    /*
    var step = Math.log(dataLegendMax)-1;
    var legendRange = [];
    var ra = 10;
    while(ra < dataLegendMax)
    {
        legendRange.push(ra)
        ra = ra * 10;
    }   
*/
	var legend = svg.selectAll("g.legend")
		.data(legendRange)
		.enter().append("g")
		.attr("class", "legend");

	legend.append("rect")
		.attr("x", 20)
		.attr("y", function(d, i){ return h/4 - (i*legendHeight) - 2*legendHeight; })
		.attr("width", legendWidth)
		.attr("height", legendHeight)
		.attr("class", function(d) { return setColor(d); });

	legend.append("text")
		.attr("x", 40 + 2)
		.attr("y", function(d, i){ return h/4 - (i*legendHeight) - 2*legendHeight + 15; })
		.attr("class", "mapSubtext")
		.text(function(d){ return d;});
};


var zoom = function() {
	var trans = d3.event.translate;
	svg.select("g")
		.attr("transform", "translate(" + trans + ")scale(" + d3.event.scale + ")");
	//scale stroke width based on zoom
	d3.selectAll("#d3_map").attr("stroke-width", ""+ (1.75/d3.event.scale) +"px");
};

//D3 hoverbox info way
var mouseover = function() {
	d3.select(this).style("stroke-width", "4px");
	var zip = d3.select(this).attr("title");
	var name = d3.select(this).attr("name");
	var value = currentData.data[zip];
	d3.select("#infoBox").html("Location:"+mapdict[zip]  + " Trips: " + value);
};


var mouseout = function() {
	d3.select(this).style("stroke-width", "");
};

var clickEvent = function() {
	var zip = d3.select(this).attr("title");
    var name = d3.select(this).attr("name");
    var value = currentData.data[zip];
	d3.select("#modalHeader").html("<h3><b>People in "+ mapdict[zip] + " have used taxi for "+value+" times in 2015<b></h3>" + "<div id='chart'></div>");
	//lookupTime(zip)
	$('#myModal').foundation('reveal', 'open');
};

//create svg element
initializeSVG();

//reading geoJSON file and assigns it to zipcode
//d3.json("static/data/zipcodes.json", function(zipcodes){
d3.json("static/data/neighbourhood.json", function(zipcodes){
	zips = zipcodes;
	return createMap(zips);
});


//monitor dropdown menu to change map colors
d3.select("#colorSelector").on("change", function() {
  d3.selectAll("svg").attr("class", this.value);
});


//monitor dropdown menu to change map data
d3.select("#dataSelector").on("change", function() {
	currentData = dataSets[this.value];
	dataLegendMax = currentData.maxDomain;

	setColor.domain([0, currentData.maxDomain]);
	createMap(zips);

	svg.attr("class", currentData.color);
});

