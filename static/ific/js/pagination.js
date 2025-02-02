$(document).ready(() => {
    console.log("paginate class")
    function Paginate(common_class) {
        this.common_class = common_class

        remove_disabled_class: (classname) => {
            $(classname).removeClass('disabled')
        }

        add_disabled_class: (classname) => {
            $(classname).addClass('disabled')
        }

        function activate_page(common_class) {
            $(common_class).click(function () {

                $(this).addClass('active').siblings().removeClass('active');
            })
        }
    }
})