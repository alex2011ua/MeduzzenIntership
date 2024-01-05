const submit_button = document.getElementById("submit_button");
const text_area = document.getElementById("text-for-analyze")
const rezult = document.getElementById("demo")

submit_button.onclick = function () {
    start();
};

function start() {
    const text = text_area.value.trim()

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

    postData("/text_analyze", {"text": text}).then((data) => {
        const pretty_json = JSON.stringify(data, undefined, 2);

        function output(inp) {
        rezult.innerHTML = inp;
        }
        function syntaxHighlight(json) {
            json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
            return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
                var cls = 'number';
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
