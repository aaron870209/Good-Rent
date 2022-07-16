// Main chart render location
let chart1Id = 'chart1';
let chart2Id = 'chart2';
let chart3Id = 'chart3';

// CHART DATA
// -----------------------------

//let income = [
//  500, 1000, 2500, 700, 3500, 600, 1000, 1000, 1000, 800, 3000, 4500, 5000,
//];
//let dates = [
//  '01/07',
//  '02/07',
//  '03/07',
//  '04/07',
//  '05/07',
//  '06/07',
//  '07/07',
//  '08/07',
//  '09/07',
//  '10/07',
//  '11/07',
//  '12/07',
//  '13/07',
//];

// CHART CONFIG
// -----------------------------


// Chart 2
function draw_realtime(data){
    let sales = [[data.new_data[data.new_data.length - 1]], [data.Taipei_591[data.Taipei_591.length-1]],
    [data.New_Taipei_591[data.New_Taipei_591.length-1]], [data.Taipei_lewu[data.Taipei_lewu.length-1]],
    [data.New_Taipei_lewu[data.New_Taipei_lewu.length-1]]];
    let chart2Data = {
      type: 'hbar',
      globals: {
        fontFamily: 'Poppins',
      },
      backgroundColor: 'transparent',
      title: {
        text: 'Real Time',
        align: 'left',
        fontColor: 'var(--lightGray)',
        fontWeight: 'normal',
        padding: '16px',
      },
      plot: {
        tooltip: {
          visible: false,
        },
        barSpace: '32px',
        barWidth: '12px',
        borderWidth: '0px',
      },
      plotarea: {
        margin: '40px 56px 16px 56px',
      },
      scaleY: {
        visible: false,
      },
      scaleX: {
        labels: ["資料量"],
        lineWidth: '0px',
        tick: {
          visible: true,
        },
      },
      scaleX2: {
        values: [
          sales[0],
          sales[1],
          sales[2],
          sales[3],
          sales[4],
        ],
        lineWidth: '0px',
        tick: {
          visible: false,
        },
      },
      series: [
        {
          values: sales[0],
          backgroundColor: 'var(--yellow)',
        },
        {
          values: sales[1],
          backgroundColor: '#FFFF6F',
        },
        {
          values: sales[2],
          backgroundColor: '#FFFFAA',
        },
        {
          values: sales[3],
          backgroundColor: '#53FF53',
        },
        {
          values: sales[4],
          backgroundColor: '#A6FFA6',
        },
      ],
    };
    zingchart.render({
      id: chart2Id,
      data: chart2Data,
      height: '300px',
      width: '100%',
    });


}




function draw_line(data){
    // Chart 3
    let chart3Data = {
      type: 'line',
      globals: {
        fontFamily: 'Poppins',
      },
      backgroundColor: 'transparent',
      scaleX: {
        labels: data.date,
        tick: {
          visible: false,
        },
      },
      scaleY: {
        values: '0: 1000',
        guide: {
          lineStyle: 'solid',
          lineColor: 'var(--lightGray)',
        },
        lineWidth: '0px',
        tick: {
          visible: false,
        },
      },
      series: [
        {
          values: data.new_data,
          lineColor: 'var(--yellow)',
          lineWidth: '5px',
          marker: {
            backgroundColor: 'var(--lightPurple)',
            borderColor: 'var(--yellow)',
            borderWidth: '3px',
            size: 8,
          },
        },
      ],
};

// Chart 3
zingchart.render({
  id: chart1Id,
  data: chart3Data,
  height: '250px',
  width: '800px',
});
}

// RENDER CHARTS
// -----------------------------

// Chart 1
//zingchart.render({
//  id: chart1Id,
//  data: chart1Data,
//  height: '300px',
//  width: '100%',
//});

// Chart 2



function draw_bar(data){
    var trace1 = {
      x: data.date,
      y: data.Taipei_591,
      name: '591_Taipei',
      type: 'bar'
    };

    var trace2 = {
      x: data.date,
      y: data.New_Taipei_591,
      name: '591_New_Taipei',
      type: 'bar',
    };
    var trace3 = {
      x: data.date,
      y: data.Taipei_lewu,
      name: 'lewu_Taipei',
      type: 'bar'
    };
    var trace4 = {
      x: data.date,
      y: data.New_Taipei_lewu,
      name: 'lewu_New_Taipei',
      type: 'bar'
    };

    var data = [trace1, trace2, trace3, trace4];

    var layout = {barmode: 'group',
                    paper_bgcolor: "#2d2d45",
                    plot_bgcolor: "#2d2d45",
                    colorway: ['#FFFF6F','#FFFFAA','#53FF53','#A6FFA6'],
                    xaxis: {tickfont: {
                        size: 14,
                        color: 'white'
                    }
                    },
                    yaxis: {
                        range: [0, 13000],
                        title: '資料筆數',
                        titlefont: {
                        size: 16,
                        color: 'white'
                        },
                        tickfont:{
                        size:14,
                        color: 'white'
                        }
                        },
                    legend:{
                        font:{
                            color:"white"
                        }
                    }
                    };

    Plotly.newPlot('chart3', data, layout);
}





function ajax(){
var xmlhttp = new XMLHttpRequest();
    var url = "/dashboard_data";
    xmlhttp.onreadystatechange = function (){
        if (this.readyState == 4 && this.status == 200) {
            let data = this.response
            console.log("total_data="+data.date)
            console.log(data.Taipei_591)
            draw_line(data)
            draw_bar(data)
            draw_realtime(data)
        };
    };


    xmlhttp.open("POST", url, true);
    xmlhttp.setRequestHeader('Content-Type','application/x-www-form-urlencode');
    xmlhttp.responseType = 'json';
    xmlhttp.send(JSON.stringify({
    }));
}
ajax()