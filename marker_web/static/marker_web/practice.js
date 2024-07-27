
let paperForm = document.querySelector("form");
paperForm.onsubmit = (event) => {
    event.preventDefault();
    // Make a loading screen
    let overlay = document.querySelector(".overlay");
    overlay.style.display = "block";

    // Send the form data to server for processing
    const formData = new FormData(event.target);
    const formObj = {};

    formData.forEach((value, key) => {
        // If data under the same input name already exists, store the next instance into an array
        if (formObj[key]) {
            if (Array.isArray(formObj[key])) {
                formObj[key].push(value);
            } else {
                formObj[key] = [formObj[key], value];
            }
        } else {
            formObj[key] = value;
        }
    });

    history.pushState(
        { 
            formData: formObj,
            view: "Practice"
        }, null, window.location.pathname + window.location.search
    );

    // Disable all textareas and submit button
    document.querySelectorAll("textarea").forEach((elem) => {
        elem.disabled = true;
    });

    document.querySelector('button[type="submit"]').disabled = true;

    // Send form data in fetch request
    fetch("/results", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(formObj),
    })
    .then((response) => response.json())
    .then((results) => {

        // Remove loading screen
        overlay.style.display = "none";
        window.scroll({
            top: 0,
            left: 0,
            behaviour: "smooth",
        });

        generate_results(results)
        
        // Save current state
        localStorage.setItem('results', JSON.stringify(results))
        
        history.pushState(
            { 
                formData: formObj,
                results: results, 
                view: 'results' 
            }, 
            "Marker AI: results", 
            window.location.pathname + window.location.search + ('&result=yes')
        );

    });
};

// Handle changing history in browser
window.addEventListener("popstate", function (event) {
    if (event.state) {
        const state = event.state;
        console.log(state)
        // Restore the form data
        Object.keys(state.formData).forEach((key) => {

            let inputs = document.querySelectorAll(`textarea[name="${key}"]`)
            console.log(key, inputs)
            if (inputs.length > 0) {
                if (inputs.length > 1) {
                    inputs.forEach((item, index) => {
                        item.value = state.formData[key][index]
                    })
                } else {
                    inputs[0].value = state.formData[key]
                }
            }
            console.log(state.formData[key])
        });

        // Remove all existing results divs
        document.querySelectorAll('form div[class="results_div"]').forEach((div) => div.remove());

        // Restore the results if they exist
        if (state.results) {
            generate_results(state.results)
        } else {
            // Clear the form and results if there's no state (initial load)
            document.querySelectorAll('form div[class="results_div"]').forEach((div) => div.remove());
            document.querySelectorAll('textarea').forEach(textarea => textarea.disabled = false);
            document.querySelector('button[type="submit"]').disabled = false;
        }
    }
});

// Handle reloading on results page
window.addEventListener('load', () => {
    // https://www.sitepoint.com/get-url-parameters-with-javascript/
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('result')) {
        // https://stackoverflow.com/questions/28314368/how-to-maintain-state-after-a-page-refresh-in-react-js
        let results = JSON.parse(localStorage.getItem('results'))
        console.log(results)
        if (results) {
            generate_results(results)
        }
    }
})

function generate_results(results){
    for (let i = 0; i < results["all_data"].length; i++) {
        data = results["all_data"][i];
        let num = data["num"];
        let mark_scheme_points = data["mark_scheme_points"];
        let correct_points = data["correct_points"];
        let got_marks = data["got_marks"];
        let max_marks = data["max_marks"];

        let textArea = document.querySelectorAll(
            `textarea[name='${num}']`
        );
        let last = textArea[textArea.length - 1];

        // Make a div to show marked data
        let marked_data = document.createElement("div");
        marked_data.className = "results_div";
        marked_data.innerHTML = `
            <br>
            <div class="card">
                <div class="card-header bg-purple">
                    <p class="text-white m-0 ">Marked results for question ${num}</p>
                </div>

                <div class="card-body">
                </div>
            </div>
        `;

        let card_body = marked_data.querySelector("div[class='card-body']");
        card_body.innerHTML = `<b>Marks</b>: ${got_marks} out of ${max_marks}<br>`;
        mark_scheme_points.forEach((val, i) => {
            card_body.append(
                (correct_points[i] ? "✅" : "❌") + val
            );
            card_body.append(document.createElement("br"));
        });
        last.after(marked_data);
    }
}