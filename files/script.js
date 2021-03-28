var request = new XMLHttpRequest()

request.open('GET', 'https://api.chess.com/pub/player/allofher/stats', true)
request.onload = function () {
  // Begin accessing JSON data here
  var data = JSON.parse(this.response)

  if (request.status >= 200 && request.status < 400) {
    data.forEach((stats) => {console.log(stats.rating)})
  } else {
    console.log('error')
  }
}

request.send()
