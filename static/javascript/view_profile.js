function currentTime() {
  time = new Date();
  if (time.getSeconds() < 10) {
    seconds = "0"+time.getSeconds().toString();
  } else {
    seconds = time.getSeconds().toString();
  }
  result = formatTime(time);
  result = result.substring(0,(result.length-3))+seconds+" UTC";
  validTime = radarTime();

  obj = document.getElementById('clock');
  obj.innerHTML = "Current Time: "+result;
}
////////////////////////////////////////////////////////////////////////////////
function return_hazard_color(hazard){
  let color = "#d9b11d";
  try {
    if (hazard.feature.properties.event.includes("Severe")){
      //color = "#0032ff"; // blue
      color = "#ffec00"; // yellow
    } else if (hazard.feature.properties.event.includes("Tornado")){
      color = "#df1717";
    } else if (hazard.feature.properties.event.includes("Marine")){
      color = "#17dfdf";
    } else if (hazard.feature.properties.event.includes("Flood")){
      color = "#3eff05";
    } else {
      color = "#d9b11d";
    }
  }
  catch {
    if (hazard.properties.event.includes("Severe")){
      //color = "#0032ff"; // blue
      color = "#ffec00"; // yellow
    } else if (hazard.properties.event.includes("Tornado")){
      color = "#df1717";
    } else if (hazard.properties.event.includes("Marine")){
      color = "#17dfdf";
    } else if (hazard.properties.event.includes("Flood")){
      color = "#3eff05";
    } else {
      color = "#d9b11d";
    }
  }
  return color;
}
////////////////////////////////////////////////////////////////////////////////
function datetime_to_epoch(datetime_string){
  // Expects a datetime string in the format:
  // 2022-07-02T20:30:00-06:00
  var year = datetime_string.substring(0,4);
  var month = parseInt(datetime_string.substring(5,7)) - 1;
  var day = datetime_string.substring(8,10);
  var hour = datetime_string.substring(11,13);
  var minute = datetime_string.substring(14,16);
  // var datetime = new Date(year,month,day,hour,minute);
  var datetime = new Date(datetime_string);
  return datetime.getTime();
}
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
function get_NWS_headlines_for_point(lat,lon){
  /// get the latest NWS alerts/headlines for a specific location (lat/lon).
  var url = `https://api.weather.gov/alerts/active?point=${lat},${lon}`;
  var product_list = [];
  var request = new XMLHttpRequest();
  request.open("GET",url, false);
  request.send(null);
  data = JSON.parse(request.response);
  products = data.features;
  products.forEach(function(product){
    let expiration_time = product.properties.ends;
    let expiration_datetime = datetime_to_epoch(expiration_time);
    let current_datetime = new Date().getTime();
    if (current_datetime <= expiration_datetime){
      product_list.push(product.properties.headline);
    }
  });
  return product_list;
}
////////////////////////////////////////////////////////////////////////////////
function get_point_metadata(lat,lon){
  var url = `https://api.weather.gov/points/${lat}%2C${lon}`;
  var request = new XMLHttpRequest();
  request.open("GET",url, false);
  request.send(null);
  data = JSON.parse(request.response);
  return data;
}
////////////////////////////////////////////////////////////////////////////////
function updateCrawlerText(lat,lon){
  const TIME_PER_HEADLINE = 30*1000; // milliseconds - time to read each headline.
  var headlines = get_NWS_headlines_for_point(lat,lon);
  // performs the actual update of the messaage/crawler string.
  var crawler_string = "";
  let color = "#C9C9C9";
  if (headlines.length == 0){
    crawler_string = "No Active NWS Alerts."
  } else {
    headlines.forEach(function(headline){
      // get the appropriate text color
      if (headline.includes("Tornado")){
        color = "#E23939";
      } else if (headline.includes("Severe")){
        color = "#FFF344";
      } else if (headline.includes("Flash flood")){
        color = "#00FF3C";
      } else if (headline.includes("Flood")){
        color = "#32B250";
      } else if (headline.includes("Winter")){
        color = "#00D5FF";
      } else if (headline.includes("Ice")){
        color = "#FF49FA";
      } else if (headline.includes("Blizzard")){
        color = "#FF49FA";
      } else if (headline.includes("Special Marine")){
        color = "#03F8FF";
      } else if (headline.includes("Heat")){
        color = "#FFAF68";
      } else if (headline.includes("Excessive")){
        color = "#F38AA2";
      } else if (headline.includes("Dense fog")){
        color = "#9D9EBA";
      } else if (headline.includes("Red Flag")){
        color = "#FF81FF";
      } else if (headline.includes("Special Weather")){
        color = "#F9D3B2";
      } else {
        color = "#C9C9C9";
      }
      crawler_string = crawler_string + `<font color=${color}>${headline}</font>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`
    });
  }
  // set the speed of the animation
  var message = document.getElementById("news_message");
  var duration = (TIME_PER_HEADLINE * headlines.length);
  message.animate([
    { transform: 'translateX(100%)'},
    { transform: 'translateX(-300%)'},
  ],{
    duration: duration,
    easing: "linear",
    iterations: Infinity,
  });
  message.innerHTML = crawler_string;
  console.log(`Updated crawler, there were ${headlines.length} headlines.`);
  var news_bar = document.getElementById("news_ticker_bar");
  var buffer = 10;
  setInterval(function(){
    if (message.getBoundingClientRect().right < news_bar.getBoundingClientRect().left-buffer){
      animate_crawler(duration); // this effectively restarts the scroll text on the right
    }
  },1000);
}
////////////////////////////////////////////////////////////////////////////////
function animate_crawler(duration){
  var message = document.getElementById("news_message");
  message.animate([
    { transform: 'translateX(100%)'},
    { transform: 'translateX(-300%)'},
  ],{
    duration: duration,
    easing: "linear",
    iterations: Infinity,
  });
}
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
