var $ = window.jQuery;
var slideIndex = 1;
var videoWidth = 640;
var videoHeight = 480;

$(window.document).ready(function () {

  document.getElementById('canvas').style.display = 'none';
  document.getElementById('wait').style.display = 'none';
  document.getElementById('message').style.display = 'none';
  document.getElementById('result').style.display = 'none';
  document.getElementById('outImage').style.display = 'none';
  document.getElementById('loadImage').style.display = 'none';

  $('#uploadbtn').on('change', upload_file);
  $('#drop-files').on('drop', upload_file);
  $('#snap').on('click', upload_video);
  $('#how-it-work').on('click', showHowItWork);
  $('#wrap-how-it-work').on('click', closeHowItWork);
  $('#close').on('click', closeHowItWork);
  $('#plus-divs--1').on('click', () => plusDivs(-1));
  $('#plus-divs-1').on('click', () => plusDivs(1));
  $('#current-div-1').on('click', () => currentDiv(1));
  $('#current-div-2').on('click', () => currentDiv(2));
  $('#current-div-3').on('click', () => currentDiv(3));

  $('#drop-files').on('dragover', function (e) {
    e.preventDefault();
    e.stopPropagation();
  });

  $('#drop-files').on('dragenter', function (e) {
    e.preventDefault();
    e.stopPropagation();
  });

  var video = document.getElementById('video');

  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({video: true}).then(function (stream) {
      video.srcObject = stream;
      video.play();
      video.onloadedmetadata = function() {
      videoWidth = this.videoWidth;
      videoHeight = this.videoHeight;
    }
    });
  }

  function validImage(filename) {
    var extension = filename.substr(filename.lastIndexOf('.') + 1);
    switch (extension) {
      case 'png':
      case 'jpg':
      case 'jpge':
      case 'PNG':
        return true;
      default:
        return false;
    }
  }

  function upload(data) {
  document.getElementById('message').style.display = 'none';
  document.getElementById('result').style.display = 'none';
  document.getElementById('wait').style.display = 'block';
    $.ajax({
      url: '/upload/',
      type: 'POST',
      data: data,
      cache: false,
      dataType: 'json',
      processData: false,
      contentType: false,
      success: uploadsuccess,
      error: function (XHR, status, error) {
        console.log('Error: ', error);
      }
    });
  }

  function getBase64(file) {
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function () {
      var data = new FormData();
      data.append("data", reader.result);
      upload(data);
      };
    reader.onerror = function (error) {
      console.log('Error: ', error);
      };
      return reader.result;
    }

  function upload_file(event) {
    event.preventDefault();
    event.stopPropagation();

    var file = event.target.files !== undefined
      ? event.target.files[0]
      : event.originalEvent.dataTransfer.files[0];

    if (validImage(file.name)) {
    getBase64(file);
    }
    else {
      window.alert('Invalid format');
    }

    var files = [];
    files[0] = file;

    // FileReader support
      if (FileReader && files && files.length) {
        var fr = new FileReader();
        fr.onload = function () {
          document.getElementById('loadImage').style.display = 'block';
          document.getElementById('outImage').style.display = 'block';
          document.getElementById('outImage').src = fr.result;
        };
        fr.readAsDataURL(file);
      }
      // Not supported
      else {
        // fallback -- perhaps submit the input to an iframe and temporarily store
        // them on the server until the user's session ends.
      }
  }

  function upload_video(event) {
    event.preventDefault();
    event.stopPropagation();

    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    var video = document.getElementById('video');
    context.canvas.width  = video.videoWidth;
    context.canvas.height = video.videoHeight;

    context.drawImage(video, 0, 0, videoWidth, videoHeight);

    var img = canvas.toDataURL("image/png");
    document.getElementById('loadImage').style.display = 'block';
    document.getElementById('outImage').style.display = 'block';
    document.getElementById("outImage").src = img;
    var data = new FormData();
    data.append("data", img);

    upload(data);
  }

  function uploadsuccess(data, status) {
    var data = JSON.parse(data);
    document.getElementById('wait').style.display = 'none';

    if (data.status == 'BAD_REQUEST'){
      var message = data.message;
      document.getElementById('message').style.display = 'block';
      $('#message').html(message);
    }
    else if (data.status == 'UNKNOWN'){
      var message = data.message;
      document.getElementById('message').style.display = 'block';
      $('#message').html(message);
    }
    else if (data.status == 'OK') {
      document.getElementById('result').style.display = 'block';
      var names = ["name1", "name2", "name3"];
      var photos = ["photo1", "photo2", "photo3"];
      for (var i = 0; i < data.persons.length; i++) {
        document.getElementById(names[i]).innerHTML = data.persons[i].name + ' (' + data.persons[i].score + '%)';
        document.getElementById(photos[i]).src = data.persons[i].image_link;
      }
      showDivs(slideIndex);

//      console.log(data.person);
//      var name = data.person.name;
//      var photo = data.person.photo;
//      document.getElementById('result').style.display = 'block';
//      document.getElementById("resultImg").src = photo;
//      $('#resultName').html(name);
    }
  }

  function plusDivs(n) {
    console.log(n);
    showDivs(slideIndex += n);
  }

  function currentDiv(n) {
    showDivs(slideIndex = n);
  }

  function showDivs(n) {
    var i;
    var names = document.getElementsByClassName("mySlidesName");
    var photos = document.getElementsByClassName("mySlidesPhoto");
    var dots = document.getElementsByClassName("demo");
    if (n > photos.length) {slideIndex = 1}
    if (n < 1) {slideIndex = photos.length}
    for (i = 0; i < photos.length; i++) {
       photos[i].style.display = "none";
       names[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
       dots[i].className = dots[i].className.replace(" w3-black", "");
    }
    photos[slideIndex-1].style.display = "block";
    names[slideIndex-1].style.display = "block";
    dots[slideIndex-1].className += " w3-black";
  }

  function showHowItWork(){
    document.getElementById('window-how-it-work').style.display = 'block';
    document.getElementById('wrap-how-it-work').style.display = 'block';
  };

  function closeHowItWork(){
    document.getElementById('window-how-it-work').style.display = 'none';
    document.getElementById('wrap-how-it-work').style.display = 'none';
  };

});
