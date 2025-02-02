(function () {
  window.getCreditCardBrand = function (number, check_length) {
    var _j, _len1,
      card_name = [],
      number = number.replace(/[ -]/g, '');

    if (!number.length) {
      return;
    }

    var check_length = (typeof check_length !== 'undefined') ? check_length : false,
      card_types = [
        {
          name: 'amex',
          pattern: /^3[47]/,
          valid_length: [15]
        }, {
          name: 'china_union_pay',
          pattern: /^(62|88)/,
          valid_length: [16, 17, 18, 19]
        }, {
          name: 'dankort',
          pattern: /^5019/,
          valid_length: [16]
        }, {
          name: 'diners_club_carte_blanche',
          pattern: /^30[0-5]/,
          valid_length: [14]
        }, {
          name: 'diners_club_international',
          pattern: /^(30[0-5]|309|36|38|39)/,
          valid_length: [14]
        }, {
          name: 'diners_club_us_and_canada',
          pattern: /^(54|55)/,
          valid_length: [16]
        }, {
          name: 'discover',
          pattern: /^(6011|622(12[6-9]|1[3-9][0-9]|[2-8][0-9]{2}|9[0-1][0-9]|92[0-5]|64[4-9])|65)/,
          valid_length: [16]
        }, {
          name: 'jcb',
          pattern: /^35(2[89]|[3-8][0-9])/,
          valid_length: [16]
        }, {
          name: 'laser',
          pattern: /^(6304|670[69]|6771)/,
          valid_length: [16, 17, 18, 19]
        }, {
          name: 'maestro',
          pattern: /^(5018|5020|5038|6304|6759|676[1-3])/,
          valid_length: [12, 13, 14, 15, 16, 17, 18, 19]
        }, {
          name: 'mastercard',
          pattern: /^(5[1-5]|222[1-9]|22[3-9]|2[3-6]|27[01]|2720)/,
          valid_length: [16]
        }, {
          name: 'visa',
          pattern: /^4/,
          valid_length: [16]
        }, {
          name: 'visa_electron',
          pattern: /^(4026|417500|4508|4844|491(3|7))/,
          valid_length: [16]
        }
      ];

    for (_j = 0, _len1 = card_types.length; _j < _len1; _j++) {
      var card = card_types[_j];

      if (card.pattern.test(number)) {
        if (check_length) {
          if (card.valid_length.indexOf(number.length) > -1) {
            card_name.push(card.name);
          }
        } else {
          card_name.push(card.name);
        }

      }
    }

    if (card_name.length) {
      return card_name.join(' ');
    }

    return null;
  };

  function is_alpha_numeric(str) {
    var code, i, len;

    for (i = 0, len = str.length; i < len; i++) {
      code = str.charCodeAt(i);
      if (!(code > 47 && code < 58) && // numeric (0-9)
        !(code > 64 && code < 91) && // upper alpha (A-Z)
        !(code > 96 && code < 123)) { // lower alpha (a-z)
        return false;
      }
    }
    return true;
  };

  function is_numeric_only(str) {
    var code, i, len;

    for (i = 0, len = str.length; i < len; i++) {
      code = str.charCodeAt(i);
      if (!(code > 47 && code < 58)) { // lower alpha (a-z)
        return false;
      }
    }
    return true;
  };

  let days_difference = function (firstDate, secondDate) {
    let startDay = new Date(firstDate);
    let endDay = new Date(secondDate);

    let millisBetween = startDay.getTime() - endDay.getTime();
    let days = millisBetween / (1000 * 3600 * 24);

    return Math.round(days);
  }

  window.Parsley.addValidator('creditcard',
    function (value, requirement) {
      var digit, n, _ref2, valid, _j, _len1,
        sum = 0;

      if (value.length < 15 && value.length > 0) {
        return false
      }

      value = value.replace(/[ -]/g, '');
      _ref2 = value.split('').reverse();

      for (n = _j = 0, _len1 = _ref2.length; _j < _len1; n = ++_j) {
        digit = _ref2[n];
        digit = +digit;

        if (n % 2) {
          digit *= 2;

          if (digit < 10) {
            sum += digit;
          } else {
            sum += digit - 9;
          }
        } else {
          sum += digit;
        }
      }
      valid = (sum % 10 === 0);

      // Checks for specific brands
      if (valid && requirement.length) {
        var valid_cards = requirement.split(','),
          valid = false,
          card = getCreditCardBrand(value, true).split(' ');

        for (var c in card) {
          if (requirement.indexOf(card[c]) > -1) {
            valid = true;
          }
        }
      }

      return valid;
    }, 32)
    .addMessage('en', 'creditcard', 'This Credit Card number is invalid.');


  window.Parsley.addValidator('cvv',
    function (value) {
      return /^[0-9]{3,4}$/.test(value);
    }, 32)
    .addMessage('en', 'cvv', 'This value should be a valid CVV number');


  window.Parsley.addValidator('expirydate',
    function (value) {
      var currentTime, expiry, prefix, ref;

      if (value.indexOf('/') === -1) {
        return false;
      }

      var date = value.split('/'),
        month = date[0].trim(),
        year = date[1].trim();

      if (!/^\d+$/.test(month)) {
        return false;
      }
      if (!/^\d+$/.test(year)) {
        return false;
      }
      if (!(parseInt(month, 10) <= 12)) {
        return false;
      }
      if (year.length === 2) {
        prefix = (new Date).getFullYear();
        prefix = prefix.toString().slice(0, 2);
        year = prefix + year;
      }
      expiry = new Date(year, month);
      currentTime = new Date;
      expiry.setMonth(expiry.getMonth() - 1);
      expiry.setMonth(expiry.getMonth() + 1, 1);
      return expiry > currentTime;
    }, 32)
    .addMessage('en', 'expirydate', 'This value should be a valid date');

  window.Parsley
    .addValidator('requiredIfYes', function (value, requirement) {
      console.log(requirement)
      if (requirement.includes(',')) {
        let rs = requirement.split(',')
        if (jQuery(rs[0]).val() == 1 || jQuery(rs[1]).val() == 1) {
          return value.length > 0 ? true : false
        }
        else {
          return true
        }
      }
      else {
        if (jQuery(requirement).val() == 1) {
          return value.length > 0 ? true : false
        }
        else {
          return true
        }
      }
    }).addMessage('en', 'requiredIfYes', 'This value is required.');

  window.Parsley
    .addValidator('requiredIfNotSelected', function (value, requirement) {
      let name_value = requirement.split('__')
      console.log(value.length)
      if (jQuery(name_value[0]).val() != name_value[1]) {
        if (value.length < 1) {
          return value.length > 0 ? true : false
        }

        return true
      }

    }).addMessage('en', 'requiredIfNotSelected', 'This value is required.');

  window.Parsley
    .addValidator('requiredIfSelected', function (value, requirement) {
      let name_value = requirement.split('__')
      if (jQuery(name_value[0]).val() == name_value[1]) {
        if (value.length < 1) {
          return value.length > 0 ? true : false
        }

        return true
      }

    }).addMessage('en', 'requiredIfSelected', 'This value is required.');

  window.Parsley
    .addValidator('requiredIfNotEmpty', function (value, requirement) {
      if (requirement.includes(',')) {
        let rs = requirement.split(',')
        if (jQuery(rs[0]).val().length > 0 || jQuery(rs[1]).val().length > 0) {
          return value.length > 0 ? true : false
        }
        else {
          return true
        }
      }
      else {
        if (jQuery(requirement).val().length > 0) {
          return value.length > 0 ? true : false
        }
        else {
          return true
        }
      }

    }).addMessage('en', 'requiredIfNotEmpty', 'This value is required.');

  window.Parsley
    .addValidator('mobileNumberWithoutZero', function (value, requirement) {



      if (!value.startsWith('1')) {
        window.Parsley.addMessage('en', 'mobileNumberWithoutZero', 'Mobile Number must start with 1');
        return false
      }
      else if (value.length < 10) {
        window.Parsley.addMessage('en', 'mobileNumberWithoutZero', 'Mobile Number must be 10 digits');
        return false
      }
      else if (value.length > 10) {
        window.Parsley.addMessage('en', 'mobileNumberWithoutZero', 'Mobile Number is more than 10 digits');
        return false
      }

      return true

    });


  window.Parsley
    .addValidator('passwordPolicy', function (password, requirement) {
      let error_message = ''

      let numbers = /^[0-9]+$/
      let cap_letters = /^[A-Z]+$/
      let small_letters = /^[a-z]+$/
      let special_characters = '!"#$%&()*^*+-,./:;<=>?@[\\]_~`\'{|}'

      let number_count = 0
      let cap_letter_count = 0
      let small_letter_count = 0
      let special_character_count = 0
      let other_char_count = 0

      for (let i = 0; i < password.length; i++) {
        if (numbers.test(password.charAt(i))) {
          number_count += 1
        }
        else if (cap_letters.test(password.charAt(i))) {
          cap_letter_count += 1
        }
        else if (small_letters.test(password.charAt(i))) {
          small_letter_count += 1
        }
        else if (special_characters.includes(password.charAt(i))) {
          special_character_count += 1
        }
        else {
          other_char_count += 1
        }
      }

      if (password.length === 0) {
        error_message = "Password field is empty"
        window.Parsley.addMessage('en', 'passwordPolicy', error_message);
        return false
      }
      else if (password.includes(' ')) {
        error_message = 'Password must not contain any blank space.'
        window.Parsley.addMessage('en', 'passwordPolicy', error_message);
        return false
      }
      else if (password.length < 8) {
        error_message = "Password must be atleast 8 characters long."
        window.Parsley.addMessage('en', 'passwordPolicy', error_message);
        return false
      }
      else if (cap_letter_count < 2) {
        error_message = 'Password should contain atleast 2 capital and 2 small letters, 2 numbers and 2 special characters.'
        window.Parsley.addMessage('en', 'passwordPolicy', error_message);
        return false
      }

      else if (small_letter_count < 2) {
        error_message = 'Password should contain atleast 2 capital and 2 small letters, 2 numbers and 2 special characters.'
        window.Parsley.addMessage('en', 'passwordPolicy', error_message);
        return false
      }

      else if (number_count < 2) {
        error_message = 'Password should contain atleast 2 capital and 2 small letters, 2 numbers and 2 special characters.'
        window.Parsley.addMessage('en', 'passwordPolicy', error_message);
        return false
      }

      else if (special_character_count < 2) {
        error_message = 'Password should contain atleast 2 capital and 2 small letters, 2 numbers and 2 special characters.'
        window.Parsley.addMessage('en', 'passwordPolicy', error_message);
        return false
      }


      return true

    });

  window.Parsley
    .addValidator('mobileNumberWithZero', function (value, requirement) {

      let country_code = $(requirement).val()
      if (country_code != '+88') {
        return true
      }

      if (!value.startsWith('0')) {
        window.Parsley.addMessage('en', 'mobileNumberWithZero', 'Mobile Number must start with 0');
        return false
      }
      else if (value.length < 11) {
        window.Parsley.addMessage('en', 'mobileNumberWithZero', 'Mobile Number must be 11 digits');
        return false
      }
      else if (value.length > 11) {
        window.Parsley.addMessage('en', 'mobileNumberWithZero', 'Mobile Number is more than 11 digits');
        return false
      }

      return true

    });

  window.Parsley
    .addValidator('mobileNumberBangladesh', function (value, requirement) {



      if (!value.startsWith('0')) {
        window.Parsley.addMessage('en', 'mobileNumberBangladesh', 'Mobile Number must start with 0');
        return false
      }
      else if (value.length < 11) {
        window.Parsley.addMessage('en', 'mobileNumberBangladesh', 'Mobile Number must be 11 digits');
        return false
      }
      else if (value.length > 11) {
        window.Parsley.addMessage('en', 'mobileNumberBangladesh', 'Mobile Number is more than 11 digits');
        return false
      }

      return true

    });

  window.Parsley
    .addValidator('mobileNumberWithZeroRequiredIfAgeLessThan', function (value, requirement) {
      let compare_days = parseInt(requirement.split('__')[1]) * 365
      let selector = requirement.split('__')[0]
      let d = new Date();
      let today = d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate();
      let days = days_difference(today, jQuery(selector).val())

      if (days < compare_days) {
        if (!value.startsWith('0')) {
          window.Parsley.addMessage('en', 'mobileNumberWithZeroRequiredIfAgeLessThan', 'Mobile Number must start with 0');
          return false
        }
        else if (value.length < 11) {
          window.Parsley.addMessage('en', 'mobileNumberWithZeroRequiredIfAgeLessThan', 'Mobile Number must be 11 digits');
          return false
        }
        else if (value.length > 11) {
          window.Parsley.addMessage('en', 'mobileNumberWithZeroRequiredIfAgeLessThan', 'Mobile Number is more than 11 digits');
          return false
        }
      }

      return true

    });


  window.Parsley
    .addValidator('sumEquals', function (value, requirement) {
      let to_value = parseInt(requirement.split('__')[1])
      let selector = requirement.split('__')[0]
      let sum = 0
      let zero_percent_found = false
      jQuery(selector).each(function () {
        let val = parseInt(jQuery(this).val())
        if (val < 1) {
          zero_percent_found = true
          return false
        }
        sum += val
      })

      if (zero_percent_found) {
        window.Parsley.addMessage('en', 'sumEquals', `No nominee can have share less than 1%`);
        return false
      }
      if (sum !== to_value) {
        window.Parsley.addMessage('en', 'sumEquals', `Nominee percentage must add up to ${to_value}%`);
        return false;
      }

      return true

    });

  window.Parsley
    .addValidator('nidNumber', function (value, requirement) {
      if (value.length == 10 || value.length == 13 || value.length == 17) {
        return true
      }
      window.Parsley.addMessage('en', 'nidNumber', 'Id number is invalid');
      return false

    });

  var check_id_types = function (id_type, value, namespace) {
    let is_alphanumeric = is_alpha_numeric(value)
    let is_numericonly = is_numeric_only(value)

    if (id_type == 'NID/Smart Card') {
      if (!is_numericonly) {
        window.Parsley.addMessage('en', namespace, `${id_type} must be digits only`);
        return false
      }
      else if (value.length != 10 && value.length != 13 && value.length != 17) {
        window.Parsley.addMessage('en', namespace, `${id_type} must be 10 or 13 or 17 digits long`);
        return false
      }
    }
    else if (id_type == 'Birth Certificate') {
      if (!is_numericonly) {
        window.Parsley.addMessage('en', namespace, `${id_type} must be digits only`);
        return false
      }
      else if (value.length > 17) {
        window.Parsley.addMessage('en', namespace, `${id_type} can't be more than 17 digits`);
        return false
      }
    }
    else if (id_type == 'Passport') {
      if (value.length > 17) {
        window.Parsley.addMessage('en', namespace, `${id_type} can't be more than 17 characters`);
        return false
      }
    }
    else if (id_type == 'Driving Licence') {
      if (value.length > 17) {
        window.Parsley.addMessage('en', namespace, `${id_type} can't be more than 17 characters`);
        return false
      }
    }
    else if (id_type == 'Employee ID') {
      if (!is_numericonly) {
        window.Parsley.addMessage('en', namespace, `${id_type} must be digits only`);
        return false
      }
      else if (value.length > 17) {
        window.Parsley.addMessage('en', namespace, `${id_type} can't be more than 17 digits`);
        return false
      }
    }
    else if (id_type == 'Student ID') {
      if (!is_numericonly) {
        window.Parsley.addMessage('en', namespace, `${id_type} must be digits only`);
        return false
      }
      else if (value.length > 17) {
        window.Parsley.addMessage('en', namespace, `${id_type} can't be more than 17 digits`);
        return false
      }
    }
    return true
  }

  window.Parsley
    .addValidator('idType', function (value, requirement) {

      let id_type = jQuery(requirement).val()
      let is_valid_id = check_id_types(id_type, value, 'idType')
      return is_valid_id

    }).addMessage('en', 'idType', 'This value is required.');


  window.Parsley
    .addValidator('requiredIfAgeLessThan', function (value, requirement) {
      let compare_days = parseInt(requirement.split('__')[1]) * 365
      let selector = requirement.split('__')[0]
      let d = new Date();
      let today = d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate();
      let days = days_difference(today, jQuery(selector).val())

      if (days < compare_days) {
        if (value.length < 1) {
          window.Parsley.addMessage('en', 'requiredIfAgeLessThan', `This value is required.`);
          return false
        }
      }

      return true

    })

  window.Parsley
    .addValidator('requiredIfAgeGreaterThan', function (value, requirement) {
      let compare_days = parseInt(requirement.split('__')[1]) * 365
      let selector = requirement.split('__')[0]
      let d = new Date();
      let today = d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate();
      let days = days_difference(today, jQuery(selector).val())

      if (days > compare_days) {
        if (value.length < 1) {
          window.Parsley.addMessage('en', 'requiredIfAgeGreaterThan', `This value is required.`);
          return false
        }
      }

      return true

    })

  window.Parsley
    .addValidator('requiredIdTypeIfAgeLessThan', function (value, requirement) {
      let compare_days = 18 * 365
      let selectors = requirement.split(',')
      let d = new Date();
      let today = d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate();
      let days = days_difference(today, jQuery(selectors[0]).val())
      let id_type = jQuery(selectors[1]).val()

      if (days < compare_days) {
        console.log(id_type, value)
        if (value.length < 1) {
          window.Parsley.addMessage('en', 'requiredIdTypeIfAgeLessThan', `This value is required.`);
          return false
        }
        let is_valid_id = check_id_types(id_type, value, 'requiredIdTypeIfAgeLessThan')
        return is_valid_id

      }

      return true

    })


  window.Parsley
    .addValidator('requiredMinimumAge', function (value, requirement) {
      let compare_days = parseInt(requirement.split('__')[1]) * 365
      let selector = requirement.split('__')[0]
      let d = new Date();
      let today = d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate();
      let days = days_difference(today, jQuery(selector).val())

      if (days < compare_days || isNaN(days)) {
        window.Parsley.addMessage('en', 'requiredMinimumAge', `Minimum age must be ${requirement.split('__')[1]} years.`);
        return false
      }

      return true

    })

  window.Parsley
    .addValidator('requiredMinimumAgeIfAgeLessThan', function (value, requirement) {
      let compare_days = parseInt(requirement.split('__')[1]) * 365
      let selector = requirement.split('__')[0]
      let d = new Date();
      let today = d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate();
      let days = days_difference(today, jQuery(selector).val())
      let self_days = days_difference(today, value)

      if (days < compare_days) {
        if (self_days < compare_days || isNaN(self_days)) {
          window.Parsley.addMessage('en', 'requiredMinimumAgeIfAgeLessThan', `Minimum age must be ${requirement.split('__')[1]} years.`);
          return false
        }
      }

      return true

    })

  window.Parsley
    .addValidator('futureDateNotAllowed', function (value, requirement) {

      let d = new Date();
      let today = d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate();
      let days = days_difference(today, value)

      if (days < 0) {
        window.Parsley.addMessage('en', 'futureDateNotAllowed', `No one can born in future.`);
        return false
      }

      return true

    })

}());
