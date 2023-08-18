console.log("Hello World!");
function btnClick(button) {
	console.log("Button clicked!");



	if (button.innerHTML == "9") {
	 var newValue = 0;
	} else {
    var currentValue = parseInt(button.innerHTML);
    var newValue = currentValue + 1;
    }
    button.innerHTML = newValue;
    button.style.color = newValue === 0 ? 'white' : 'black';
    checkAllValues();
    checkDuplicates();
}

function sendAllValues() {
    var buttonData = [];
    var buttons = document.querySelectorAll('.sBtn');

//    console.log("buttons", buttons);

    buttons.forEach(button => {
    	var id = button.id;
		var value = parseInt(button.innerHTML);
		buttonData.push({ id: id, value: value }); // Increment the value
    }
    );



    fetch('/solve-sudoku', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(buttonData)
    }).then(response => {
        if (response.ok) {
            // Handle success if needed

            return response.json();

        } else {
            // Handle error if needed
        }
    })
    .then(data => {
    // Handle the parsed response data
    console.log("Success!");
    console.log(data); // Log the returned array
    data.forEach(updatedButton => {
            var button = document.getElementById(updatedButton.id);
            if (button) {
                button.innerHTML = updatedButton.value;

                button.style.color = updatedButton.value === 0 ? 'white' : 'black';
            }
        });
     // make button with id = sendAllButton not visible and make button with id = reset visible
    })
    .catch(error => {
        // Handle error
    });
}

function clearAllValues() {
var buttonData = [];
    var buttons = document.querySelectorAll('.sBtn');

    buttons.forEach(button => {
        var id = button.id;
        var value = '0';
        // make all buttons white
        button.style.color = 'white';
        // make all buttons 0
        button.innerHTML = value;
        // make the button with id="reset" not visible
        document.getElementById("reset").style.visibility = "hidden";
        // make the button with id="sendAllButton" not visible
        document.getElementById("sendAllButton").style.visibility = "hidden";

    });
}

// if all buttons are 0 then make button with id="sendAllButton" not visible
// if any button is not 0 then make button with id="sendAllButton" visible
function checkAllValues() {
	var buttonData = [];
	var buttons = document.querySelectorAll('.sBtn');
	var allZeros = true;

	buttons.forEach(button => {
		var id = button.id;
		var value = parseInt(button.innerHTML);
		buttonData.push({ id: id, value: value }); // Increment the value
		if (value !== 0) {
			allZeros = false;
		}
	});

	if (allZeros) {
		document.getElementById("sendAllButton").style.visibility = "hidden";
	document.getElementById("reset").style.visibility = "hidden";
	} else {
		document.getElementById("sendAllButton").style.visibility = "visible";
		// make the button with id="reset" visible
		document.getElementById("reset").style.visibility = "visible";
	}
}

// make button with id="reset" not visible and make button with id="sendAllButton" not visible
function reset() {
	var buttonData = [];
	var buttons = document.querySelectorAll('.sBtn');

	buttons.forEach(button => {
		var id = button.id;
		var value = '0';
		// make all buttons white
		button.style.color = 'white';
		// make all buttons 0
		button.innerHTML = value;
		// make the button with id="reset" not visible
		document.getElementById("reset").style.visibility = "hidden";
		// make the button with id="sendAllButton" not visible
		document.getElementById("sendAllButton").style.visibility = "hidden";

	});
}

function checkDuplicates() {
var buttonData = [];
    var buttons = document.querySelectorAll('.sBtn');
    var r1st = []
    var r2nd = []
    var r3rd = []
    var r4th = []
    var r5th = []
    var r6th = []
    var r7th = []
    var r8th = []
    var r9th = []
    var s1st = []
    var s2nd = []
    var s3rd = []
    var s4th = []
    var s5th = []
    var s6th = []
    var s7th = []
    var s8th = []
    var s9th = []

    buttons.forEach(button => {
        var id = button.id;
        var value = parseInt(button.innerHTML);
        buttonData.push({ id: id, value: value });
        // get second last character of id
        var secondLastChar = id.charAt(id.length - 2);
        // get last character of id
        var lastChar = id.charAt(id.length - 1);

        if (secondLastChar == 0) {
        if (value !== 0) {
            r1st.push(value);
            }
        }
        if (secondLastChar == 1) {
        if (value !== 0) {
			r2nd.push(value);
			}
		}
		if (secondLastChar == 2) {
		if (value !== 0) {
			r3rd.push(value);
			}

		}
		if (secondLastChar == 3) {
		if (value !== 0) {
			r4th.push(value);
			}

		}
		if (secondLastChar == 4) {
		if (value !== 0) {
			r5th.push(value);
			}

		}
		if (secondLastChar == 5) {
		if (value !== 0) {
			r6th.push(value);
			}

		}
		if (secondLastChar == 6) {
		if (value !== 0) {
			r7th.push(value);
			}

		}
		if (secondLastChar == 7) {
		if (value !== 0) {
			r8th.push(value);
			}

		}
		if (secondLastChar == 8) {
		if (value !== 0) {
			r9th.push(value);
			}

		}
		if ((lastChar == 0 || lastChar == 1 || lastChar == 2 ) && (secondLastChar == 0 || secondLastChar == 1 || secondLastChar == 2)) {
		if (value !== 0) {
			s1st.push(value);
			}
			}
		if ((lastChar == 3 || lastChar == 4 || lastChar == 5 ) && (secondLastChar == 0 || secondLastChar == 1 || secondLastChar == 2)) {
			if (value !== 0) {
			s2nd.push(value);
			}
			}
		if ((lastChar == 6 || lastChar == 7 || lastChar == 8 ) && (secondLastChar == 0 || secondLastChar == 1 || secondLastChar == 2)) {
			if (value !== 0) {
			s3rd.push(value);
			}
			}
		if ((lastChar == 0 || lastChar == 1 || lastChar == 2 ) && (secondLastChar == 3 || secondLastChar == 4 || secondLastChar == 5)) {
			if (value !== 0) {
			s4th.push(value);
			}
			}
		if ((lastChar == 3 || lastChar == 4 || lastChar == 5 ) && (secondLastChar == 3 || secondLastChar == 4 || secondLastChar == 5)) {
			if (value !== 0) {
			s5th.push(value);
			}
			}
		if ((lastChar == 6 || lastChar == 7 || lastChar == 8 ) && (secondLastChar == 3 || secondLastChar == 4 || secondLastChar == 5)) {
			if (value !== 0) {
			s6th.push(value);
			}
			}
		if ((lastChar == 0 || lastChar == 1 || lastChar == 2 ) && (secondLastChar == 6 || secondLastChar == 7 || secondLastChar == 8)) {
			if (value !== 0) {
			s7th.push(value);
			}
			}
		if ((lastChar == 3 || lastChar == 4 || lastChar == 5 ) && (secondLastChar == 6 || secondLastChar == 7 || secondLastChar == 8)) {
			if (value !== 0) {
			s8th.push(value);
			}
			}
		if ((lastChar == 6 || lastChar == 7 || lastChar == 8 ) && (secondLastChar == 6 || secondLastChar == 7 || secondLastChar == 8)) {
			if (value !== 0) {
			s9th.push(value);
			}
			}
    });

//    console.log("r1st",r1st);
//    console.log("r2nd",r2nd);
//    console.log("r3rd",r3rd);
//    console.log("r4th",r4th);
//    console.log("r5th",r5th);
//    console.log("r6th",r6th);
//    console.log("r7th",r7th);
//    console.log("r8th",r8th);
//    console.log("r9th",r9th);
//    console.log("s1st",s1st);
//    console.log("s2nd",s2nd);
//    console.log("s3rd",s3rd);
//    console.log("s4th",s4th);
//    console.log("s5th",s5th);
//    console.log("s6th",s6th);
//    console.log("s7th",s7th);
//    console.log("s8th",s8th);
//    console.log("s9th",s9th);

    // check if there are any duplicates in the array r1st
    var r1stDuplicates = r1st.filter(function(item, index){
    	return r1st.indexOf(item) != index;
    }
    );
    if (r1stDuplicates.length > 0) {
		// set h1 with id of error to have innerHTML of "There are duplicates in the first row"
		return document.getElementById("error").innerHTML = "There are duplicates in the first row";
	}
	// check if there are any duplicates in the array r2nd
	var r2ndDuplicates = r2nd.filter(function(item, index){
			return r2nd.indexOf(item) != index;
	}
	);
	if (r2ndDuplicates.length > 0) {
		// set h1 with id of error to have innerHTML of "There are duplicates in the second row"
		return document.getElementById("error").innerHTML = "There are duplicates in the second row";
	}
	// check if there are any duplicates in the array r3rd
	var r3rdDuplicates = r3rd.filter(function(item, index){
			return r3rd.indexOf(item) != index;

	}
	);
	if (r3rdDuplicates.length > 0) {
		// set h1 with id of error to have innerHTML of "There are duplicates in the third row"
		return document.getElementById("error").innerHTML = "There are duplicates in the third row";
	}

    // check if there are any duplicates in the array r4th
    	var r4thDuplicates = r4th.filter(function(item, index){
    			return r4th.indexOf(item) != index;

    	}
    	);
    	if (r4thDuplicates.length > 0) {
    		// set h1 with id of error to have innerHTML of "There are duplicates in the fourth row"
			return document.getElementById("error").innerHTML = "There are duplicates in the fourth row";
    	}
    	// check if there are any duplicates in the array r5th
    	var r5thDuplicates = r5th.filter(function(item, index){
            return r5th.indexOf(item) != index;
        }
        );
	    if (r5thDuplicates.length > 0) {
	        // set h1 with id of error to have innerHTML of "There are duplicates in the fifth row"
	        return document.getElementById("error").innerHTML = "There are duplicates in the fifth row";

	    }
		// check if there are any duplicates in the array r6th
		var r6thDuplicates = r6th.filter(function(item, index){
			return r6th.indexOf(item) != index;
		}
		);

		if (r6thDuplicates.length > 0) {
			// set h1 with id of error to have innerHTML of "There are duplicates in the sixth row"
			return document.getElementById("error").innerHTML = "There are duplicates in the sixth row";
		}
		// check if there are any duplicates in the array r7th
		var r7thDuplicates = r7th.filter(function(item, index){
			return r7th.indexOf(item) != index;
		}
		);
		if (r7thDuplicates.length > 0) {
			// set h1 with id of error to have innerHTML of "There are duplicates in the seventh row"
			return document.getElementById("error").innerHTML = "There are duplicates in the seventh row";
		}
		// check if there are any duplicates in the array r8th
		var r8thDuplicates = r8th.filter(function(item, index){
			return r8th.indexOf(item) != index;
		}
		);
		if (r8thDuplicates.length > 0) {
			// set h1 with id of error to have innerHTML of "There are duplicates in the eighth row"
			return document.getElementById("error").innerHTML = "There are duplicates in the eighth row";
		}
		// check if there are any duplicates in the array r9th
		var r9thDuplicates = r9th.filter(function(item, index){
			return r9th.indexOf(item) != index;
		}
		);
		if (r9thDuplicates.length > 0) {
			// set h1 with id of error to have innerHTML of "There are duplicates in the ninth row"
			return document.getElementById("error").innerHTML = "There are duplicates in the ninth row";
		}
		// check if there are any duplicates in the array s1st
		var s1stDuplicates = s1st.filter(function(item, index){
			return s1st.indexOf(item) != index;
		}
		);
		if (s1stDuplicates.length > 0) {
			// set h1 with id of error to have innerHTML of "There are duplicates in the first column"
			return document.getElementById("error").innerHTML = "There are duplicates in top left square";
		}
		// do the same for the remaining arrays s2nd, s3rd, s4th, s5th, s6th, s7th, s8th, s9th
		var s2ndDuplicates = s2nd.filter(function(item, index){
			return s2nd.indexOf(item) != index;
		}
		);
		if (s2ndDuplicates.length > 0) {
			// set h1 with id of error to have innerHTML of "There are duplicates in the second column"
			return document.getElementById("error").innerHTML = "There are duplicates in top middle square";
		}
		var s3rdDuplicates = s3rd.filter(function(item, index){
			return s3rd.indexOf(item) != index;
		}
		);
		if (s3rdDuplicates.length > 0) {
			// set h1 with id of error to have innerHTML of "There are duplicates in the third column"
			return document.getElementById("error").innerHTML = "There are duplicates in top right square";
		}
		var s4thDuplicates = s4th.filter(function(item, index){
			return s4th.indexOf(item) != index;
		}
		);
		if (s4thDuplicates.length > 0) {
			// set h1 with id of error to have innerHTML of "There are duplicates in the fourth column"
			return document.getElementById("error").innerHTML = "There are duplicates in middle left square";
		}
		var s5thDuplicates = s5th.filter(function(item, index){
			return s5th.indexOf(item) != index;
		}
		);
		if (s5thDuplicates.length > 0) {
			// set h1 with id of error to have innerHTML of "There are duplicates in the fifth column"
			return document.getElementById("error").innerHTML = "There are duplicates in middle middle square";
		}
		var s6thDuplicates = s6th.filter(function(item, index){
			return s6th.indexOf(item) != index;
		}
		);
		if (s6thDuplicates.length > 0) {
			// set h1 with id of error to have innerHTML of "There are duplicates in the sixth column"
			return document.getElementById("error").innerHTML = "There are duplicates in middle right square";
		}
		var s7thDuplicates = s7th.filter(function(item, index){
			return s7th.indexOf(item) != index;
		}
		);
		if (s7thDuplicates.length > 0) {
			// set h1 with id of error to have innerHTML of "There are duplicates in the seventh column"
			return document.getElementById("error").innerHTML = "There are duplicates in bottom left square";
		}
		var s8thDuplicates = s8th.filter(function(item, index){
			return s8th.indexOf(item) != index;
		}
		);
		if (s8thDuplicates.length > 0) {
			// set h1 with id of error to have innerHTML of "There are duplicates in the eighth column"
			return document.getElementById("error").innerHTML = "There are duplicates in bottom middle square";
		}
		var s9thDuplicates = s9th.filter(function(item, index){
			return s9th.indexOf(item) != index;
		}
		);
		if (s9thDuplicates.length > 0) {
			// set h1 with id of error to have innerHTML of "There are duplicates in the ninth column"
			return document.getElementById("error").innerHTML = "There are duplicates in bottom right square";
		}
		// if there are no duplicates in any of the arrays, set h1 with id of error to have innerHTML of ""

		return document.getElementById("error").innerHTML = "";

}

// only do the checkvalues function if the url is sudoku.html
if (window.location.href.indexOf("sudoku.html") > -1) {
	checkValues();
}

// Get references to the file input and submit button
    const fileInput = document.getElementById('fileInput');
    const submitButton = document.getElementById('submitButton');

    // Add an event listener to the file input
    fileInput.addEventListener('change', function() {
        // Enable the submit button if a file is selected, otherwise disable it
        if (fileInput.files.length > 0) {
            submitButton.disabled = false;
        } else {
            submitButton.disabled = true;
        }
    });





