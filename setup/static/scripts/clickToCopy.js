const outputTextArea = document.querySelector("#output-textarea");
const inputTextArea = document.querySelector("#input-textarea");
const copyButton = document.querySelector("#copy-btn");
const dowloadButton = document.querySelector("#download-btn");
const resumeButton = document.querySelector("#resume-btn");

/*function textTransform() {
 
  fetch("https://jsonplaceholder.typicode.com/posts/")
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error(error));

  var text = inputTextArea.value;
  outputTextArea.value = text;
  console.log(text);

}*/

function dowloadText() {}
function clickToCopy() {
  outputTextArea.select();
  outputTextArea.setSelectionRange(0, 99999);

  navigator.clipboard.writeText(outputTextArea.value);

  alert("Texto copiado.");
}
copyButton.addEventListener("click", clickToCopy);



function makeRequest(url, params, outputElementId, successMessage) {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', url, true);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        document.getElementById(outputElementId).textContent = successMessage(response);
      }
    }
  };

  var formData = new URLSearchParams();
  for (var key in params) {
    formData.append(key, params[key]);
  }

  xhr.send(formData);
}

document.getElementById('postForm').addEventListener('submit', function(e) {
  e.preventDefault();

  var texto = document.getElementById('input-textarea').value;
  var num_sentencas = document.getElementById('input-numero').value;
  var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

  var params = {
    texto: texto,
    num_sentencas: num_sentencas,
    csrfmiddlewaretoken: csrfToken
  };

  makeRequest('/sumarizar_texto', params, 'output-textarea', function(response) {
    return response.resumo;
  });

  makeRequest('/obter_informacoes_texto', params, 'output-textarea2', function(response) {
    var result = 'Melhores sentenças: \n' + response.melhores_sentencas.join(', ') + '\n';
    result += 'Número de sentenças calculado: \n' + response.num_sentencas + '\n';
    result += 'Palavras redundantes: \n' + response.palavras_redundantes.join(', ');
    return result;
  });
});



/*
document.getElementById('postForm').addEventListener('submit', getData);

function getData(e){
  e.preventDefault();

  var texto = document.getElementById('input-textarea').value;
  var num_sentencas = document.getElementById('input-numero').value;
  var params = {user_input:texto, quant: num_sentencas}

  var xhr = new XMLHttpRequest();
  xhr.open('post', '/sumarizar_texto', true);
  
  // Verifique se a solicitação xhr foi criada corretamente antes de configurar o cabeçalho
  if (xhr) {
      var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
      xhr.setRequestHeader('X-CSRFToken', csrfToken);
  }
  xhr.onload = function() {
    document.getElementById('output-textarea').textContent = this.responseText;
  };

  xhr.send(JSON.stringify(params));
}

/*
document.getElementById('postForm').addEventListener('submit', getData);

function getData(e){
  e.preventDefault();

  var texto = document.getElementById('input-textarea').value;
  var num_sentencas = document.getElementById('input-numero').value;
  var params = {user_input:texto, quant: num_sentencas}

  var xhr = new XMLHttpRequest();

  xhr.open('post', '/sumarizar_texto/', true);
  xhr.setRequestHeader('Content-type','application/json')
  'csrfmiddlewaretoken'('input[name=csrfmiddlewaretoken]').val()

  xhr.onload = function(){
    document.getElementById('output-textarea').innerHTML = this.responseText;
  }

  xhr.send(JSON.stringify(params));
}


/*Pegando o arquivo de texto inserido pelo usuario e enviando para o backend
document.getElementById('inputFile').addEventListener('change', function() {
  var file = new FileReader();
  file.onload = () => {
    document.getElementById('fileForm').addEventListener('submit', function(e){
      e.preventDefault();

      var name = file.result;
      var quant2 = document.getElementById('quant2').value;
      var params = {user_input:name, quant: quant2}

      var xhr = new XMLHttpRequest();

      xhr.open('post', '../file', true);
      xhr.setRequestHeader('Content-type','application/json')

      xhr.onload = function(){
        document.getElementById('sumarizado').innerHTML = this.responseText;
      }
            
      xhr.send(JSON.stringify(params));
    });
  }
  file.readAsText(this.files[0]);
});         
*/
