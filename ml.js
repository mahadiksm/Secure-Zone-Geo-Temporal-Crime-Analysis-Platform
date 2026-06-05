async function loadMLAndUpdateLineGraph(lineId, tLabels, tValues){

try{
let res = await fetch("http://127.0.0.1:5000/predict");
let ml = await res.json();

let newX = [...tLabels, ml.next_year];
let newY = [...tValues, ml.predicted_crime];

Plotly.newPlot(lineId,[
{
x: tLabels,
y: tValues,
mode: "lines+markers",
name: "Actual Data",
line:{color:"#00ccff"}
},
{
x: newX,
y: newY,
mode: "lines+markers",
name: "ML Prediction",
line:{color:"#ff4d4d", dash:"dot"}
}
],{
title:"LINE GRAPH (WITH ML)",
paper_bgcolor:"#111827",
plot_bgcolor:"#111827",
font:{color:"white"}
});

}catch(e){
console.error("ML Error:", e);
}

}