const analyze_button = document.getElementById("analyze_button");
const sentiment_button = document.getElementById("sentiment_button");
const text_area = document.getElementById("text-for-analyze")
const rezalt = document.getElementById("demo")
const rezalt2 = document.getElementById("demo2")
rezalt2.style.fontSize = "200%"
rezalt2.style.alignContent = "center"
let analyzed_data = []


analyze_button.onclick = function () {
    start();
};
sentiment_button.onclick = function () {
    sentiment();
};
async function postData(url = "", data = {}) {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data), // body data type must match "Content-Type" header
      });
      return response.json(); // parses JSON response into native JavaScript objects
     }
function start() {
    rezalt.innerHTML = "";
    const text = text_area.value.trim()

    postData("/text_analyze", {"text": text}).then((data) => {
        const pretty_json = JSON.stringify(data, undefined, 2);
        analyzed_data = data;
        function output(inp) {
        rezalt.innerHTML = inp;
        }
        function syntaxHighlight(json) {
            json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
            return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
                let cls = 'number';
                if (/^"/.test(match)) {
                    if (/:$/.test(match)) {
                        cls = 'key';
                    } else {
                        cls = 'string';
                    }
                } else if (/true|false/.test(match)) {
                    cls = 'boolean';
                } else if (/null/.test(match)) {
                    cls = 'null';
                }
                return '<span class="' + cls + '">' + match + '</span>';
            });
        }
        output(syntaxHighlight(pretty_json));
    });
}

function sentiment() {
    postData("/sentiment_analyze", {"analyzed_text": analyzed_data}).then((data) => {
        let ul = document.getElementById("ul")
        ul.innerText= "";
        rezalt2.innerText = "";

        let count_sentiment = 0;
        data.forEach(renderProductList);
            function renderProductList(element, index, arr) {
                let text = element[0];
                let sentiment = element[1];
                count_sentiment += sentiment;
                let color = "black"
                if (sentiment > 0){color = "green"}
                else if (sentiment < 0) { color= "red"}

                let li = document.createElement('li');
                li.setAttribute('class','item');
                ul.appendChild(li);
                li.innerHTML=li.innerHTML + text;
                li.style.color = color;
                li.style.listStyleType = "none";
            }
        if(count_sentiment > 0){
            rezalt2.innerText = "Good";
            rezalt2.style.color = "green";
        }
        else if (count_sentiment < 0){
            rezalt2.innerText = "Bad";
            rezalt2.style.color = "red";
        }
        else {
            rezalt2.innerText = "Neutral";
            rezalt2.style.color = "black";
        }

    });
}
