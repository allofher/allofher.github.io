fetch('https://api.chess.com/pub/player/allofher/stats')
  .then((response) => {
    return response.json()
  })
  .then((data) => {
    if (request.status >= 200 && request.status < 400) {
    data.forEach((stats) => {console.log(stats.rating)})
  } else {
    console.log('loop error')
  }
  })
  .catch((err) => {
    console.log('bigger error')
  })
