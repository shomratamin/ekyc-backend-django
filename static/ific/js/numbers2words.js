function translate_number_to_words(amount){
let _amount = amount.toString();
let words = '';
if(_amount.length > 8){
    let a = _amount.substring(0, _amount.length - 7);
    words = number_to_words(a);
    words = words + "Crores "
    // a = _amount.substring(_amount.length - 7);
    // words = words + number_to_words(a) + 'Crores ';
}
else{
    words = number_to_words(amount);
}

return words;
}

function number_to_words(amount) {
    var words = new Array();
    words[0] = '';
    words[1] = 'One';
    words[2] = 'Two';
    words[3] = 'Three';
    words[4] = 'Four';
    words[5] = 'Five';
    words[6] = 'Six';
    words[7] = 'Seven';
    words[8] = 'Eight';
    words[9] = 'Nine';
    words[10] = 'Ten';
    words[11] = 'Eleven';
    words[12] = 'Twelve';
    words[13] = 'Thirteen';
    words[14] = 'Fourteen';
    words[15] = 'Fifteen';
    words[16] = 'Sixteen';
    words[17] = 'Seventeen';
    words[18] = 'Eighteen';
    words[19] = 'Nineteen';
    words[20] = 'Twenty';
    words[30] = 'Thirty';
    words[40] = 'Forty';
    words[50] = 'Fifty';
    words[60] = 'Sixty';
    words[70] = 'Seventy';
    words[80] = 'Eighty';
    words[90] = 'Ninety';
    amount = amount.toString();
    var atemp = amount.split(".");
    var number = atemp[0].split(",").join("");
    var n_length = number.length;
    var words_string = "";
    if (n_length <= 9) {
        var n_array = new Array(0, 0, 0, 0, 0, 0, 0, 0, 0);
        var received_n_array = new Array();
        for (var i = 0; i < n_length; i++) {
            received_n_array[i] = number.substr(i, 1);
        }
        for (var i = 9 - n_length, j = 0; i < 9; i++, j++) {
            n_array[i] = received_n_array[j];
        }
        for (var i = 0, j = 1; i < 9; i++, j++) {
            if (i == 0 || i == 2 || i == 4 || i == 7) {
                if (n_array[i] == 1) {
                    n_array[j] = 10 + parseInt(n_array[j]);
                    n_array[i] = 0;
                }
            }
        }
        value = "";
        for (var i = 0; i < 9; i++) {
            if (i == 0 || i == 2 || i == 4 || i == 7) {
                value = n_array[i] * 10;
            } else {
                value = n_array[i];
            }
            if (value != 0) {
                words_string += words[value] + " ";
            }
            if ((i == 1 && value != 0) || (i == 0 && value != 0 && n_array[i + 1] == 0)) {
                if (value == 1) {
                    words_string += "Crore ";
                }
                else {
                    words_string += "Crores ";
                }
            }
            if ((i == 3 && value != 0) || (i == 2 && value != 0 && n_array[i + 1] == 0)) {
                if (value == 1) {
                    words_string += "Lakh ";
                }
                else {
                    words_string += "Lakhs ";
                }
            }
            if ((i == 5 && value != 0) || (i == 4 && value != 0 && n_array[i + 1] == 0)) {
                if (value == 1) {
                    words_string += "Thousand ";
                }
                else {
                    words_string += "Thousands ";
                }
            }
            if (i == 6 && value != 0 && (n_array[i + 1] != 0 && n_array[i + 2] != 0)) {
                if (value == 1) {
                    words_string += "Hundred and ";
                }
                else {
                    words_string += "Hundreds and ";
                }

            } else if (i == 6 && value != 0) {
                if (value == 1) {
                    words_string += "Hundred ";
                }
                else {
                    words_string += "Hundreds ";
                }
            }
        }
        words_string = words_string.split("  ").join(" ");
    }
    return words_string;
}



function translate_number_to_words_eng(number) {
    var language = {
      units: ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'],
      tens: ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'],
      scales: ['', 'thousand', 'million', 'billion', 'trillion', 'quadrillion', 'quintillion', 'sextillion', 'septillion', 'octillion', 'nonillion', 'decillion', 'undecillion', 'duodecillion', 'tredecillion', 'quatttuor-decillion', 'quindecillion', 'sexdecillion', 'septen-decillion', 'octodecillion', 'novemdecillion', 'vigintillion', 'centillion'],
      negative: 'minus',
      zero: 'zero',
      hundred: 'hundred',
      and: 'and'
    }
    var numberToString = number.toString().replace('-', '');
    var numberLength = numberToString.length;
    var sections = [];
    var words = [];
    var endPoint, integers, i;
    if (parseInt(number, 10) === 0) {
      return language.zero;
    }
    while (numberLength > 0) {
      endPoint = numberLength;
      sections.push(numberToString.slice((numberLength = Math.max(0, numberLength - 3)), endPoint));
    }
    for (i = 0; i < sections.length; i++) {
      integers = sections[i].split('').reverse().map(parseFloat);
      if (integers[1] === 1) {
        integers[0] += 10;
      }
      if (language.scales[i]) {
        words.push(language.scales[i]);
      }
      if (language.units[integers[0]]) {
        words.push(language.units[integers[0]]);
      }
      if (language.tens[integers[1]]) {
        words.push(language.tens[integers[1]]);
      }
      if (integers[0] || integers[1]) {
        if (integers[2] || (i === 0 && number > 100)) {
          words.push(language.and);
        }
      }
      if (language.units[integers[2]]) {
        words.push(language.units[integers[2]] + ' ' + language.hundred);
      }
    }
    if (number < 0) {
      words.push(language.negative);
    }
    return words.reverse().join(' ');
  }
