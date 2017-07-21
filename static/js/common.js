var $ = window.jQuery;

$(window.document).ready(function () {

  document.getElementById('canvas').style.display = 'none';
  document.getElementById('message').style.display = 'none';

  $('#uploadbtn').on('change', upload_file);
  $('#drop-files').on('drop', upload_file);
  $('#snap').on('click', upload_video);

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
      video.src = window.URL.createObjectURL(stream);
      video.play();
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

    context.drawImage(video, 0, 0, 640, 480);

    var img = canvas.toDataURL("image/png");
    document.getElementById("outImage").src = img;
    var data = new FormData();
    data.append("data", img);

    upload(data);
  }

  function uploadsuccess(data, status) {
    var data = JSON.parse(data);
    var table = document.getElementById("table");
    var rows = table.getElementsByTagName("tr").length;
    document.getElementById('message').style.display = 'none';
    for (var j = 0; j < rows; j++) {
      table.deleteRow(0);
    }

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
      for (var i = 0; i < data.persons.length; i++) {
        var row = table.insertRow(i);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        cell1.innerHTML = data.persons[i].name;
        cell2.innerHTML = data.persons[i].score;
      }
    }
  }

});
