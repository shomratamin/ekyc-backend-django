function add_classes(element, classes) {
    let _classes = classes.split(' ')
    _classes.forEach(function (item, index) {
        if (typeof (element) !== 'undefined') {
            element.classList.add(item)
        }
    })
}

function remove_classes(element, classes) {
    let _classes = classes.split(' ')
    _classes.forEach(function (item, index) {
        if (typeof (element) !== 'undefined') {
            element.classList.remove(item)
        }
    })
}

class_invalid = 'fas fa-exclamation-circle fa-lg'
let class_valid = 'fas fa-check-circle fa-lg'
let class_empty = ''

function validate_on_submit(form_classname, form_inputs) {

    $('#wrapper').delegate(form_classname, 'submit', function (event) {

        let has_error = false
        let msg = ''

        for (let i = 0; i < form_inputs.length; i++) {

            let validation_rule = form_inputs[i].getAttribute('validation_rule')
            let value = form_inputs[i].value

            let parentofSelected = form_inputs[i].parentNode;
            let current_validation_message = parentofSelected.getElementsByClassName(validation_rule)[0]
            let current_validation_icon = parentofSelected.getElementsByClassName(validation_rule + '-icon')[0]

            if (validation_rule === "mobileNumber") {
                msg = check_mobile_number_validity(value)
                has_error |= msg.length
                current_validation_message.innerHTML = msg
                if (msg.length > 0 && current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_valid)
                    add_classes(current_validation_icon, class_invalid)
                }
                else if (current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_invalid)
                    add_classes(current_validation_icon, class_valid)
                }
            }

            if (validation_rule === "email") {
                msg = check_email_validity(value)
                has_error |= msg.length
                current_validation_message.innerHTML = msg
                if (msg.length > 0 && current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_valid)
                    add_classes(current_validation_icon, class_invalid)
                }
                else if (current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_invalid)
                    add_classes(current_validation_icon, class_valid)
                }
            }

            if (validation_rule === "email_optional") {
                msg = check_email_optional_validity(value)
                has_error |= msg.length
                current_validation_message.innerHTML = msg
                if (msg.length > 0 && current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_valid)
                    add_classes(current_validation_icon, class_invalid)
                }
                else if (current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_invalid)
                    add_classes(current_validation_icon, class_valid)
                }
            }

            if (validation_rule === "password") {
                // msg = check_password_validity(value)
                msg = ""
                has_error |= msg.length
                current_validation_message.innerHTML = msg
                if (msg.length > 0 && current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_valid)
                    add_classes(current_validation_icon, class_invalid)
                }
                else if (current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_invalid)
                    add_classes(current_validation_icon, class_valid)
                }
            }

            if (validation_rule === "cPassword") {
                msg = check_password_match($('#password').val(), value)
                has_error |= msg.length
                current_validation_message.innerHTML = msg
                if (msg.length > 0 && current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_valid)
                    add_classes(current_validation_icon, class_invalid)
                }
                else if (current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_invalid)
                    add_classes(current_validation_icon, class_valid)
                }
            }

            if (validation_rule === "terms-and-conditions") {
                if (!$('.terms-condition-input').is(":checked")) {
                    msg = 'You must agree with the terms and conditions'
                    has_error |= msg.length
                    current_validation_message.innerHTML = msg

                } else {
                    msg = ''
                    has_error |= msg.length
                    current_validation_message.innerHTML = msg

                }

            }

            if (validation_rule === "email_or_phone") {
                prediction = predict_phone_or_email(value)
                if (prediction === "email") {
                    msg = check_email_validity(value)
                } else if (prediction === "phone") {
                    msg = check_mobile_number_validity(value)
                } else {
                    msg = "You must enter either email or phone to login"
                }
                has_error |= msg.length
                current_validation_message.innerHTML = msg
                if (msg.length > 0 && current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_valid)
                    add_classes(current_validation_icon, class_invalid)
                }
                else if (current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_invalid)
                    add_classes(current_validation_icon, class_valid)
                }
            }


            if (validation_rule === 'image_file') {

                msg = check_image_validity(value)

                has_error |= msg.length
                current_validation_message.innerHTML = msg
            }
            if (validation_rule === 'nominee_image') {

                msg = check_nominee_image_validity(value)

                has_error |= msg.length
                current_validation_message.innerHTML = msg
            }
            if (validation_rule === 'etin') {

                msg = check_etin_validity(value)

                has_error |= msg.length
                current_validation_message.innerHTML = msg
                if (msg.length > 0 && current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_valid)
                    add_classes(current_validation_icon, class_invalid)
                }
                else if (current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_invalid)
                    add_classes(current_validation_icon, class_valid)
                }
            }
            if (validation_rule === 'account_number') {

                msg = check_account_number_validity(value)
                console.log(msg)

                has_error |= msg.length
                current_validation_message.innerHTML = msg
                if (msg.length > 0 && current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_valid)
                    add_classes(current_validation_icon, class_invalid)
                }
                else if (current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_invalid)
                    add_classes(current_validation_icon, class_valid)
                }
            }
            if (validation_rule === 'general_mobile_number') {

                msg = check_general_mobile_number_validity(value)
                console.log(msg)
                has_error |= msg.length
                current_validation_message.innerHTML = msg
                if (msg.length > 0 && current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_valid)
                    add_classes(current_validation_icon, class_invalid)
                }
                else if (current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_invalid)
                    add_classes(current_validation_icon, class_valid)
                }
            }
            if (validation_rule === 'nid_number') {

                msg = check_nominee_nid_validity(value)
                console.log(msg)
                has_error |= msg.length
                current_validation_message.innerHTML = msg
                if (msg.length > 0 && current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_valid)
                    add_classes(current_validation_icon, class_invalid)
                }
                else if (current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_invalid)
                    add_classes(current_validation_icon, class_valid)
                }
            }
            if (validation_rule === 'card_number') {

                msg = check_card_number_validity(value)
                console.log(msg)
                has_error |= msg.length
                current_validation_message.innerHTML = msg
                if (msg.length > 0 && current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_valid)
                    add_classes(current_validation_icon, class_invalid)
                }
                else if (current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_invalid)
                    add_classes(current_validation_icon, class_valid)
                }
            }
            if (validation_rule === 'only_text') {

                msg = check_card_number_validity(value)
                console.log(msg)
                has_error |= msg.length
                current_validation_message.innerHTML = msg
                if (msg.length > 0 && current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_valid)
                    add_classes(current_validation_icon, class_invalid)
                }
                else if (current_validation_icon != 'undefined') {
                    remove_classes(current_validation_icon, class_invalid)
                    add_classes(current_validation_icon, class_valid)
                }
            }


            for (let i = 0; i < 3; i++) {
                if (validation_rule === `percentage_[0]${i}`) {

                    msg = check_total_percentage()
                    has_error |= msg.length
                    current_validation_message.innerHTML = msg
                    if (msg.length > 0 && current_validation_icon != 'undefined') {
                        remove_classes(current_validation_icon, class_valid)
                        add_classes(current_validation_icon, class_invalid)
                    }
                    else if (current_validation_icon != 'undefined') {
                        remove_classes(current_validation_icon, class_invalid)
                        add_classes(current_validation_icon, class_valid)
                    }
                }

                if (validation_rule === `nominee_name_[0]${i}`) {

                    msg = check_nominee_name_validity(value)
                    console.log(msg)
                    has_error |= msg.length
                    current_validation_message.innerHTML = msg
                    if (msg.length > 0 && current_validation_icon != 'undefined') {
                        remove_classes(current_validation_icon, class_valid)
                        add_classes(current_validation_icon, class_invalid)
                    }
                    else if (current_validation_icon != 'undefined') {
                        remove_classes(current_validation_icon, class_invalid)
                        add_classes(current_validation_icon, class_valid)
                    }
                }
                if (validation_rule === `nominee_relation_[0]${i}`) {

                    msg = check_nominee_relation_validity(value)
                    has_error |= msg.length
                    current_validation_message.innerHTML = msg
                    if (msg.length > 0 && current_validation_icon != 'undefined') {
                        remove_classes(current_validation_icon, class_valid)
                        add_classes(current_validation_icon, class_invalid)
                    }
                    else if (current_validation_icon != 'undefined') {
                        remove_classes(current_validation_icon, class_invalid)
                        add_classes(current_validation_icon, class_valid)
                    }
                }
                if (validation_rule === `nominee_dob_[0]${i}`) {

                    msg = check_dob_validity(value)
                    has_error |= msg.length
                    current_validation_message.innerHTML = msg
                    if (msg.length > 0 && current_validation_icon != 'undefined') {
                        remove_classes(current_validation_icon, class_valid)
                        add_classes(current_validation_icon, class_invalid)
                    }
                    else if (current_validation_icon != 'undefined') {
                        remove_classes(current_validation_icon, class_invalid)
                        add_classes(current_validation_icon, class_valid)
                    }
                }
                if (validation_rule === `nominee_photo_image_[0]${i}`) {
                    // msg = check_image_validity(value)
                    // has_error |= msg.length
                    // current_validation_message.innerHTML = msg
                    console.log("img", $(`#nominee_image_preview_[0]${i}`).css('background-image'))
                    msg = ''
                    has_error |= msg.length
                    current_validation_message.innerHTML = msg
                }
            }

        }

        if (has_error) {
            event.preventDefault()
        }

        let _form = $(this)
        console.log(_form.attr('action'))
        // event.preventDefault()
        return;
    })
}



function check_total_percentage() {
    let error_message = ''
    let total = 0, per_0_num, per_1_num, per_2_num
    let per_0 = document.getElementById("percentage_0")

    let per_1 = document.getElementById("percentage_1")
    let per_2 = document.getElementById("percentage_2")

    if (per_0 && per_1 && per_2) {
        per_0_num = Number(per_0.value)
        per_1_num = Number(per_1.value)
        per_2_num = Number(per_2.value)
        total = per_0_num + per_1_num + per_2_num
    } else if (per_0 && per_1) {
        per_0_num = Number(per_0.value)
        per_1_num = Number(per_1.value)
        total = per_0_num + per_1_num
    } else {
        per_0_num = Number(per_0.value)
        total = per_0_num
    }
    console.log(total)

    if (total !== 100) {
        error_message = "Summation of all nominee percentages must be 100."
    }
    return error_message
}

function check_nominee_name_validity(name) {
    let error_message = ""
    let numbers = /[0-9]/g

    if (name.length === 0) {
        error_message = "Nominee name can not be empty."
    }
    else if (numbers.test(name.toLowerCase())) {
        error_message = "Nominee name should not contain any numbers"
    } else {
        error_message = ""
    }
    return error_message

}
function check_nominee_relation_validity(relation) {
    let error_message = ""
    let numbers = /[0-9]/g

    if (relation.length === 0) {
        error_message = "You must specify your relationship with nominee."
    }
    else if (numbers.test(relation.toLowerCase())) {
        error_message = "Relationship should not contain any numbers"
    } else {
        error_message = ""
    }
    return error_message

}
function check_dob_validity(dob) {
    let error_message = ""

    if (dob.length === 0) {
        error_message = "You must specify your nominee date of birth."
    } else {
        error_message = ""
    }
    return error_message

}


function check_image_validity(img) {
    let error_message = ''
    if (!img) {
        error_message = `Please upload required image.`
    }
    else {
        error_message = ''
    }
    return error_message
}
function check_nominee_image_validity(img) {
    let error_message = ''
    if (!img) {
        error_message = `Please upload nominee image.`
    }
    else {
        error_message = ''
    }
    return error_message
}
function check_etin_validity(etin_number) {
    let error_message = ''
    if (etin_number.length === 12 || etin_number.length === 0) {
        error_message = ''
    }
    else {
        error_message = 'Invalid E-Tin Number.'
    }
    return error_message
}



function check_account_number_validity(number) {
    let error_message = ''

    let regex_numbers = /^[0-9]+$/

    for (let i = 0; i < number.length; i++) {
        if (regex_numbers.test(charAt(i))) {
            error_message = ''
        }
        else if (number.length === 0) {
            error_message = ''
        }
        else {
            error_message = 'Invalid Account Number.'
            return
        }
    }
    return error_message
}
function check_card_number_validity(card_number) {
    let error_message = ''
    if (card_number.length > 16 || card_number.length < 15) {
        error_message = 'Invalid Card Number.'
    }
    else if (card_number.length === 0) {
        error_message = ''
    }
    else {
        error_message = ''
    }
    return error_message
}
function check_only_text_validity(text) {
    let error_message = ''
    let cap_letters = /^[A-Z]+$/
    let small_letters = /^[a-z]+$/

    for (let i = 0; i < text.length; i++) {
        if (!cap_letters.test(charAt(i)) || !small_letters.test(charAt(i))) {
            error_message = 'Text field should not contain any number or special character.'
        }
        else if (text.length === 0) {
            error_message = ''
        }
        else {
            error_message = ''
        }
    }

    return error_message
}


function check_general_mobile_number_validity(number) {
    let error_message = ''
    let num = number.toString()

    let regex_numbers = /^[0-9]+$/

    for (let i = 0; i < num.length; i++) {
        if (!regex_numbers.test(num.charAt(i))) {
            error_message = "Mobile number should not contain any letters."
            return error_message
        }
    }


    if (num.length === 0) {
        error_message = ""
    }
    else if (num.length != 11) {
        error_message = "Mobile Number is less than 11 digits"
    }

    return error_message
}

function check_nominee_nid_validity(number) {
    let error_message = ''
    let num = number.toString()

    let regex_numbers = /^[0-9]+$/

    for (let i = 0; i < num.length; i++) {
        if (!regex_numbers.test(num.charAt(i))) {
            error_message = "NID/Smart Card number should not contain any letters."
            return error_message
        }
    }


    if (num.length === 0) {
        error_message = ""
    }
    else if (num.length != 10 || num.length != 13 || num.length != 17) {
        error_message = "Invalid NID/Smart Card Number"
    }

    return error_message
}

function check_mobile_number_validity(number) {
    let error_message = ''
    let num = number.toString()

    let regex_numbers = /^[0-9]+$/

    for (let i = 0; i < num.length; i++) {
        if (!regex_numbers.test(num.charAt(i))) {
            error_message = "Mobile number should not contain any letters."
            return error_message
        }
    }


    if (num.length === 0) {
        error_message = "Mobile Number field is empty"
    }
    else if (!num.startsWith('1')) {
        error_message = "Mobile Number must start with 1"
    }
    else if (num.length < 10) {
        error_message = "Mobile Number is less than 10 digits"
    }
    else if (num.length > 10) {
        error_message = "Mobile Number is more than 10 digits"
    }
    return error_message
}


function check_email_validity(email) {
    console.log("called")
    let error_message = ''
    let reg_ex_email = /(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/
    let common_suffix = ['.com', '.io', '.bd', '.asia', '.ai', '.web', '.us', '.uk', '.tel', '.sl', '.sk', '.se', '.sd', '.sa', '.sch.uk', '.qa', '.ru', '.py', '.pt', '.pk', '.om', '.org.uk', '.np', '.net', '.net.uk', '.ng', '.my', '.mod.uk', '.mm', '.ml', '.mil', '.lk', '.info', '.ie', '.id', '.gov.uk', '.fr', '.firm', '.eu', '.eg', '.co.uk', '.ch', '.ca', '.bt', '.br', '.bt', '.biz', '.af', '.ae']

    if (email.length === 0) {
        error_message = "Email can not be empty."
    } else {
        if (!reg_ex_email.test(email.toLowerCase())) {
            error_message = "please enter a valid email address."
        }
        else {

            for (j = 0; j < common_suffix.length; j++) {
                if (!email.endsWith(common_suffix[j])) {
                    error_message = "Please enter a valid email address with valid suffix."
                    continue
                } else {
                    error_message = ""
                    return error_message
                }
            }


        }
    }


    return error_message
}

function check_email_optional_validity(email) {
    let error_message = ''
    let reg_ex_email = /(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/
    let common_suffix = ['.com', '.io', '.za', '.yu', '.yt', '.ye', '.web', '.vi', '.vn', '.ve', '.va', '.uz', '.uy', '.us', '.uk', '.ua', 'ug', '.tr', '.th', '.tel', 'sy', 'so', '.sl', '.sk', '.se', '.sd', '.sa', '.sch.uk', '.qa', '.ru', '.py', '.pt', '.pk', '.om', '.org.uk', '.np', '.net', '.net.uk', '.ng', '.my', '.mod.uk', '.mm', '.ml', '.mil', '.lk', '.info', '.ie', '.id', '.gov.uk', '.fr', '.firm', '.eu', '.eg', '.co.uk', '.ch', '.ca', '.bt', '.br', '.bt', '.biz', '.bd', '.asia', '.ai', '.af', '.ae']
    let ignored_suffix = 'ificbankbd.com'

    if (email.length === 0) {
        error_message = ''
    }
    else {
        if (!reg_ex_email.test(email.toLowerCase())) {
            error_message = "please enter a valid email address."
        }
        else {

            if (email.endsWith('ificbankbd.com') || email.endsWith('ificbank.bd.com')) {
                error_message = "Email associated with ific bank is prohibited"
                return error_message
            } else {
                for (j = 0; j < common_suffix.length; j++) {
                    if (!email.endsWith(common_suffix[j])) {
                        error_message = "Please enter a valid email address with valid suffix."
                        continue
                    } else {
                        error_message = ""
                        return error_message
                    }
                }
            }



        }
    }

    return error_message
}


function check_password_validity(password) {
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
        return error_message
    }
    else if (password.includes(' ')) {
        error_message = 'Password must not contain any blank space.'
        return error_message
    }
    else if (password.length < 8) {
        error_message = "Password must be atleast 8 characters long."
        return error_message
    }
    else if (cap_letter_count < 2) {
        error_message = 'Password should contain atleast 2 capital and 2 small letters, 2 numbers and 2 special characters.'
        return error_message
    }

    else if (small_letter_count < 2) {
        error_message = 'Password should contain atleast 2 capital and 2 small letters, 2 numbers and 2 special characters.'
        return error_message
    }

    else if (number_count < 2) {
        error_message = 'Password should contain atleast 2 capital and 2 small letters, 2 numbers and 2 special characters.'
        return error_message
    }

    else if (special_character_count < 2) {
        error_message = 'Password should contain atleast 2 capital and 2 small letters, 2 numbers and 2 special characters.'
        return error_message
    }

    else {
        error_message = ''
        return error_message
    }


}

function check_password_match(password_1, password_2) {
    let pass_1 = password_1.toString().trim()
    let pass_2 = password_2.toString().trim()
    let msg = ''
    if (pass_1 === pass_2 && pass_1 !== ("") && pass_2 !== ("")) {
        msg = ''
    } else {
        msg = 'Password Mismatch'
    }
    return msg
}


function predict_phone_or_email(value) {
    let letters = /^[A-Za-z]+$/
    let prediction = ''
    let has_at_sign = value.includes('@')
    if (has_at_sign) {
        prediction = "email"
    }
    else {
        for (let i = 0; i < value.length; i++) {
            if (letters.test(value.charAt(i))) {
                prediction = 'email'
                break
            } else {
                prediction = 'phone'
            }
        }
    }

    return prediction
}

function clear_on_click(input_class) {
    $(`${input_class}`).bind('click', function () {
        let validation_rule = $(this).attr('validation_rule')
        if (validation_rule != 'undefined') {
            $(this).siblings(`.${validation_rule}`).html("")
            let icon_class = `.${validation_rule}-icon`
            // $(this).siblings(icon_class).removeClass(class_valid)
            if ($(this).siblings(icon_class).hasClass('fa-exclamation-circle')) {
                $(this).siblings(icon_class).removeClass(class_invalid)
            }
        }
        $('.invalid_error').css('display', 'none')
    })
}



$(document).ready(function () {

    $("#wrapper").delegate(".dateselect", "click focus", function () {
        $(this).datepicker({
            format: 'yyyy/mm/dd',
            todayHighlidht: true,
            viewMode: 'decades'
        })
    })

    $("#wrapper").delegate(".dateselect", "changeDate", function () {
        $(this).datepicker('hide')
    })

    // $('#wrapper').delegate('a', 'click tap', function (event) {
    //     let url = $(this).attr('href');
    //     let page_title = $(this).attr('page-title');
    //     let is_modal = $(this).attr('data-toggle')
    //     if (typeof (page_title) === 'undefined' || page_title.length < 1) {
    //         if (is_modal !== 'modal') window.location = url;
    //     }
    //     else if (typeof (url) !== 'undefined' && url.indexOf('onboarding') !== -1) {
    //         event.preventDefault();
    //         $.get(url, function (data) {
    //             window.history.pushState("", page_title, url);
    //             document.title = page_title
    //             $('#wrapper').html(data);
    //         })
    //     }
    // })
})
// {{ resend_otp(request, user_pk, cmb) }}

$(document).ready(function () {
    $(document).delegate('#resend_otp', 'click tap', function () {

        let url = $(this).attr('resend_link');
        console.log(url)
        $.get(url, function (response) {
            console.log(response)
            response = response.trim()
            if (response === 'success') {
                $("#notify_container").css('transition', 'all 200ms')
                $("#notify_container").css('transform', 'translate(-50%, 9px)')
                setTimeout(function () {
                    $("#notify_container").css('transform', 'translate(-50%, -50px)')
                }, 5000)
            }
            // else if (response === 'failed') {
            //     $("#notify_container").css('transition', 'all 200ms')
            //     $("#notify_container").css('transform', 'translate(-50%, 9px)')
            //     setTimeout(function() {
            //         $("#notify_container").css('transform', 'translate(-50%, -50px)')
            //     }, 5000)
            // }

        })
    });
})








function get_filename(filepath) {
    let splitted_array = filepath.split('\\')
    let filename = splitted_array[splitted_array.length - 1]
    return filename
}


function base64_to_blob(b64Data, contentType, sliceSize) {
    contentType = contentType || '';
    sliceSize = sliceSize || 512;

    var byteCharacters = atob(b64Data);
    var byteArrays = [];

    for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
        var slice = byteCharacters.slice(offset, offset + sliceSize);

        var byteNumbers = new Array(slice.length);
        for (var i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }

        var byteArray = new Uint8Array(byteNumbers);

        byteArrays.push(byteArray);
    }

    var blob = new Blob(byteArrays, { type: contentType });
    return blob;
}


$(document).ready(function () {


    var inputs = document.getElementsByTagName("input")

    validate_on_submit('.needs-validation', inputs)
    clear_on_click('.form-control')
    clear_on_click('.terms-condition-input')
    clear_on_click('.custom-file-input')
    clear_on_click('.tin_number')

    $('.custom-file-input').on('change', function () {
        let filename = get_filename($(this).val())
        $(this).next('.custom-file-label').html(filename)
    })

    $('.countrycode').css("display", "none")
    $('#email_or_phone').on('input', show_or_hide_countrycode)

    function show_or_hide_countrycode(e) {
        let value = e.target.value
        prediction = predict_phone_or_email(value)
        if (prediction === "phone") {
            $('.countrycode').css("display", "inline")
        }
        else {
            $('.countrycode').css("display", "none")
        }
    }


    $('#wrapper').delegate('.logout-btn', 'click', function (event) {
        window.location = `/${app_route}/logout/`
    })

    $('#customer_status_filter').on('change', function () {
        var cstatus = $(this).val();
        if (cstatus) {
            let url = `/onboarding/customer-list/?cstatus=${cstatus}`
            window.location = url;
        }
        return false;
    });

    $('.avro-bangla-typing').avro();

    // highlight_select('profession')
})


// function highlight_select (select_element) {
//     let select = document.getElementById(select_element)
//     let selected_value = select.options[select.selectedIndex].value
//     console.log(selected_value)
// }




$(document).ready(function () {


    $('#wrapper').delegate('#add-nominee', 'click', function (event) {





        let current_number_of_tabs = nominee_count;
        nominee_count++;
        if (nominee_count > 3) {
            nominee_count = 3;
            return
        }
        let add_nominee_index = parseInt($(this).attr('add-nominee-index'))

        let tab_1_header = get_tab_header(add_nominee_index)
        let tab_1_content = get_tab_content(add_nominee_index)

        if (add_nominee_index == 1) {
            add_tab_header(tab_1_header, '#my_tab')
            add_tab_content(tab_1_content, '#my_tab_content')
            $('#nominee_tab_header_1').addClass('show active')
            $('#nominee_1').addClass('show active')

            $('#nominee_tab_header_0').removeClass('show active')
            $('#nominee_tab_header_2').removeClass('show active')
            $('#nominee_0').removeClass('show active')
            $('#nominee_2').removeClass('show active')

        }
        else if (add_nominee_index == 2) {
            add_tab_header(tab_1_header, '#my_tab')
            add_tab_content(tab_1_content, '#my_tab_content')
            $('#nominee_tab_header_2').addClass('show active')
            $('#nominee_2').addClass('show active')

            $('#nominee_tab_header_0').removeClass('show active')
            $('#nominee_tab_header_1').removeClass('show active')
            $('#nominee_0').removeClass('show active')
            $('#nominee_1').removeClass('show active')
        }

        if (add_nominee_index == 2) {
            add_nominee_index = 1
        }
        else {
            add_nominee_index = 2
        }
        $(this).attr('add-nominee-index', add_nominee_index)


        bind_validator()
        autocomplete()
    })




})

function add_active_class(element) {
    $(element).addClass("active")
}


function add_tab_header(tab_header, tab_id) {
    $(tab_id).append(tab_header)
}
function add_tab_content(tab_content, tab_id) {
    $(tab_id).append(tab_content)
}




function get_tab_header(i) {
    if (nominee_count == 2) {
        tab_title = '2nd Nominee'
    } else if (nominee_count == 3) {
        tab_title = '3rd Nominee'
    }
    let tab =
    {
        id: i,
        title: tab_title,
        href: `#nominee_${i}`,
        aria_controls: `nominee_${i}`,
        aria_selected: true,
        show_active: true,
        aria_labelledby: `nominee_tab_header_${i}`,
        input_nominee_name: `nominee_name[${i}]`,
        input_relation: `nominee_relation[${i}]`,
        input_share_percentage: `nominee_share_percentage[${i}]`,
    }

    var link = ''
    if (user_type == 'agent') {
        link = `/${app_route}/manage-nominee/?tid=${tid}&uuid=${uuid}`
    }
    else if (user_type == 'customer') {
        link = `/${app_route}/manage-nominee/?uuid=${uuid}`
    }

    let tab_header_id = `nominee_tab_header_${tab.id}`
    let tab_header = ` 
    <li class="nav-item">
        <a class="nominee_tab_header nav-link active" id=${tab_header_id} data-toggle="tab" href=${tab.href} role="tab" aria-controls=${tab.aria_controls} aria-selected=${tab.aria_selected}>${tab.title}</a>
        <i id="nominee_close_${tab.id}" link="${link}" class="fa fa-window-close fa-lg close_nominee" nominee_index="${tab.id}" nominee_action="remove" style="color: #fff"></i>
    </li>`
    return tab_header
}


function get_tab_content(j) {

    let tab_content = `
    <div class="tab-pane fade show active" id="nominee_${j}" role="tabpanel" aria-labelledby="nominee_tab_header_${j}">
            <div class="nominee-box">

              <div class="nominee-info">
                <div class="md-form">
                  <input name="nominee_name_eng[0][${j}]" type="text" id="nominee_name_${j}" validation_rule="nominee_name_${j}" class="form-control">
                  <i class="nominee_name_${j}-icon"></i>
                  <label for="nominee_name_${j}">Name (in English)</label>
                  <div class="invalid-msg nominee_name_${j}"></div>
                </div>
                <div class="md-form">
                  <input name="nominee_dob[0][${j}]" type="text" id="nominee_dob_${j}" index="${j}" class="form-control nominee_dob dateselect" readonly">
                  <span class=" input-group-addon calender_icon"><i class="fa fa-calendar"></i></span>
                  <label class="active" for="nominee_dob_${j}">Date of Birth (yyyy/mm/dd)</label>
                </div>
                <div class="md-form d-flex justify-content-start">
                  <div class="md-form" style="margin: 0px 15px 0px 0px;">
                    <select name="nominee_id_type[0][${j}]" class="form-control ific-select" style="margin: 0; height: 41px">
                    <option value="NID/Smart Card" selected>NID/Smart Card</option>
                    <option value="Birth Certificate">Birth Certificate</option>
                    <option value="Passport">Passport</option>
                    <option value="Driving Licence">Driving Licence</option>
                    <option value="Employee ID">Employee ID</option>
                    <option value="Student ID">Student ID</option>
                    </select>
                  </div>
                  <div class="md-form" style="flex-grow: 1;margin: 0px;">
                    <input name="nominee_id_number[0][${j}]" type="text" id="nominee_id_number_${j}"  class="form-control">
                    <i class="nominee_id_number_${j}-icon"></i>
                    <label for="nominee_id_number_${j}">ID Number</label>
                    <div class="invalid-msg nominee_id_number_${j}"></div>
                </div>
                </div>
                <div class="md-form" style="flex-grow: 1;margin: 0px;">
                    <input name="nominee_account_number[0][${j}]" type="number" id="nominee_account_number_${j}" class="form-control">
                    <i class="nominee_account_number_${j}-icon"></i>
                    <label for="nominee_account_number_${j}">Account Number (if any)</label>
                    <div class="invalid-msg nominee_account_number_${j}"></div>
                </div>
                

              </div>

              <div class="nominee-image-primary" style="justify-content: flex-start">
                <h5 style="color: darkgray;">Nominee Image</h5>
                <div id="nominee_image_preview_${j}" class="nomineephoto"></div>
                <div class='file-input my-2' id="browse-nominee">
                  
                  <input data_input="nominee_photo_image_base64[0][${j}]" preview_window="nominee_image_preview_${j}" type='file' validation-rule="nominee_photo_image_${j}" id="nominee_photo_image_${j}" accept=".jpg, .png, .gif"  >
                  <input type="text" class="photo_or_image" name="nominee_photo_image_base64[0][${j}]" id="nominee_photo_image_base64[0][${j}]">
                  <span class='button'>Choose</span>
                  <span class='label' id="front-label" data-js-label>No file selected</span>
                  <div class="invalid-msg nominee_photo_image_${j}"></div>
                </div>
                <button type="button" class="capture-button" data-toggle="modal" data-target="#camera-modal-front-${j}">
                  Camera
                </button>
                
                <div class="modal fade" style="z-index: 999999999999" id="camera-modal-front-${j}" tabindex="-1" role="dialog" aria-labelledby="nominee_label_[${j}]" aria-hidden="true">
                  <div class="modal-dialog modal-xl">

                    <div class="modal-content">

                      <div class="modal-header">
                        <h5 class="modal-title" id="nominee_label_[${j}]">Capture nominee photo.</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                          <span aria-hidden="true">&times;</span>
                        </button>
                      </div>

                      <div class="modal-body">
                        <div id="camera-front-${j}" style="margin: 0 auto;"></div>
                      </div>

                      <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button type="button" id="camera-take-snapshot-${j}" class="btn btn-primary">Snap</button>
                      </div>

                    </div>

                  </div>
                </div>
              </div>

            </div>
            <div>
            <div class="row">
                <div class="col-md-6">
                    <div class="md-form">
                        <input name="nominee_relation[0][${j}]" type="text" id="nominee_relation_${j}" validation_rule="nominee_relation_${j}" class="form-control">
                        <i class="nominee_relation_${j}-icon"></i>
                        <label for="nominee_relation_${j}">Relationship with A/C holder</label>
                        <div class="invalid-msg nominee_relation_${j}"></div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="md-form">
                        <input name="nominee_share_percentage[0][${j}]" type="number" min="0" id="percentage_${j}" class="form-control"  >
                        <i class="percentage_${j}-icon"></i>
                        <label for="percentage_${j}">Percentage( % )</label>
                        <div class="invalid-msg percentage_${j}"></div>
                    </div>
                </div>
            </div>
            <div class="row">
            <div class="col-md-6">
              <div class="md-form">
                <input name="nominee_pres_address_eng[0][${j}]" type="text" id="nominee_pres_address_eng[0][${j}]" class="form-control" style="margin: 0" />
                <label for="nominee_pres_address_eng[0][${j}]" style="margin: 0">Present Address</label>
              </div>
            </div>
            <div class="col-md-6">
              <div class="md-form">
                <input name="nominee_perm_address_eng[0][${j}]" type="text" id="nominee_perm_address_eng[0][${j}]" class="form-control" style="margin: 0" />
                <label for="nominee_perm_address_eng[0][${j}]" style="margin: 0">Permanent Address</label>
              </div>
            </div>
          </div>

            <div class="form-group" style="margin-top: 30px; display: none;">
            <label class="" style="font-size: 18px; font-weight: 700; margin-right: 30px;">Is Nominee Minor?</label>
            <div class="radio-item">
              <input type="radio" id="nominee_minor_yes_${j}" value="1" class="nominee_minor" index="${j}" name="nominee_minor[0][${j}]">
              <label for="nominee_minor_yes_${j}">Yes</label>
            </div>
            <div class="radio-item" style="margin-top:0;">
              <input type="radio" id="nominee_minor_no_${j}" value="0" class="nominee_minor" index="${j}" name="nominee_minor[0][${j}]">
              <label for="nominee_minor_no_${j}">No</label>
            </div>
          </div>

          <div style="margin-bottom: 30px; display: none; width: 100%;" id="nominee_other_id_image_${j}">
              <h4 class="nominee_nid_box_${j}" style="font-size: 18px; font-weight: 700; text-align: center;">Upload Nominee ID Card</h4>
              <p class="" style="font-size: 12px; font-weight: 500; text-align: center; margin-bottom: 10px;">Total file size may not exceed 5MB</p>
              
              <div class="all-sides">
                <div class="front-side">
                  <h4 style="text-align: center;">Nominee ID Card</h4>
                  <div class="camera-component">
                    <div id="other_id_image_preview_${j}" margin: 0 auto;" class="frontsideimage"></div>

                    <div class="camera-buttons">

                      <div class='file-input' nid="back" id="browse-other" style="margin-right: 10px">
                        <input data_input="nominee_other_id_image_base64[0][${j}]" class="file-input" preview_window="other_id_image_preview_${j}" type='file' id="front_nid_file_input_${j}" accept=".jpg, .png, .gif" title="Nominee Other ID Card Image">
                        <input type="text" class="photo_or_image" name="nominee_other_id_image_base64[0][${j}]" id="nominee_other_id_image_base64[0][${j}]" >
                        <span class='button'>Choose</span>
                        <span class="label" id="other-label" data-js-label>No file selected</span>
                      </div>

                      
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div id="legal-guardian_${j}" style="margin-bottom: 30px; display: none;">
              <h4 class="" style="font-size: 22px; font-weight: 700;margin-bottom: 30px;">Legal Guardian Information</h4>
              <div class="row">
                <div class="col-md-6">
                  <div class="md-form" style="flex-grow: 1;">
                    <input name="nominee_minor_legal_guardian_name[0][${j}]" type="text" id="legal_guardian_name_${j}" class="form-control" style="margin: 0" data-parsley-required-if-checked="#nominee_minor_yes_${j}" data-parsley-validate-if-empty>
                    <label for="legal_guardian_name_${j}" style="margin: 0">Legal Guardian Name</label>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="md-form d-flex justify-content-start">
                    <div class="md-form" style="margin: 0px 15px 0px 0px;">
                      <select name="nominee_minor_legal_guardian_id_type[0][${j}]" class="form-control ific-select" style="margin: 0; height: 41px">
                      <option value="NID/Smart Card">NID/Smart Card</option>
                      <option value="Birth Certificate">Birth Certificate</option>
                      <option value="Passport">Passport</option>
                      <option value="Driving Licence">Driving Licence</option>
                      <option value="Employee ID">Employee ID</option>
                      <option value="Student ID">Student ID</option>
                      </select>
                    </div>
                    
                    <div class="md-form" style="flex-grow: 1;margin: 0px;">
                      <input name="nominee_minor_legal_guardian_id_number[0][${j}]" type="text" id="legal_guardian_id_${j}" class="form-control" style="margin: 0" />
                      <label for="legal_guardian_id_${j}" style="margin: 0">ID Number</label>
                    </div>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6">
                <div class="md-form">
                    <input name="nominee_minor_legal_guardian_dob[0][${j}]" type="text" id="legal_guardian_dob_${j}" index="${j}" class="form-control dateselect"  readonly">
                    <span class=" input-group-addon calender_icon"><i class="fa fa-calendar"></i></span>
                    <label for="legal_guardian_dob_${j}">Date of Birth (yyyy/mm/dd)</label>
                  </div>
                  
                </div>
                <div class="col-md-6">
                  <div class="md-form" style="flex-grow: 1;">
                    <input name="nominee_minor_legal_guardian_perm_address_eng[0][${j}]" type="text" id="legal_guardian_present_address_${j}" class="form-control" style="margin: 0" />
                    <label for="legal_guardian_present_address_${j}" style="margin: 0">Permanent Address</label>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6">
                  <div class="md-form" style="flex-grow: 1;">
                    <input name="nominee_minor_legal_guardian_relation[0][${j}]" type="text" id="legal_guardian_relation_${j}" class="form-control" style="margin: 0">
                    <label for="legal_guardian_relation_${j}" style="margin: 0">Relationship with minor</label>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="md-form" style="flex-grow: 1;">
                    <input name="nominee_minor_legal_guardian_contact_no[0][${j}]" type="number" id="legal_guardian_contact_number_${j}" class="form-control" style="margin: 0">
                    <label for="legal_guardian_contact_number_${j}" style="margin: 0">Contact Number</label>
                  </div>
                </div>
              </div>
              <!-- LEGAL GUARDIAN PHOTO IMAGE -->
              <div class="nominee-image-primary" style="justify-content: flex-start">
                <h5 style="color: darkgray;">Legal Guardian Image</h5>
                <div id="legal_guardian_image_preview_${j}" style="background-image: url({{customer_nominees[i].nominee_minor_legal_guardian_photo_image or ''}});" class="nomineephoto"></div>
                <div class='file-input my-2' id="browse-legal_guardian">
                  
                  <input data_input="nominee_minor_legal_guardian_photo_image[0][${j}]" preview_window="legal_guardian_image_preview_${j}" type='file' id="legal_guardian_image_${j}" accept=".jpg, .png, .gif"  >
                  <input type="text" class="photo_or_image" name="nominee_minor_legal_guardian_photo_image_base64[0][${j}]" id="nominee_minor_legal_guardian_photo_image[0][${j}]">
                  <span class='button'>Choose</span>
                  <span class='label' id="front-label" data-js-label>No file selected</span>
                  <div class="invalid-msg legal_guardian_photo_image_${j}"></div>
                </div>
                <button type="button" class="capture-button" data-toggle="modal" data-target="#camera-modal-front-legal-${j}">
                  Camera
                </button>

                <div class="modal fade" style="z-index: 999999999999" id="camera-modal-front-legal-${j}" tabindex="-1" role="dialog" aria-labelledby="legal_guardian_label_[${j}]" aria-hidden="true">
                  <div class="modal-dialog modal-xl">

                    <div class="modal-content">

                      <div class="modal-header">
                        <h5 class="modal-title" id="legal_guardian_label_[${j}]">Capture Legal Guardian's photo.</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                          <span aria-hidden="true">&times;</span>
                        </button>
                      </div>

                      <div class="modal-body">
                        <div id="camera-front-legal-${j}" style="margin: 0 auto;"></div>
                      </div>

                      <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button type="button" id="camera-take-snapshot-legal-${j}" class="btn btn-primary">Snap</button>
                      </div>

                    </div>

                  </div>
                </div>
                <div style="width: 100%;" id="legal_guardian_nid_images_${j}">
                <h4 class="legal_nid_box_${j}" style="font-size: 18px; font-weight: 700; text-align: center;">Upload Legal Guardians NID or Smart card front and back side page</h4>
                <p class="" style="font-size: 12px; font-weight: 500; text-align: center; margin-bottom: 10px;">Make sure to upload images into correct tab. Total file size may not exceed 5MB</p>

                <div class="all-sides">
                    <div class="front-side">
                        <h4 style="text-align: center;">Front Side</h4>
                        <div class="camera-component">
                            <div id="legal_guardian_front_side_image_preview_${j}" style="background-image: url({{ account_nominees[i].nominee_minor_legal_guardian_id_front_image }});margin: 0 auto;" class="frontsideimage"></div>
                            <div class="camera-buttons">

                                <div class='file-input' nid="back" id="browse-front" style="margin-right: 10px">
                                    <input data_input="nominee_minor_legal_guardian_id_front_image_base64[0][${j}]" class="file-input" preview_window="legal_guardian_front_side_image_preview_${j}" type='file' id="legal_guardian_front_nid_file_input_${j}" accept=".jpg, .png, .gif" title="NID/Smart Card Front"  >
                                    <input type="text" class="photo_or_image" name="nominee_minor_legal_guardian_id_front_image_base64[0][${j}]" id="nominee_minor_legal_guardian_id_front_image_base64[0][${j}]">
                                    <span class='button'>Choose</span>
                                    <span class="label" id="front-label" data-js-label>No file selected</span>
                                </div>



                            </div>
                        </div>
                    </div>
                    <div class="back-side">
                        <h4 style="text-align: center;">Back Side</h4>
                        <div class="camera-component">
                            <div id="legal_guardian_back_side_image_preview_${j}" style="background-image: url({{ account_nominees[i].nominee_minor_legal_guardian_id_back_image }});margin: 0 auto;" class="backsideimage"></div>
                            <div class="camera-buttons">

                                <div class='file-input' name="nominee_minor_legal_guardian_id_back_image_base64[0][${j}]" nid="back" id="browse-back" style="margin-right: 10px">
                                    <input data_input="nominee_minor_legal_guardian_id_back_image_base64[0][${j}]" class="file-input" preview_window="legal_guardian_back_side_image_preview_${j}" type='file' id="legal_guardian_back_nid_file_input_${j}" accept=".jpg, .png, .gif" title="NID/Smart Card Back"  >
                                    <input type="text" class="photo_or_image" name="nominee_minor_legal_guardian_id_back_image_base64[0][${j}]" id="nominee_minor_legal_guardian_id_back_image_base64[0][${j}]">
                                    <span class='button'>Choose</span>
                                    <span class='label' id="back-label" data-js-label>No file selected</span>
                                </div>


                            </div>
                        </div>
                    </div>
                </div>
            </div>
              </div>
            </div>
            <div style="width: 100%;" id="nominee_nid_images_${j}">
            <h4 class="nominee_nid_box_${j}" style="font-size: 18px; font-weight: 700; text-align: center;">Upload Nominee NID or Smart card front and back side page</h4>
            <h4 class="legal_nid_box_${j}" style="font-size: 18px; font-weight: 700; text-align: center; display: none;">Upload Legal Guardians NID or Smart card front and back side page</h4>
              <p class="" style="font-size: 12px; font-weight: 500; text-align: center; margin-bottom: 10px;">Make sure to upload images into correct tab. Total file size may not exceed 5MB</p>

              <div class="all-sides">
                <div class="front-side">
                  <h4 style="text-align: center;">Front Side</h4>
                  <div class="camera-component">
                    <div id="front_side_image_preview_${j}" style="margin: 0 auto;" class="frontsideimage"></div>

                    <div class="camera-buttons">

                      <div class='file-input' nid="back" id="browse-front" style="margin-right: 10px">
                        <input data_input="nominee_id_front_image_base64[0][${j}]" class="file-input" preview_window="front_side_image_preview_${j}" type='file' id="front_nid_file_input_${j}" accept=".jpg, .png, .gif" title="NID/Smart Card Front"  >
                        <input type="text" class="photo_or_image" name="nominee_id_front_image_base64[0][${j}]" id="nominee_id_front_image_base64[0][${j}]" >
                        <span class='button'>Choose</span>
                        <span class="label" id="front-label" data-js-label>No file selected</span>
                      </div>

                    </div>
                  </div>
                </div>
                <div class="back-side">
                  <h4 style="text-align: center;">Back Side</h4>
                  <div class="camera-component">
                    <div id="back_side_image_preview_${j}" style="margin: 0 auto;" class="backsideimage"></div>
                    
                    <div class="camera-buttons">

                      <div class='file-input' name="nominee_id_back_image_base64[0][${j}]" nid="back" id="browse-back" style="margin-right: 10px">
                        <input data_input="nominee_id_back_image_base64[0][${j}]" class="file-input" preview_window="back_side_image_preview_${j}" type='file' id="back_nid_file_input_${j}" accept=".jpg, .png, .gif" title="NID/Smart Card Back"  >
                        <input type="text" class="photo_or_image" name="nominee_id_back_image_base64[0][${j}]"  id="nominee_id_back_image_base64[0][${j}]">
                        <span class='button'>Choose</span>
                        <span class='label' id="back-label" data-js-label>No file selected</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
    `

    return tab_content
}








function read_image(input) {
    if (input.files && input.files[0]) {

        let reader = new FileReader();

        reader.onload = function (e) {
            let preview_window = $(input).attr('preview_window')
            $(`#${preview_window}`)
                .css('background-image', `url(${e.target.result})`)
            let data_input = $(input).attr('data_input')
            document.getElementById(`${data_input}`).value = e.target.result


            let _text = $(input).text()
            $(input).val()
            $(input).text(_text)
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function show_tab(tab_id, header_index) {
    show_tab_header(tab_id, header_index)
    show_tab_content(tab_id)
}
function hide_tab(tab_id) {
    hide_tab_header(tab_id)
    hide_tab_content(tab_id)
}

function show_tab_header(tab_id, header_index) {
    console.log("called header")
    $(`#nominee_tab_header_${tab_id}`).addClass("active")
    $(`#nominee_tab_header_${tab_id}`).text(`${header_index} Nominee`)
}

function show_tab_content(tab_id) {
    console.log("called content", tab_id)
    $(`#nominee_${tab_id}`).removeClass("fade")
    $(`#nominee_${tab_id}`).addClass("show active")
}

function hide_tab_header(tab_id) {
    console.log("called")
    $('#my_tab').children().each(function (index, value) {
        if (index === tab_id) {
            console.log($(this))
            $(this).remove()
        }
    })
}


function hide_tab_content(tab_id) {
    $('#my_tab_content').children().each(function (index, value) {
        if (index === tab_id) {
            $(this).remove()
        }
    })
}



$('document').ready(function () {
    $("#wrapper").delegate('.nominee_tab_header', 'click', function () {
        window.gflow_validator.validate()
    })

    $('#wrapper').delegate('input[type=number]', 'focus', function (e) {
        $(this).on('wheel.disableScroll', function (e) {
            e.preventDefault()
        })
    })
    $('#wrapper').delegate('input[type=number]', 'blur', function (e) {
        $(this).off('wheel.disableScroll')
    })



    $("#mNomineYes").hide();
    $("#mNomineNO").show();

    $("input[name='usResident']").click(function () {
        if ($("#usResidentYes").is(":checked")) {
            $("#mNomineYes").show();
            $("#mNomineNO").hide();
        } else {
            $("#mNomineNO").show();
            $("#mNomineYes").hide();
        }
    });

    $("#idType").change(function () {
        // alert($(this).val())
        if ($(this).val() == "") {
            $("#idTypeLabel").hide();
        }
        else {
            $("#idTypeLabel").show();
        }
    });
    // legal gurdian id type
    $("#idTypeL").change(function () {
        // alert($(this).val())
        if ($(this).val() == "") {
            $("#idTypeLabelL").hide();
        }
        else {
            $("#idTypeLabelL").show();
        }
    });


    // $("#mNomineNO").show();

    // $("input[name='account_operation_type']").click(function () {
    //     if ($("#Joint").is(":checked")) {
    //         $("#jointDiv").show();
    //         //$("#mNomineNO").hide();
    //     } else {
    //         // $("#mNomineNO").show();
    //         $("#jointDiv").hide();
    //     }
    // });

    // $("#wrapper").delegate("input[type=radio][name=transaction_limit_monthly]", "change", function(event) {
    //     if(this.value === "Above 1,00,000 BDT"){
    //         $("#deposit_and_currency_box").css("display", "block")
    //     } else {
    //         $("#deposit_and_currency_box").css("display", "none")
    //     }
    // })




    $('#wrapper').delegate('#nominee_close_1', 'click', function (event) {
        let url = $(this).attr('link');

        let nominee_index = $(this).attr('nominee_index');
        console.log('nominee_index c1', nominee_index)

        nominee_count--;
        if (nominee_count < 1) {
            nominee_count = 1
        }

        if (nominee_count == 2) {
            hide_tab(1)
            show_tab(2, '2nd')
        }
        else if (nominee_count == 1) {
            hide_tab(1)
            show_tab(0, '1st')
        }
        console.log('nominee count', nominee_count)
        if (nominee_count == 2) {
            $('#nominee_tab_header_2').text('2nd Nominee')
            $('#nominee_tab_header_2').addClass('show active')
            $('#nominee_2').addClass('show active')

            $('#nominee_tab_header_0').removeClass('show active')
            $('#nominee_tab_header_1').removeClass('show active')
            $('#nominee_0').removeClass('show active')
            $('#nominee_1').removeClass('show active')

        }
        else if (nominee_count == 1) {
            $('#nominee_tab_header_0').addClass('show active')
            $('#nominee_0').addClass('show active')
        }

        if (nominee_count == 1) {
            nominee_index = 1
        }
        $('#add-nominee').attr('add-nominee-index', nominee_index)



        let nominee_action = $(this).attr('nominee_action');


        $.post(url, { nominee_index_delete: nominee_index, nominee_action: nominee_action }, function (response) {
            response = response.trim()
        })
    })

    $('#wrapper').delegate('#nominee_close_2', 'click', function (event) {


        let url = $(this).attr('link');
        let nominee_index = $(this).attr('nominee_index');
        console.log('nominee_index c2', nominee_index)

        $('#add-nominee').attr('add-nominee-index', nominee_index)

        if (nominee_count)

            nominee_count--;
        if (nominee_count < 1) {
            nominee_count = 1
        }
        console.log('nominee count', nominee_count)

        if (nominee_count == 2) {
            hide_tab(2)
            show_tab(1, '2nd')
        }
        else if (nominee_count == 1) {
            hide_tab(1)
            show_tab(0, '1st')
        }
        if (nominee_count == 1) {
            $('#add-nominee').attr('add-nominee-index', 1)
        }

        let nominee_action = $(this).attr('nominee_action');

        if (access_channel == 'bankled') {
            $.post(url, { nominee_index_delete: nominee_index, nominee_action: nominee_action }, function (response) {
                response = response.trim()
            })
        }
        else {
            $.post(url, { nominee_index_delete: nominee_index, nominee_action: nominee_action, tid: -1 }, function (response) {
                response = response.trim()
            })
        }

    })



    $('#wrapper').delegate('.file-input [type="file"]', 'change', function () {
        if (!$(this).val()) return
        let value = $(this).val().replace(/^.*[\\\/]/, '')
        let truncatedString = value
        if (value.length > 13) {
            let start_string = value.substring(0, 9)
            let end_string = value.substring(value.length - 4, value.length)
            truncatedString = `${start_string}..${end_string}`
        }

        $(this).className += ' -chosen'

        $(this).next().next()[0].innerText = truncatedString
        read_image(this);

    });

    $('#wrapper').delegate('select[name^="nominee_id_type"]', 'change', function () {

        window.gflow_validator.validate()
    });
    $('#wrapper').delegate('select[name^="nominee_minor_legal_guardian_id_type"]', 'change', function () {

        window.gflow_validator.validate()
    });

    $('#wrapper').delegate('input[name^="nominee_dob"]', 'change', function () {

        window.gflow_validator.validate()
    });

    $('#wrapper').delegate('select[name^="otherbank_name"]', 'change', function () {

        let all_empty = true
        $('input[name^="otherbank_"] select[name^="otherbank_"]').each(function (i) {
            if ($(this).val().length > 0) {
                $('input[name^="otherbank_"] select[name^="otherbank_"]').attr('required', 'required')
                all_empty = false
            }
        })
        if (all_empty == true) {
            $('input[name^="otherbank_"] select[name^="otherbank_"]').removeAttr('required')
            // window.gflow_validator.validate()
        }

    });
    $('#wrapper').delegate('input[name^="otherbank_"]', 'keyup', function () {

        let all_empty = true
        $('input[name^="otherbank_"] select[name^="otherbank_"]').each(function (i) {
            if ($(this).val().length > 0) {
                $('input[name^="otherbank_"] select[name^="otherbank_"]').attr('required', 'required')
                all_empty = false
            }
        })
        if (all_empty == true) {
            $('input[name^="otherbank_"] select[name^="otherbank_"]').removeAttr('required')
            // window.gflow_validator.validate()
        }

    });


    $('#wrapper').delegate('input[name^="introducer_"]', 'keyup', function () {
        let all_empty = true
        $('input[name^="introducer_"]').each(function (i) {
            if ($(this).val().length > 0) {
                $('input[name^="introducer_"]').attr('required', 'required')
                all_empty = false
            }
        })
        if (all_empty == true) {
            $('input[name^="introducer_"]').removeAttr('required')
            window.gflow_validator.validate()
        }

    });


    $('#wrapper').delegate('select[name^="otherbankcard_name"]', 'change', function () {
        let all_empty = true
        $('input[name^="otherbankcard_"] select[name^="otherbankcard_"]').each(function (i) {
            if ($(this).val().length > 0) {
                $('input[name^="otherbankcard_"] select[name^="otherbankcard_"]').attr('required', 'required')
                all_empty = false
            }
        })
        if (all_empty == true) {
            $('input[name^="otherbankcard_"] select[name^="otherbankcard_"]').removeAttr('required')
            // window.gflow_validator.validate()
        }

    });

    $('#wrapper').delegate('input[name^="otherbankcard_"]', 'keyup', function () {
        let all_empty = true
        $('input[name^="otherbankcard_"] select[name^="otherbankcard_"]').each(function (i) {
            if ($(this).val().length > 0) {
                $('input[name^="otherbankcard_"] select[name^="otherbankcard_"]').attr('required', 'required')
                all_empty = false

            }
        })
        if (all_empty == true) {
            $('input[name^="otherbankcard_"] select[name^="otherbankcard_"]').removeAttr('required')
            // window.gflow_validator.validate()
        }

    });

    $('#wrapper').delegate('#customer_picture [type="file"]', 'change', function () {
        if (!$(this).val()) return
        let value = $(this).val().replace(/^.*[\\\/]/, '')
        let truncatedString = value
        if (value.length > 13) {
            let start_string = value.substring(0, 9)
            let end_string = value.substring(value.length - 4, value.length)
            truncatedString = `${start_string}..${end_string}`
        }

        $(this).className += ' -chosen'

        $(this).next().next()[0].innerText = truncatedString
        read_image(this);

    });

    if (typeof Webcam !== 'undefined') {
        Webcam.set({
            width: 800,
            height: 490,
            image_format: 'jpeg',
            jpeg_quality: 100,
        })

        function attach_camera(camera_id, div_id) {
            $('#wrapper').delegate(camera_id, 'show.bs.modal', function () {
                $('body').css('overflow', 'hidden')
                Webcam.attach(div_id)
            })
            $('#wrapper').delegate(camera_id, 'hidden.bs.modal', function () {
                $('body').css('overflow-y', 'auto')
                Webcam.reset()
            })
        }

        function snap_preview_send(camera_button_id, camera_id, preview_window_id, sender_input_name) {
            $('#wrapper').delegate(camera_button_id, 'click tap', function () {
                Webcam.snap(function (data_uri) {
                    Webcam.reset()
                    $(camera_id).modal('hide')
                    let n_index = preview_window_id.split('_')
                    n_index = n_index[n_index.length - 1]
                    $(preview_window_id).css('background-image', `url(${data_uri})`)
                    console.log('n_index', n_index)
                    $(`input[name="${sender_input_name}[0][${n_index}]"]`).val(data_uri)
                    // console.log("input = ", $(sender_input_id))
                    // $(sender_input_id).val(data_uri)
                })
            })
        }

        attach_camera("#camera-modal-front-0", "#camera-front-0")
        attach_camera("#camera-modal-front-1", "#camera-front-1")
        attach_camera("#camera-modal-front-2", "#camera-front-2")

        attach_camera("#camera-modal-front-legal-0", "#camera-front-legal-0")
        attach_camera("#camera-modal-front-legal-1", "#camera-front-legal-1")
        attach_camera("#camera-modal-front-legal-2", "#camera-front-legal-2")

        attach_camera("#camera_app_0", "#camera_window_0")
        attach_camera("#camera_app_1", "#camera_window_1")
        attach_camera("#camera_app_2", "#camera_window_2")


        snap_preview_send('#camera_snap_0', '#camera_app_0', '#applicant_photo_preview_0', "#customer_photo_from_app_image_base64[0]")
        snap_preview_send('#camera_snap_1', '#camera_app_1', '#applicant_photo_preview_1', "#customer_photo_from_app_image_base64[1]")
        snap_preview_send('#camera_snap_2', '#camera_app_2', '#applicant_photo_preview_2', "#customer_photo_from_app_image_base64[2]")


        snap_preview_send('#camera-take-snapshot-0', '#camera-modal-front-0', '#nominee_image_preview_0', "nominee_photo_image_base64")
        snap_preview_send('#camera-take-snapshot-1', '#camera-modal-front-1', '#nominee_image_preview_1', "nominee_photo_image_base64")
        snap_preview_send('#camera-take-snapshot-2', '#camera-modal-front-2', '#nominee_image_preview_2', "nominee_photo_image_base64")


        snap_preview_send('#camera-take-snapshot-legal-0', '#camera-modal-front-legal-0', '#legal_guardian_image_preview_0', "nominee_minor_legal_guardian_photo_image_base64")
        snap_preview_send('#camera-take-snapshot-legal-1', '#camera-modal-front-legal-1', '#legal_guardian_image_preview_1', "nominee_minor_legal_guardian_photo_image_base64")
        snap_preview_send('#camera-take-snapshot-legal-2', '#camera-modal-front-legal-2', '#legal_guardian_image_preview_2', "nominee_minor_legal_guardian_photo_image_base64")



    }

})





// let inputs = document.querySelectorAll('.file-input')

// for (let i = 0, len = inputs.length; i < len; i++) {
//    customInput(inputs[i])
// }


// const fileInput = el.querySelector('[type="file"]')
// const label = el.querySelector('[data-js-label]')


function autocomplete() {
    let r = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    $('input').attr('autocomplete', r);
    return r;
}

$(document).ready(function () {
    let r = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    autocomplete()


})

$(document).ready(function () {
    $("#wrapper").delegate(".left-controls a", "click tap", function (e) {
        let arrow = $(this).find('span').text()
        if (arrow === "›") {
            if (bank_account.tracking_number === null) {
                e.preventDefault()
            }
        } else {
            return
        }
    })
})