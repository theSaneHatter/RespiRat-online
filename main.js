console.log('main.js is running')
fetch('/test')
  .then(response => response.text())
  .then(data => {
    window.prefix = data;
    console.log('we got our data:', window.prefix);
  })
  .catch(err => console.error(err));


function get_temp(){
  fetch('/temp')
    .then(response => response.text())
    .then(data => {
      document.getElementById('temp').innerHTML = "temp is " + data;
      console.log('got temp as: ', data)
    })
}

setInterval(get_temp, 10000)

function get_adc(){
  fetch('/adc')
    .then(response => response.text())
    .then(data => {
      document.getElementById('adc').innerHTML = "adc is: " + data.value;
      console.log('got adc as: ', data.value)
    })
}
// setInterval(get_adc, 100)

function lightoff(){
  let button = document.getElementById('lightoff')
  button.style.color = 'red'
  fetch('/lightoff')
    .then(response => response.text())
    .then(data => {
      document.getElementById('led').innerHTML = 'led is '+data
      button.style.color = 'black'
    })
}
function lighton(){
  let button = document.getElementById('lighton')
  button.style.color = 'red'
  fetch('/lighton')
    .then(response => response.text())
    .then(data => {
      document.getElementById('led').innerHTML = 'led is '+data
      button.style.color = 'black'
    })
}


//graph stuff



let canvas = document.getElementById("can")
let ctx = canvas.getContext('2d')

ctx.fillStyle = 'rgb(50,5,50)'
ctx.fillRect(0, 0, 50, 50)

ctx.fillStyle="rgb(0,256,0)"
ctx.fillRect(0,0,1000,1000)

function graph_adc(){

  let data = [[1,10],[2,20],[3,30],[4,40]]
  fetch('/adc')
    .then(response => response.text())
    .then(data => {
      document.getElementById('adc').innerHTML = "adc is: " + data;
      console.log('got adc as: ', data)
    })

}

function fillCircle(x, y, r) {
  ctx.beginPath();
  ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fill();
}

let x = 0
let y = 0
let s = 0
let f = 0

let data = [[1,10],[2,20],[3,30],[4,40]]
let startTime = Date.now()
let recevedTime = 0

function update_data(){
  console.log('!!!@debug:@updateData():starting update_data()...')
  fetch('/adc')
    .then(response => response.json())
    .then(value => {
      document.getElementById('adc').innerHTML = "adc is: " + value.value;
      console.log('got adc as: ', value)
      recevedTime = Math.round(Date.now()/1000)
      console.log('recevedTime-value.time:',recevedTime - value.time)
      let x = Math.abs(recevedTime - value.time)
      let y = Math.round(value.value)
      let toAdd = [x,y]
      data.push(toAdd)
      console.log("toAdd:",toAdd)
      //remove later? artifical delay for recall
      setTimeout(update_data,100)
    })
}
update_data()

let delay = 1000

// graph section
let lastTime = 0
function graph(time){
  const dt = (time-lastTime)/1000
  lastTime = time
  f += dt*60

  data = data.map(function(e){return [e[0]+delay/10,e[1]]})
  data = data.filter(([x,_]) => x <= canvas.width + 100)

  console.log("@debug:@graphSection:start of section, f =",f)
  //clear screen
  ctx.fillStyle="rgb(255,255,255)"
  ctx.fillRect(0,0,1000,1000)
  //center line
  ctx.fillStyle = 'rgb(0,0,0)'
  ctx.fillRect(0,498,1000,2)


  //fillCircle(f/2,Math.sin(f/20)*200 + 500,10)
 // data.push([f,Math.sin(f)*400+500])


  ctx.fillStyle = 'rgb(0,0,255)'
  for (let i = 0;i<data.length;i++){
    [x,y] = [data[i][0], data[i][1]]
    console.log('@debug:@about_to_draw_point_square:x,y:',x,y)
    ctx.fillStyle = 'rgb(255,0,0)'
    ctx.fillRect(x-1, y-1, 20,20)
  }

  ctx.lineWidth = 1;
  ctx.strokeStyle = "black";
  for (let i = 0;i<data.length;i++){
    [x,y] = [data[i][0], data[i][1]]
    if (i > 0){
      ctx.beginPath();
      ctx.moveTo(data[i-1][0], data[i-1][1]);
      ctx.lineTo(data[i][0], data[i][1]);
      ctx.stroke();
       }
   }

  console.log('@debug@the_end_of_interval:data:',data)

  requestAnimationFrame(graph)
}
requestAnimationFrame(graph)
